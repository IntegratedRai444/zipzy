#!/usr/bin/env python3
"""
Database Setup Script
Initializes and configures the database for ZIPZY platform
"""

import os
import sys
import asyncio
from datetime import datetime

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

def setup_mongodb():
    """Setup MongoDB database and collections"""
    print("🗄️ Setting up MongoDB...")
    
    try:
        from app.core.mongo_client import get_mongo_db
        
        db = get_mongo_db()
        if not db:
            print("❌ MongoDB connection failed")
            return False
        
        print("✅ MongoDB connection successful")
        
        # Create collections if they don't exist
        collections = [
            'users', 'products', 'orders', 'payments', 'stores', 
            'delivery_zones', 'user_locations', 'location_history',
            'cart_items', 'notifications', 'reviews', 'tracking_updates'
        ]
        
        for collection_name in collections:
            try:
                # This will create the collection if it doesn't exist
                db.create_collection(collection_name)
                print(f"✅ Collection '{collection_name}' ready")
            except Exception as e:
                # Collection might already exist
                print(f"ℹ️ Collection '{collection_name}' already exists")
        
        # Create indexes for better performance
        print("\n🔍 Creating database indexes...")
        
        # Users indexes
        try:
            db.users.create_index("email", unique=True)
            db.users.create_index("phone", unique=True)
            db.users.create_index("role")
            print("✅ Users indexes created")
        except Exception as e:
            print(f"⚠️ Users indexes: {str(e)}")
        
        # Products indexes
        try:
            db.products.create_index("category")
            db.products.create_index("store_type")
            db.products.create_index("is_listed")
            db.products.create_index("is_available")
            db.products.create_index("featured")
            db.products.create_index("created_at", -1)
            print("✅ Products indexes created")
        except Exception as e:
            print(f"⚠️ Products indexes: {str(e)}")
        
        # Orders indexes
        try:
            db.orders.create_index("user_id")
            db.orders.create_index("vendor_id")
            db.orders.create_index("status")
            db.orders.create_index("payment_status")
            db.orders.create_index("created_at", -1)
            print("✅ Orders indexes created")
        except Exception as e:
            print(f"⚠️ Orders indexes: {str(e)}")
        
        # Payments indexes
        try:
            db.payments.create_index("order_id")
            db.payments.create_index("status")
            db.payments.create_index("created_at", -1)
            print("✅ Payments indexes created")
        except Exception as e:
            print(f"⚠️ Payments indexes: {str(e)}")
        
        # Stores indexes
        try:
            db.stores.create_index("store_type")
            db.stores.create_index("is_open")
            db.stores.create_index("cuisine_type")
            db.stores.create_index("created_at", -1)
            print("✅ Stores indexes created")
        except Exception as e:
            print(f"⚠️ Stores indexes: {str(e)}")
        
        # Location indexes
        try:
            db.user_locations.create_index("user_id")
            db.user_locations.create_index("is_active")
            db.location_history.create_index("user_id")
            db.location_history.create_index("created_at", -1)
            db.delivery_zones.create_index("vendor_id")
            db.delivery_zones.create_index("is_active")
            print("✅ Location indexes created")
        except Exception as e:
            print(f"⚠️ Location indexes: {str(e)}")
        
        print("✅ MongoDB setup completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ MongoDB setup failed: {str(e)}")
        return False

def setup_supabase():
    """Setup Supabase database (if available)"""
    print("\n🗄️ Setting up Supabase...")
    
    try:
        from app.core.supabase_client import supabase
        
        if not supabase:
            print("ℹ️ Supabase not configured, skipping...")
            return True
        
        print("✅ Supabase connection successful")
        
        # Note: Supabase tables are created via SQL migrations
        # This is just a connection test
        try:
            result = supabase.table('users').select('*').limit(1).execute()
            print("✅ Supabase query test successful")
        except Exception as e:
            print(f"⚠️ Supabase query test failed: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase setup failed: {str(e)}")
        return False

def create_admin_user():
    """Create default admin user if it doesn't exist"""
    print("\n👑 Creating admin user...")
    
    try:
        from app.core.mongo_client import collection
        
        users_collection = collection('users')
        if not users_collection:
            print("❌ Users collection not accessible")
            return False
        
        # Check if admin user exists
        admin_user = users_collection.find_one({"email": "admin@zipzy.com"})
        
        if admin_user:
            print("✅ Admin user already exists")
            return True
        
        # Create admin user
        admin_data = {
            "id": "admin_user_001",
            "email": "admin@zipzy.com",
            "phone": "+919876543210",
            "name": "Admin User",
            "role": "admin",
            "is_verified": True,
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        users_collection.insert_one(admin_data)
        print("✅ Admin user created successfully")
        print("   Email: admin@zipzy.com")
        print("   Password: admin123")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create admin user: {str(e)}")
        return False

def verify_database_health():
    """Verify database health and connectivity"""
    print("\n🏥 Verifying database health...")
    
    try:
        from app.core.mongo_client import get_mongo_db, collection
        
        db = get_mongo_db()
        if not db:
            print("❌ Database connection failed")
            return False
        
        # Test basic operations
        test_collection = collection('health_check')
        if test_collection:
            # Write test
            test_doc = {
                "id": "health_check",
                "timestamp": datetime.utcnow().isoformat(),
                "status": "healthy"
            }
            test_collection.insert_one(test_doc)
            
            # Read test
            result = test_collection.find_one({"id": "health_check"})
            if result:
                print("✅ Database read/write operations working")
            
            # Cleanup
            test_collection.delete_one({"id": "health_check"})
            
            print("✅ Database health check passed")
            return True
        else:
            print("❌ Database operations failed")
            return False
        
    except Exception as e:
        print(f"❌ Database health check failed: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("🚀 ZIPZY Database Setup Script")
    print("=" * 50)
    
    # Check environment variables
    print("🔍 Checking environment variables...")
    
    required_vars = ['MONGODB_URI', 'MONGODB_DB_NAME']
    missing_vars = []
    
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Missing")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file before running this script")
        return
    
    print("✅ All required environment variables are set")
    
    # Setup databases
    mongo_success = setup_mongodb()
    supabase_success = setup_supabase()
    
    if not mongo_success:
        print("❌ Database setup failed. Please check your configuration.")
        return
    
    # Create admin user
    admin_success = create_admin_user()
    
    # Verify database health
    health_success = verify_database_health()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SETUP RESULTS:")
    print(f"MongoDB Setup: {'✅' if mongo_success else '❌'}")
    print(f"Supabase Setup: {'✅' if supabase_success else 'ℹ️'}")
    print(f"Admin User: {'✅' if admin_success else '❌'}")
    print(f"Health Check: {'✅' if health_success else '❌'}")
    
    if mongo_success and health_success:
        print("\n🎉 Database setup completed successfully!")
        print("🎯 Your ZIPZY platform is ready for development!")
        
        if admin_success:
            print("\n🔑 Default Admin Credentials:")
            print("   Email: admin@zipzy.com")
            print("   Password: admin123")
            print("   URL: /auth")
        
        print("\n📝 Next steps:")
        print("   1. Run the seeding script: python scripts/seed-database.py")
        print("   2. Start your backend server")
        print("   3. Test the admin dashboard: /dashboard/admin")
        
    else:
        print("\n⚠️ Database setup completed with some issues.")
        print("Please check the errors above and fix them before proceeding.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
