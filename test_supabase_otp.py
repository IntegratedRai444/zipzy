#!/usr/bin/env python3
"""
Test Supabase OTP endpoints directly
"""
import asyncio
import json
from app.core.supabase_client import get_supabase_client

async def test_supabase_otp():
    """Test Supabase OTP RPCs"""
    print("🔍 Testing Supabase OTP endpoints...")
    
    # Get Supabase client
    supabase = get_supabase_client()
    if not supabase:
        print("❌ Supabase client not configured")
        return
    
    print("✅ Supabase client configured")
    
    # Test 1: Request OTP
    print("\n📱 Testing OTP request...")
    try:
        result = supabase.rpc(
            'register_or_login_and_send_otp',
            {
                'p_name': 'Test User',
                'p_email': 'test@example.com',
                'p_mobile': '+911234567890',
                'p_purpose': 'login'
            }
        ).execute()
        
        if result.data:
            print("✅ OTP request successful")
            print(f"Response: {json.dumps(result.data, indent=2)}")
            
            # Extract OTP for verification test
            otp_data = result.data[0]
            email_otp = otp_data.get('email_otp')
            mobile_otp = otp_data.get('mobile_otp')
            
            if email_otp or mobile_otp:
                print(f"\n🔐 Testing OTP verification with code: {email_otp or mobile_otp}")
                
                # Test 2: Verify OTP
                verify_result = supabase.rpc(
                    'verify_otp',
                    {
                        'p_identifier': '+911234567890',
                        'p_code': email_otp or mobile_otp,
                        'p_purpose': 'login'
                    }
                ).execute()
                
                if verify_result.data:
                    print("✅ OTP verification successful")
                    print(f"Verification response: {json.dumps(verify_result.data, indent=2)}")
                else:
                    print("❌ OTP verification failed")
                    print(f"Error: {verify_result.error}")
            else:
                print("❌ No OTP generated")
        else:
            print("❌ OTP request failed")
            print(f"Error: {result.error}")
            
    except Exception as e:
        print(f"❌ Error testing OTP: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_supabase_otp())
