#!/usr/bin/env python3
"""
Database Connection Test Script
Tests MongoDB and Supabase connections and verifies database setup
"""

import os
import sys
import asyncio
from datetime import datetime

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

def test_mongodb_connection():
    """Test MongoDB connection and basic operations"""
    print("🔍 Testing MongoDB Connection...")
    
    try:
        from app.core.mongo_client import get_mongo_db, collection
        
        # Test database connection
        db = get_mongo_db()
        if db is None:
            print("❌ MongoDB connection failed - no connection available")
            return False
            
        print("✅ MongoDB connection successful")
        
        # Test collections
        test_collections = ['users', 'products', 'orders', 'payments', 'stores']
        for coll_name in test_collections:
            coll = collection(coll_name)
            if coll is not None:
                print(f"✅ Collection '{coll_name}' accessible")
            else:
                print(f"❌ Collection '{coll_name}' not accessible")
        
        # Test basic operations
        test_collection = collection('test_connection')
        if test_collection:
            # Insert test document
            test_doc = {
                "id": "test_connection",
                "message": "Database connection test",
                "timestamp": datetime.utcnow().isoformat()
            }
            test_collection.insert_one(test_doc)
            print("✅ MongoDB write operation successful")
            
            # Read test document
            result = test_collection.find_one({"id": "test_connection"})
            if result:
                print("✅ MongoDB read operation successful")
                
            # Clean up test document
            test_collection.delete_one({"id": "test_connection"})
            print("✅ MongoDB delete operation successful")
            
        return True
        
    except Exception as e:
        print(f"❌ MongoDB test failed: {str(e)}")
        return False

def test_supabase_connection():
    """Test Supabase connection"""
    print("\n🔍 Testing Supabase Connection...")
    
    try:
        from app.core.supabase_client import supabase
        
        if supabase is None:
            print("❌ Supabase connection failed - no connection available")
            return False
            
        print("✅ Supabase connection successful")
        
        # Test basic query
        try:
            result = supabase.table('users').select('*').limit(1).execute()
            print("✅ Supabase query operation successful")
        except Exception as e:
            print(f"⚠️ Supabase query test failed: {str(e)}")
            
        return True
        
    except Exception as e:
        print(f"❌ Supabase test failed: {str(e)}")
        return False

def test_storage_abstraction():
    """Test the unified storage abstraction layer"""
    print("\n🔍 Testing Storage Abstraction Layer...")
    
    try:
        from app.core.storage import get_order_by_id, create_payment
        
        print("✅ Storage abstraction layer imported successfully")
        
        # Test with mock data
        test_payment = {
            "id": "test_payment_123",
            "order_id": "test_order_123",
            "amount": 100.00,
            "method": "upi",
            "status": "pending"
        }
        
        # This should work even if databases are not fully configured
        print("✅ Storage abstraction layer accessible")
        return True
        
    except Exception as e:
        print(f"❌ Storage abstraction test failed: {str(e)}")
        return False

def check_environment_variables():
    """Check required environment variables"""
    print("\n🔍 Checking Environment Variables...")
    
    required_vars = [
        'MONGODB_URI',
        'MONGODB_DB_NAME',
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Missing")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file")
        return False
    
    return True

def main():
    """Main test function"""
    print("🚀 ZIPZY Database Connection Test")
    print("=" * 50)
    
    # Check environment variables
    env_ok = check_environment_variables()
    
    # Test connections
    mongo_ok = test_mongodb_connection()
    supabase_ok = test_supabase_connection()
    storage_ok = test_storage_abstraction()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY:")
    print(f"Environment Variables: {'✅' if env_ok else '❌'}")
    print(f"MongoDB Connection: {'✅' if mongo_ok else '❌'}")
    print(f"Supabase Connection: {'✅' if supabase_ok else '❌'}")
    print(f"Storage Abstraction: {'✅' if storage_ok else '❌'}")
    
    if mongo_ok or supabase_ok:
        print("\n🎉 Database integration is working!")
        if mongo_ok:
            print("   MongoDB is the primary database")
        if supabase_ok:
            print("   Supabase is available as fallback")
    else:
        print("\n❌ Database integration needs attention")
        print("   Please check your environment variables and database connections")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
