#!/usr/bin/env python3
"""
Database Seeding Script
Populates the database with sample data for testing and development
"""

import os
import sys
import asyncio
from datetime import datetime, timedelta
from uuid import uuid4

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

def seed_users():
    """Seed users table with sample data"""
    print("👥 Seeding users...")
    
    try:
        from app.core.mongo_client import collection
        
        users_collection = collection('users')
        if not users_collection:
            print("❌ Users collection not accessible")
            return False
        
        sample_users = [
            {
                "id": "admin_user_001",
                "email": "admin@zipzy.com",
                "phone": "+919876543210",
                "name": "Admin User",
                "role": "admin",
                "is_verified": True,
                "is_active": True,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": "customer_001",
                "email": "rahul@example.com",
                "phone": "+919876543211",
                "name": "Rahul Kumar",
                "role": "customer",
                "is_verified": True,
                "is_active": True,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": "partner_001",
                "email": "delivery@zipzy.com",
                "phone": "+919876543212",
                "name": "Delivery Partner",
                "role": "partner",
                "is_verified": True,
                "is_active": True,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
        ]
        
        for user in sample_users:
            users_collection.update_one(
                {"id": user["id"]}, 
                {"$set": user}, 
                upsert=True
            )
        
        print(f"✅ Seeded {len(sample_users)} users")
        return True
        
    except Exception as e:
        print(f"❌ Failed to seed users: {str(e)}")
        return False

def seed_products():
    """Seed products table with sample data"""
    print("🍕 Seeding products...")
    
    try:
        from app.core.mongo_client import collection
        
        products_collection = collection('products')
        if not products_collection:
            print("❌ Products collection not accessible")
            return False
        
        sample_products = [
            {
                "id": "product_001",
                "name": "Margherita Pizza",
                "description": "Classic tomato and mozzarella pizza",
                "price": 250.00,
                "category": "Pizza",
                "subcategory": "Italian",
                "stock": 50,
                "is_available": True,
                "is_listed": True,
                "featured": True,
                "tags": ["vegetarian", "italian", "pizza"],
                "images": ["/api/placeholder/400/300"],
                "store_type": "restaurant",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": "product_002",
                "name": "Chicken Burger",
                "description": "Juicy chicken patty with fresh vegetables",
                "price": 180.00,
                "category": "Burger",
                "subcategory": "Fast Food",
                "stock": 30,
                "is_available": True,
                "is_listed": True,
                "featured": False,
                "tags": ["non-vegetarian", "fast-food", "burger"],
                "images": ["/api/placeholder/400/300"],
                "store_type": "restaurant",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": "product_003",
                "name": "Veg Biryani",
                "description": "Aromatic rice with mixed vegetables and spices",
                "price": 200.00,
                "category": "Biryani",
                "subcategory": "Indian",
                "stock": 25,
                "is_available": True,
                "is_listed": True,
                "featured": True,
                "tags": ["vegetarian", "indian", "biryani"],
                "images": ["/api/placeholder/400/300"],
                "store_type": "restaurant",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
        ]
        
        for product in sample_products:
            products_collection.update_one(
                {"id": product["id"]}, 
                {"$set": product}, 
                upsert=True
            )
        
        print(f"✅ Seeded {len(sample_products)} products")
        return True
        
    except Exception as e:
        print(f"❌ Failed to seed products: {str(e)}")
        return False

def seed_stores():
    """Seed stores/restaurants table with sample data"""
    print("🏪 Seeding stores...")
    
    try:
        from app.core.mongo_client import collection
        
        stores_collection = collection('stores')
        if not stores_collection:
            print("❌ Stores collection not accessible")
            return False
        
        sample_stores = [
            {
                "id": "store_001",
                "name": "Pizza Palace",
                "description": "Best pizza in town with authentic Italian recipes",
                "store_type": "restaurant",
                "is_open": True,
                "hours": {
                    "monday": "10:00-22:00",
                    "tuesday": "10:00-22:00",
                    "wednesday": "10:00-22:00",
                    "thursday": "10:00-22:00",
                    "friday": "10:00-23:00",
                    "saturday": "10:00-23:00",
                    "sunday": "11:00-21:00"
                },
                "image_url": "/api/placeholder/400/300",
                "cuisine_type": "Italian",
                "address": "123 Main Street, Delhi",
                "phone": "+919876543213",
                "rating": 4.5,
                "review_count": 150,
                "delivery_time": "30-45 minutes",
                "minimum_order": 100.00,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": "store_002",
                "name": "Burger House",
                "description": "Delicious burgers and fast food",
                "store_type": "restaurant",
                "is_open": True,
                "hours": {
                    "monday": "11:00-21:00",
                    "tuesday": "11:00-21:00",
                    "wednesday": "11:00-21:00",
                    "thursday": "11:00-21:00",
                    "friday": "11:00-22:00",
                    "saturday": "11:00-22:00",
                    "sunday": "12:00-20:00"
                },
                "image_url": "/api/placeholder/400/300",
                "cuisine_type": "Fast Food",
                "address": "456 Park Avenue, Delhi",
                "phone": "+919876543214",
                "rating": 4.2,
                "review_count": 89,
                "delivery_time": "25-35 minutes",
                "minimum_order": 80.00,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
        ]
        
        for store in sample_stores:
            stores_collection.update_one(
                {"id": store["id"]}, 
                {"$set": store}, 
                upsert=True
            )
        
        print(f"✅ Seeded {len(sample_stores)} stores")
        return True
        
    except Exception as e:
        print(f"❌ Failed to seed stores: {str(e)}")
        return False

def seed_orders():
    """Seed orders table with sample data"""
    print("📦 Seeding orders...")
    
    try:
        from app.core.mongo_client import collection
        
        orders_collection = collection('orders')
        if not orders_collection:
            print("❌ Orders collection not accessible")
            return False
        
        # Create sample orders
        sample_orders = [
            {
                "id": "order_001",
                "user_id": "customer_001",
                "vendor_id": "store_001",
                "order_number": "ZIP123456",
                "status": "pending",
                "payment_status": "pending",
                "subtotal": 500.00,
                "delivery_fee": 25.00,
                "tax": 25.00,
                "total": 550.00,
                "delivery_address": "Hostel Block A, Room 101, Delhi University",
                "delivery_instructions": "Please call when arriving",
                "estimated_delivery": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": "order_002",
                "user_id": "customer_001",
                "vendor_id": "store_002",
                "order_number": "ZIP123457",
                "status": "preparing",
                "payment_status": "paid",
                "subtotal": 260.00,
                "delivery_fee": 20.00,
                "tax": 13.00,
                "total": 293.00,
                "delivery_address": "Apartment 5B, Green Park, Delhi",
                "delivery_instructions": "Leave at reception",
                "estimated_delivery": (datetime.utcnow() + timedelta(minutes=45)).isoformat(),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
        ]
        
        for order in sample_orders:
            orders_collection.update_one(
                {"id": order["id"]}, 
                {"$set": order}, 
                upsert=True
            )
        
        print(f"✅ Seeded {len(sample_orders)} orders")
        return True
        
    except Exception as e:
        print(f"❌ Failed to seed orders: {str(e)}")
        return False

def seed_delivery_zones():
    """Seed delivery zones table with sample data"""
    print("🗺️ Seeding delivery zones...")
    
    try:
        from app.core.mongo_client import collection
        
        zones_collection = collection('delivery_zones')
        if not zones_collection:
            print("❌ Delivery zones collection not accessible")
            return False
        
        sample_zones = [
            {
                "id": "zone_001",
                "vendor_id": "store_001",
                "name": "Delhi University Campus",
                "center_latitude": 28.7041,
                "center_longitude": 77.1025,
                "radius_km": 3.0,
                "base_delivery_fee": 25.00,
                "per_km_fee": 8.00,
                "is_active": True,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": "zone_002",
                "vendor_id": "store_002",
                "name": "North Campus Area",
                "center_latitude": 28.7041,
                "center_longitude": 77.1025,
                "radius_km": 4.0,
                "base_delivery_fee": 30.00,
                "per_km_fee": 10.00,
                "is_active": True,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
        ]
        
        for zone in sample_zones:
            zones_collection.update_one(
                {"id": zone["id"]}, 
                {"$set": zone}, 
                upsert=True
            )
        
        print(f"✅ Seeded {len(sample_zones)} delivery zones")
        return True
        
    except Exception as e:
        print(f"❌ Failed to seed delivery zones: {str(e)}")
        return False

def main():
    """Main seeding function"""
    print("🚀 ZIPZY Database Seeding Script")
    print("=" * 50)
    
    # Check if we can connect to database
    try:
        from app.core.mongo_client import get_mongo_db
        db = get_mongo_db()
        if not db:
            print("❌ Cannot connect to database. Please check your connection settings.")
            return
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return
    
    print("✅ Database connection successful")
    
    # Seed all tables
    results = []
    results.append(("Users", seed_users()))
    results.append(("Products", seed_products()))
    results.append(("Stores", seed_stores()))
    results.append(("Orders", seed_orders()))
    results.append(("Delivery Zones", seed_delivery_zones()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SEEDING RESULTS:")
    
    success_count = 0
    for table_name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {table_name}")
        if success:
            success_count += 1
    
    print(f"\n🎉 Successfully seeded {success_count}/{len(results)} tables!")
    
    if success_count == len(results):
        print("🎯 Database is ready for development and testing!")
    else:
        print("⚠️ Some tables failed to seed. Check the errors above.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
