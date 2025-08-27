#!/usr/bin/env python3
"""
UPI Payment Processor for ZIPZY
Handles UPI payment processing, QR code generation, and database integration
"""

import qrcode
import io
import base64
import uuid
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import sqlite3
import os

class UPIPaymentProcessor:
    def __init__(self, upi_id: str = "rishabhkap30@okicici", db_path: str = "zipzy.db"):
        self.upi_id = upi_id
        self.db_path = db_path
        self.merchant_name = "ZIPZY"
        self.currency = "INR"
        
        # Initialize database
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create payments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id TEXT PRIMARY KEY,
                order_id TEXT NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT DEFAULT 'upi',
                status TEXT DEFAULT 'pending',
                upi_id TEXT,
                customer_name TEXT,
                customer_phone TEXT,
                transaction_id TEXT,
                upi_transaction_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP
            )
        ''')
        
        # Create orders table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                total_amount REAL,
                status TEXT DEFAULT 'pending',
                payment_status TEXT DEFAULT 'pending',
                payment_method TEXT,
                delivery_address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_upi_qr_code(self, order_id: str, amount: float, customer_name: str = "", customer_phone: str = "") -> Dict[str, Any]:
        """Generate UPI QR code for payment"""
        
        # Generate unique transaction ID
        transaction_id = str(uuid.uuid4())
        
        # Create UPI payment URL
        upi_payment_url = f"upi://pay?pa={self.upi_id}&pn={self.merchant_name}&tn=Order_{order_id}&am={amount}&cu={self.currency}&tr={transaction_id}"
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(upi_payment_url)
        qr.make(fit=True)
        
        # Create QR image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Store payment in database
        payment_data = {
            'id': transaction_id,
            'order_id': order_id,
            'amount': amount,
            'payment_method': 'upi',
            'status': 'pending',
            'upi_id': self.upi_id,
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'transaction_id': transaction_id,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(minutes=15)).isoformat()
        }
        
        self.save_payment(payment_data)
        
        return {
            'order_id': order_id,
            'amount': amount,
            'upi_id': self.upi_id,
            'qr_code': f"data:image/png;base64,{qr_base64}",
            'payment_url': upi_payment_url,
            'expires_at': payment_data['expires_at'],
            'transaction_id': transaction_id
        }
    
    def save_payment(self, payment_data: Dict[str, Any]):
        """Save payment data to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO payments 
            (id, order_id, amount, payment_method, status, upi_id, customer_name, customer_phone, transaction_id, created_at, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            payment_data['id'],
            payment_data['order_id'],
            payment_data['amount'],
            payment_data['payment_method'],
            payment_data['status'],
            payment_data['upi_id'],
            payment_data['customer_name'],
            payment_data['customer_phone'],
            payment_data['transaction_id'],
            payment_data['created_at'],
            payment_data['expires_at']
        ))
        
        conn.commit()
        conn.close()
    
    def get_payment_status(self, order_id: str) -> Dict[str, Any]:
        """Get payment status for an order"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM payments WHERE order_id = ? ORDER BY created_at DESC LIMIT 1
        ''', (order_id,))
        
        payment = cursor.fetchone()
        conn.close()
        
        if payment:
            return {
                'order_id': order_id,
                'payment_status': payment[4],  # status column
                'amount': payment[2],  # amount column
                'upi_id': payment[5],  # upi_id column
                'transaction_id': payment[8],  # transaction_id column
                'created_at': payment[10],  # created_at column
                'expires_at': payment[12]  # expires_at column
            }
        
        return {
            'order_id': order_id,
            'payment_status': 'not_found',
            'amount': 0,
            'upi_id': None,
            'transaction_id': None,
            'created_at': None,
            'expires_at': None
        }
    
    def confirm_payment(self, order_id: str, payment_status: str = "completed", upi_transaction_id: str = None) -> Dict[str, Any]:
        """Confirm payment and update order status"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update payment status
        cursor.execute('''
            UPDATE payments 
            SET status = ?, upi_transaction_id = ?, updated_at = ?
            WHERE order_id = ?
        ''', (payment_status, upi_transaction_id, datetime.now().isoformat(), order_id))
        
        # Update order status
        order_status = 'confirmed' if payment_status == 'completed' else 'pending'
        cursor.execute('''
            UPDATE orders 
            SET payment_status = ?, status = ?, updated_at = ?
            WHERE id = ?
        ''', (payment_status, order_status, datetime.now().isoformat(), order_id))
        
        conn.commit()
        conn.close()
        
        return {
            'message': 'Payment status updated successfully',
            'order_id': order_id,
            'payment_status': payment_status,
            'order_status': order_status,
            'updated_at': datetime.now().isoformat()
        }
    
    def create_order(self, order_id: str, user_id: str, amount: float, delivery_address: str) -> Dict[str, Any]:
        """Create a new order"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO orders 
            (id, user_id, total_amount, delivery_address, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            order_id,
            user_id,
            amount,
            delivery_address,
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return {
            'order_id': order_id,
            'user_id': user_id,
            'amount': amount,
            'status': 'pending',
            'payment_status': 'pending',
            'created_at': datetime.now().isoformat()
        }
    
    def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Get order details"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = cursor.fetchone()
        conn.close()
        
        if order:
            return {
                'id': order[0],
                'user_id': order[1],
                'total_amount': order[2],
                'status': order[3],
                'payment_status': order[4],
                'payment_method': order[5],
                'delivery_address': order[6],
                'created_at': order[7],
                'updated_at': order[8]
            }
        
        return None
    
    def get_upi_details(self) -> Dict[str, Any]:
        """Get UPI payment details"""
        return {
            'upi_id': self.upi_id,
            'merchant_name': self.merchant_name,
            'currency': self.currency,
            'supported_apps': [
                'Google Pay',
                'PhonePe', 
                'Paytm',
                'BHIM',
                'Amazon Pay',
                'Any UPI App'
            ],
            'instructions': [
                '1. Open any UPI app',
                '2. Scan QR code or enter UPI ID',
                '3. Enter amount and complete payment',
                '4. Click confirm payment button'
            ]
        }
    
    def validate_payment(self, order_id: str, amount: float) -> bool:
        """Validate payment amount and order"""
        order = self.get_order(order_id)
        if not order:
            return False
        
        return abs(order['total_amount'] - amount) < 0.01  # Allow small floating point differences
    
    def cleanup_expired_payments(self):
        """Clean up expired payments"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE payments 
            SET status = 'expired', updated_at = ?
            WHERE expires_at < ? AND status = 'pending'
        ''', (datetime.now().isoformat(), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()

# Example usage
if __name__ == "__main__":
    # Initialize payment processor
    processor = UPIPaymentProcessor()
    
    # Example: Create an order
    order_id = "ORD-123456"
    user_id = "user-123"
    amount = 450.0
    delivery_address = "Hostel Block A, Room 101"
    
    # Create order
    order = processor.create_order(order_id, user_id, amount, delivery_address)
    print(f"Created order: {order}")
    
    # Generate UPI QR code
    qr_data = processor.generate_upi_qr_code(
        order_id=order_id,
        amount=amount,
        customer_name="Rahul Kumar",
        customer_phone="+91 98765 43210"
    )
    print(f"Generated QR code for order: {qr_data['order_id']}")
    print(f"UPI ID: {qr_data['upi_id']}")
    print(f"Amount: ₹{qr_data['amount']}")
    
    # Get payment status
    status = processor.get_payment_status(order_id)
    print(f"Payment status: {status['payment_status']}")
    
    # Confirm payment (simulate)
    confirmation = processor.confirm_payment(order_id, "completed", "UPI123456789")
    print(f"Payment confirmed: {confirmation}")
    
    # Get UPI details
    upi_details = processor.get_upi_details()
    print(f"UPI Details: {upi_details}")
