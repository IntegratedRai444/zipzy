"""
Python-based OTP authentication demo using MongoDB (pymongo).

Collections
- users: {_id, name, email, mobile, otp, otp_expiry}

Environment (optional)
- MONGODB_URI=mongodb://localhost:27017
- MONGODB_DB=zipzy_demo
- MONGODB_USERS_COLLECTION=users

Usage
  python scripts/mongo_otp_demo.py
"""

import os
import sys
import random
from datetime import datetime, timedelta, timezone
from typing import Optional

from pymongo import MongoClient
from bson import ObjectId


# -----------------------------
# MongoDB Connection Utilities
# -----------------------------

def get_mongo_client() -> MongoClient:
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    return MongoClient(uri)


def get_users_collection():
    client = get_mongo_client()
    db_name = os.getenv("MONGODB_DB", "zipzy_demo")
    coll_name = os.getenv("MONGODB_USERS_COLLECTION", "users")
    return client[db_name][coll_name]


# -----------------------------
# OTP Core Functions
# -----------------------------

def generate_otp(user_id: str, ttl_minutes: int = 5) -> Optional[int]:
    """Generate a 6-digit OTP, store with expiry in user's document.

    Returns the OTP (int) on success, None if user is not found.
    """
    users = get_users_collection()
    user = users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return None

    otp = random.randint(100000, 999999)
    expiry = datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)

    users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"otp": otp, "otp_expiry": expiry}}
    )
    return otp


def send_otp(user_id: str) -> bool:
    """Fetch user's contact and print OTP to console (simulated send)."""
    users = get_users_collection()
    user = users.find_one({"_id": ObjectId(user_id)})
    if not user:
        print("User not found.")
        return False
    if "otp" not in user:
        print("OTP not generated yet. Call generate_otp first.")
        return False
    print(f"[DEV OTP] Send OTP {user['otp']} to email={user.get('email')} mobile={user.get('mobile')}")
    return True


def verify_otp(user_id: str, entered_otp: int) -> bool:
    """Verify OTP and expiry. Clear on success."""
    users = get_users_collection()
    user = users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return False

    otp = user.get("otp")
    expiry = user.get("otp_expiry")
    now = datetime.now(timezone.utc)

    if otp is None or expiry is None:
        return False
    if now > expiry:
        return False
    if int(entered_otp) != int(otp):
        return False

    # Success → clear OTP fields
    users.update_one(
        {"_id": ObjectId(user_id)},
        {"$unset": {"otp": "", "otp_expiry": ""}}
    )
    return True


# -----------------------------
# Demo / Test Flow
# -----------------------------

def _ensure_demo_user() -> str:
    users = get_users_collection()
    demo = users.find_one({"email": "demo@zipzy.local"})
    if demo:
        return str(demo["_id"])
    res = users.insert_one({
        "name": "Demo User",
        "email": "demo@zipzy.local",
        "mobile": "+911234567890"
    })
    return str(res.inserted_id)


def main():
    print("Connecting to MongoDB and preparing demo user...")
    user_id = _ensure_demo_user()
    print(f"Demo user id: {user_id}")

    print("\nGenerating OTP...")
    otp = generate_otp(user_id)
    if otp is None:
        print("Failed to generate OTP (user not found).")
        sys.exit(1)
    print("OTP generated. (It will be printed below.)")

    print("\nSending OTP (console print)...")
    send_otp(user_id)

    try:
        entered = input("Enter the OTP you received: ").strip()
        ok = verify_otp(user_id, int(entered))
    except Exception:
        ok = False

    if ok:
        print("Authentication successful ✔")
    else:
        print("Authentication failed ✖ (invalid or expired OTP)")


if __name__ == "__main__":
    main()


