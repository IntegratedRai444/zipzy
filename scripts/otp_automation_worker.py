"""
OTP Automation Worker (MongoDB + Email + HTTP SMS, no Twilio)

Flow
- Insert a document into `otp_requests` to trigger an OTP (mobile/email).
- Worker detects the request (change stream or polling), generates a 6‑digit OTP,
  stores it in `users` with 5m expiry, sends via Email and/or HTTP SMS.
- Provides verify_otp(email_or_mobile, code) helper.
- Periodic cleanup removes expired OTPs.

Env
  MONGODB_URI=mongodb://localhost:27017
  MONGODB_DB=zipzy_auth
  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, EMAIL_FROM
  SMS_PROVIDER=http|none
  SMS_HTTP_URL, SMS_HTTP_METHOD=POST, SMS_HTTP_TO_FIELD=to, SMS_HTTP_MSG_FIELD=message
  SMS_HTTP_AUTH_HEADER, SMS_HTTP_AUTH_VALUE, SMS_HTTP_EXTRA_JSON

Usage
  # Terminal 1: run worker
  python scripts/otp_automation_worker.py worker

  # Terminal 2: enqueue a request (or call enqueue_otp_request from your app)
  python scripts/otp_automation_worker.py request +911234567890 test@example.com

  # Verify
  python scripts/otp_automation_worker.py verify test@example.com 123456
"""

from __future__ import annotations

import json
import os
import random
import smtplib
import sys
import time
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from typing import Any, Dict, Optional

import requests  # type: ignore
from bson import ObjectId
from pymongo import MongoClient, ASCENDING
from pymongo.collection import Collection


# ---------------- Mongo helpers ----------------

def get_db():
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    dbname = os.getenv("MONGODB_DB", "zipzy_auth")
    client = MongoClient(uri)
    db = client[dbname]
    # Create indexes
    db.users.create_index([("email", ASCENDING)], unique=False)
    db.users.create_index([("mobile", ASCENDING)], unique=False)
    db.users.create_index([("otp_expiry", ASCENDING)], unique=False)
    db.otp_requests.create_index([("status", ASCENDING), ("created_at", ASCENDING)])
    return db


# ---------------- Core logic ----------------

def _now() -> datetime:
    return datetime.now(timezone.utc)


def generate_code() -> int:
    return random.randint(100000, 999999)


def upsert_user(db, email: Optional[str], mobile: Optional[str]) -> Dict[str, Any]:
    q: Dict[str, Any] = {}
    if email:
        q["email"] = email
    if mobile:
        q["mobile"] = mobile
    user = db.users.find_one(q) if q else None
    if not user:
        user = {
            "name": (email or mobile or "user"),
            "email": email,
            "mobile": mobile,
        }
        user["_id"] = db.users.insert_one(user).inserted_id
    return user


def persist_otp(db, user_id: ObjectId, otp: int, ttl_minutes: int = 5) -> None:
    db.users.update_one(
        {"_id": user_id},
        {
            "$set": {
                "otp": otp,
                "otp_expiry": _now() + timedelta(minutes=ttl_minutes),
            }
        },
    )


# ---------------- Email/SMS senders ----------------

def send_email(to_email: str, subject: str, body: str) -> bool:
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    pwd = os.getenv("SMTP_PASS")
    from_addr = os.getenv("EMAIL_FROM", user or "no-reply@example.com")
    if not (host and user and pwd and to_email):
        # Dev fallback: log only
        print(f"[DEV EMAIL] to={to_email} subject={subject} body={body}")
        return True
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = to_email
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, pwd)
            server.sendmail(from_addr, [to_email], msg.as_string())
        return True
    except Exception as e:
        print(f"Email send failed: {e}")
        return False


def send_sms_http(to_phone: str, message: str) -> bool:
    provider = os.getenv("SMS_PROVIDER", "http").lower()
    if provider == "none":
        print(f"[DEV SMS] to={to_phone} msg={message}")
        return True
    url = os.getenv("SMS_HTTP_URL")
    if not url:
        print(f"[DEV SMS] to={to_phone} msg={message}")
        return True
    method = os.getenv("SMS_HTTP_METHOD", "POST").upper()
    to_field = os.getenv("SMS_HTTP_TO_FIELD", "to")
    msg_field = os.getenv("SMS_HTTP_MSG_FIELD", "message")
    auth_header = os.getenv("SMS_HTTP_AUTH_HEADER")
    auth_value = os.getenv("SMS_HTTP_AUTH_VALUE")
    extra = os.getenv("SMS_HTTP_EXTRA_JSON")
    headers = {"Content-Type": "application/json"}
    if auth_header and auth_value:
        headers[auth_header] = auth_value
    payload = {to_field: to_phone, msg_field: message}
    if extra:
        try:
            payload.update(json.loads(extra))
        except Exception:
            pass
    try:
        if method == "GET":
            r = requests.get(url, params=payload, headers=headers, timeout=10)
        else:
            r = requests.post(url, json=payload, headers=headers, timeout=10)
        return 200 <= r.status_code < 300
    except Exception as e:
        print(f"SMS send failed: {e}")
        return False


# ---------------- Worker ops ----------------

def process_pending(db) -> None:
    req: Dict[str, Any]
    req = db.otp_requests.find_one_and_update(
        {"status": "pending"}, {"$set": {"status": "processing"}}
    )
    if not req:
        return
    email = req.get("email")
    mobile = req.get("mobile")
    user = upsert_user(db, email, mobile)
    code = generate_code()
    persist_otp(db, user["_id"], code, ttl_minutes=5)
    body = f"Your ZIPZY OTP is {code}. It expires in 5 minutes. Do not share."
    ok_email = send_email(email, "Your ZIPZY OTP", body) if email else True
    ok_sms = send_sms_http(mobile, body) if mobile else True
    status = "sent" if (ok_email and ok_sms) else "failed"
    db.otp_requests.update_one({"_id": req["_id"]}, {"$set": {"status": status}})
    print(f"Processed request {req['_id']} email_ok={ok_email} sms_ok={ok_sms}")


def cleanup_expired(db) -> int:
    res = db.users.update_many(
        {"otp_expiry": {"$lt": _now()}}, {"$unset": {"otp": "", "otp_expiry": ""}}
    )
    return res.modified_count


def enqueue_otp_request(mobile: Optional[str], email: Optional[str]) -> str:
    db = get_db()
    doc = {
        "mobile": mobile,
        "email": email,
        "status": "pending",
        "created_at": _now(),
    }
    _id = db.otp_requests.insert_one(doc).inserted_id
    return str(_id)


def verify_otp(identifier: str, code: str) -> bool:
    db = get_db()
    user = db.users.find_one({"$or": [{"email": identifier}, {"mobile": identifier}]})
    if not user:
        return False
    if user.get("otp") is None or user.get("otp_expiry") is None:
        return False
    if _now() > user["otp_expiry"]:
        return False
    if str(user["otp"]) != str(code):
        return False
    db.users.update_one({"_id": user["_id"]}, {"$unset": {"otp": "", "otp_expiry": ""}})
    return True


def worker_loop() -> None:
    db = get_db()
    print("OTP worker started. Watching for pending requests...")
    last_cleanup = time.time()
    while True:
        process_pending(db)
        if time.time() - last_cleanup > 60:
            removed = cleanup_expired(db)
            if removed:
                print(f"Cleaned {removed} expired OTP(s)")
            last_cleanup = time.time()
        time.sleep(0.5)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "worker":
        worker_loop()
    elif len(sys.argv) >= 4 and sys.argv[1] == "request":
        _, __, mobile, email = sys.argv[:4]
        print(enqueue_otp_request(mobile if mobile != "none" else None,
                                  email if email != "none" else None))
    elif len(sys.argv) >= 4 and sys.argv[1] == "verify":
        _, __, ident, code = sys.argv[:4]
        print("OK" if verify_otp(ident, code) else "FAIL")
    else:
        print("Usage:\n  python scripts/otp_automation_worker.py worker\n  python scripts/otp_automation_worker.py request <mobile|none> <email|none>\n  python scripts/otp_automation_worker.py verify <email_or_mobile> <code>")


