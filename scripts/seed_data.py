#!/usr/bin/env python3
"""
Database Seeding Script for ZIPZY
Creates sample data for restaurants, menu items, and admin user
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db import engine, create_tables
from app.models.orm import *
from sqlmodel import Session
import bcrypt

async def seed_database():
    """Seed the database with initial data"""
    print("🌱 Starting database seeding...")
    
    # Create tables
    await create_tables()
    print("✅ Database tables created")
    
    with Session(engine) as session:
        # Create admin user
        admin_password = "Rishabhkapoor@0444"
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        admin_user = User(
            name="Rishabh Kapoor",
            email="admin@zipzy.com",
            phone="9876543210",
            hashed_password=hashed_password,
            is_student=False,
            points=1000,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Check if admin already exists
        existing_admin = session.query(User).filter(User.email == "admin@zipzy.com").first()
        if not existing_admin:
            session.add(admin_user)
            session.commit()
            print("✅ Admin user created: Rishabh Kapoor")
        else:
            print("ℹ️ Admin user already exists")
        
        # Create sample restaurants
        restaurants_data = [
            {
                "name": "Pizza Palace",
                "rating": 4.5,
                "cuisine": "pizza",
                "delivery_time": "25-35 min",
                "delivery_fee": 30,
                "min_order": 200,
                "image": "🍕",
                "is_open": True,
                "discount": "20% OFF"
            },
            {
                "name": "Burger House",
                "rating": 4.3,
                "cuisine": "burger",
                "delivery_time": "20-30 min",
                "delivery_fee": 25,
                "min_order": 150,
                "image": "🍔",
                "is_open": True,
                "discount": "15% OFF"
            },
            {
                "name": "Biryani Corner",
                "rating": 4.7,
                "cuisine": "biryani",
                "delivery_time": "30-40 min",
                "delivery_fee": 40,
                "min_order": 250,
                "image": "🍚",
                "is_open": True,
                "discount": "10% OFF"
            },
            {
                "name": "Chinese Wok",
                "rating": 4.2,
                "cuisine": "chinese",
                "delivery_time": "25-35 min",
                "delivery_fee": 35,
                "min_order": 180,
                "image": "🥢",
                "is_open": True,
                "discount": "25% OFF"
            }
        ]
        
        # Create vendors (restaurants)
        vendors = []
        for restaurant_data in restaurants_data:
            vendor = Vendor(
                name=restaurant_data["name"],
                rating=restaurant_data["rating"]
            )
            session.add(vendor)
            session.commit()
            vendors.append(vendor)
            print(f"✅ Restaurant created: {restaurant_data['name']}")
        
        # Create menu items
        menu_items_data = [
            # Pizza Palace items
            {"name": "Margherita Pizza", "price": 299, "vendor_id": vendors[0].id, "image": "🍕", "description": "Classic tomato sauce with mozzarella cheese", "is_veg": True, "is_spicy": False, "preparation_time": "20-25 min"},
            {"name": "Pepperoni Pizza", "price": 399, "vendor_id": vendors[0].id, "image": "🍕", "description": "Spicy pepperoni with melted cheese", "is_veg": False, "is_spicy": True, "preparation_time": "20-25 min"},
            {"name": "BBQ Chicken Pizza", "price": 449, "vendor_id": vendors[0].id, "image": "🍕", "description": "BBQ sauce with grilled chicken", "is_veg": False, "is_spicy": False, "preparation_time": "25-30 min"},
            
            # Burger House items
            {"name": "Classic Burger", "price": 199, "vendor_id": vendors[1].id, "image": "🍔", "description": "Juicy beef patty with fresh vegetables", "is_veg": False, "is_spicy": False, "preparation_time": "15-20 min"},
            {"name": "Veg Burger", "price": 179, "vendor_id": vendors[1].id, "image": "🍔", "description": "Plant-based patty with vegetables", "is_veg": True, "is_spicy": False, "preparation_time": "15-20 min"},
            {"name": "Spicy Chicken Burger", "price": 249, "vendor_id": vendors[1].id, "image": "🍔", "description": "Spicy chicken with jalapeños", "is_veg": False, "is_spicy": True, "preparation_time": "18-23 min"},
            
            # Biryani Corner items
            {"name": "Chicken Biryani", "price": 299, "vendor_id": vendors[2].id, "image": "🍚", "description": "Aromatic basmati rice with tender chicken", "is_veg": False, "is_spicy": True, "preparation_time": "25-30 min"},
            {"name": "Veg Biryani", "price": 249, "vendor_id": vendors[2].id, "image": "🍚", "description": "Fragrant rice with fresh vegetables", "is_veg": True, "is_spicy": False, "preparation_time": "20-25 min"},
            {"name": "Mutton Biryani", "price": 399, "vendor_id": vendors[2].id, "image": "🍚", "description": "Rich biryani with tender mutton", "is_veg": False, "is_spicy": True, "preparation_time": "30-35 min"},
            
            # Chinese Wok items
            {"name": "Chicken Fried Rice", "price": 199, "vendor_id": vendors[3].id, "image": "🥢", "description": "Stir-fried rice with chicken and vegetables", "is_veg": False, "is_spicy": False, "preparation_time": "15-20 min"},
            {"name": "Veg Noodles", "price": 179, "vendor_id": vendors[3].id, "image": "🥢", "description": "Stir-fried noodles with vegetables", "is_veg": True, "is_spicy": False, "preparation_time": "12-17 min"},
            {"name": "Chilli Chicken", "price": 299, "vendor_id": vendors[3].id, "image": "🥢", "description": "Spicy chicken with green chillies", "is_veg": False, "is_spicy": True, "preparation_time": "20-25 min"}
        ]
        
        for item_data in menu_items_data:
            item = Item(
                name=item_data["name"],
                price=item_data["price"],
                vendor_id=item_data["vendor_id"]
            )
            session.add(item)
            print(f"✅ Menu item created: {item_data['name']}")
        
        session.commit()
        print("✅ All menu items created")
        
        # Create sample user
        sample_user_password = "password123"
        hashed_sample_password = bcrypt.hashpw(sample_user_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        sample_user = User(
            name="John Student",
            email="john@student.com",
            phone="9876543211",
            hashed_password=hashed_sample_password,
            is_student=True,
            university="Delhi University",
            college_email="john.student@du.ac.in",
            student_id="DU2024001",
            points=500,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        existing_sample_user = session.query(User).filter(User.email == "john@student.com").first()
        if not existing_sample_user:
            session.add(sample_user)
            session.commit()
            print("✅ Sample user created: John Student")
        else:
            print("ℹ️ Sample user already exists")
        
        print("\n🎉 Database seeding completed successfully!")
        print("\n📋 Sample Data Created:")
        print(f"   👤 Admin User: Rishabh Kapoor (admin@zipzy.com)")
        print(f"   👤 Sample User: John Student (john@student.com)")
        print(f"   🍕 Restaurants: {len(restaurants_data)}")
        print(f"   🍽️ Menu Items: {len(menu_items_data)}")
        print(f"\n🔑 Admin Login:")
        print(f"   Email: admin@zipzy.com")
        print(f"   Password: Rishabhkapoor@0444")
        print(f"\n🔑 Sample User Login:")
        print(f"   Email: john@student.com")
        print(f"   Password: password123")

if __name__ == "__main__":
    asyncio.run(seed_database())
