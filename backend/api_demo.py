#!/usr/bin/env python3
"""
Satoshi Sensei API Demo Script

This script demonstrates all API endpoints with curl-like functionality.
Run this script to test the complete API functionality.
"""

import requests
import json
import time
import sys
from typing import Dict, Any, Optional


class SatoshiSenseiAPIDemo:
    """API Demo class for testing all endpoints."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token: Optional[str] = None
        self.user_id: Optional[str] = None
        self.wallet_id: Optional[str] = None
        self.recommendation_id: Optional[str] = None
    
    def print_header(self, title: str):
        """Print a formatted header."""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    
    def print_response(self, response: requests.Response, title: str = "Response"):
        """Print formatted response."""
        print(f"\n{title}:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        try:
            data = response.json()
            print(f"JSON Response:")
            print(json.dumps(data, indent=2))
        except:
            print(f"Text Response: {response.text}")
        
        return response
    
    def test_health_check(self):
        """Test health check endpoint."""
        self.print_header("Health Check")
        
        response = self.session.get(f"{self.base_url}/health")
        self.print_response(response, "Health Check")
        
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print("❌ Health check failed")
            return False
        return True
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        self.print_header("Root Endpoint")
        
        response = self.session.get(f"{self.base_url}/")
        self.print_response(response, "Root Endpoint")
        
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print("❌ Root endpoint failed")
            return False
        return True
    
    def test_user_signup(self):
        """Test user signup."""
        self.print_header("User Signup")
        
        signup_data = {
            "email": "demo@satoshisensei.ai",
            "password": "demo_password_123"
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/auth/signup",
            json=signup_data
        )
        self.print_response(response, "User Signup")
        
        if response.status_code == 200:
            data = response.json()
            self.user_id = data.get("id")
            print("✅ User signup successful")
            return True
        else:
            print("❌ User signup failed")
            return False
    
    def test_user_login(self):
        """Test user login."""
        self.print_header("User Login")
        
        login_data = {
            "email": "demo@satoshisensei.ai",
            "password": "demo_password_123"
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/auth/login",
            json=login_data
        )
        self.print_response(response, "User Login")
        
        if response.status_code == 200:
            data = response.json()
            self.auth_token = data.get("access_token")
            print("✅ User login successful")
            return True
        else:
            print("❌ User login failed")
            return False
    
    def test_get_current_user(self):
        """Test getting current user."""
        self.print_header("Get Current User")
        
        if not self.auth_token:
            print("❌ No auth token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.get(
            f"{self.base_url}/api/v1/auth/me",
            headers=headers
        )
        self.print_response(response, "Get Current User")
        
        if response.status_code == 200:
            print("✅ Get current user successful")
            return True
        else:
            print("❌ Get current user failed")
            return False
    
    def test_connect_wallet(self):
        """Test wallet connection."""
        self.print_header("Connect Wallet")
        
        if not self.auth_token:
            print("❌ No auth token available")
            return False
        
        wallet_data = {
            "address": "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
            "network": "stacks",
            "label": "Demo Wallet"
        }
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.post(
            f"{self.base_url}/api/v1/wallet/connect",
            json=wallet_data,
            headers=headers
        )
        self.print_response(response, "Connect Wallet")
        
        if response.status_code == 200:
            data = response.json()
            self.wallet_id = data.get("id")
            print("✅ Wallet connection successful")
            return True
        else:
            print("❌ Wallet connection failed")
            return False
    
    def test_get_user_wallets(self):
        """Test getting user wallets."""
        self.print_header("Get User Wallets")
        
        if not self.auth_token:
            print("❌ No auth token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.get(
            f"{self.base_url}/api/v1/wallet/",
            headers=headers
        )
        self.print_response(response, "Get User Wallets")
        
        if response.status_code == 200:
            print("✅ Get user wallets successful")
            return True
        else:
            print("❌ Get user wallets failed")
            return False
    
    def test_get_wallet_balances(self):
        """Test getting wallet balances."""
        self.print_header("Get Wallet Balances")
        
        if not self.auth_token or not self.wallet_id:
            print("❌ No auth token or wallet ID available")
            return False
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.get(
            f"{self.base_url}/api/v1/wallet/{self.wallet_id}/balances",
            headers=headers
        )
        self.print_response(response, "Get Wallet Balances")
        
        if response.status_code == 200:
            print("✅ Get wallet balances successful")
            return True
        else:
            print("❌ Get wallet balances failed")
            return False
    
    def test_get_strategy_recommendation(self):
        """Test getting strategy recommendation."""
        self.print_header("Get Strategy Recommendation")
        
        if not self.auth_token:
            print("❌ No auth token available")
            return False
        
        strategy_request = {
            "risk_tolerance": "medium",
            "investment_amount": 1000.0,
            "time_horizon": "long",
            "preferred_protocols": ["alex", "arkadiko"]
        }
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.post(
            f"{self.base_url}/api/v1/strategy/recommend",
            json=strategy_request,
            headers=headers
        )
        self.print_response(response, "Get Strategy Recommendation")
        
        if response.status_code == 200:
            data = response.json()
            self.recommendation_id = data.get("id")
            print("✅ Get strategy recommendation successful")
            return True
        else:
            print("❌ Get strategy recommendation failed")
            return False
    
    def test_get_user_recommendations(self):
        """Test getting user recommendations."""
        self.print_header("Get User Recommendations")
        
        if not self.auth_token:
            print("❌ No auth token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.get(
            f"{self.base_url}/api/v1/strategy/recommendations",
            headers=headers
        )
        self.print_response(response, "Get User Recommendations")
        
        if response.status_code == 200:
            print("✅ Get user recommendations successful")
            return True
        else:
            print("❌ Get user recommendations failed")
            return False
    
    def test_get_specific_recommendation(self):
        """Test getting specific recommendation."""
        self.print_header("Get Specific Recommendation")
        
        if not self.auth_token or not self.recommendation_id:
            print("❌ No auth token or recommendation ID available")
            return False
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.get(
            f"{self.base_url}/api/v1/strategy/recommendations/{self.recommendation_id}",
            headers=headers
        )
        self.print_response(response, "Get Specific Recommendation")
        
        if response.status_code == 200:
            print("✅ Get specific recommendation successful")
            return True
        else:
            print("❌ Get specific recommendation failed")
            return False
    
    def test_execute_strategy(self):
        """Test strategy execution."""
        self.print_header("Execute Strategy")
        
        if not self.auth_token or not self.recommendation_id:
            print("❌ No auth token or recommendation ID available")
            return False
        
        execution_request = {
            "recommendation_id": self.recommendation_id,
            "transaction_signature": "0xabcdef1234567890",
            "gas_fee": 25000
        }
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.post(
            f"{self.base_url}/api/v1/strategy/execute",
            json=execution_request,
            headers=headers
        )
        self.print_response(response, "Execute Strategy")
        
        if response.status_code == 200:
            print("✅ Strategy execution successful")
            return True
        else:
            print("❌ Strategy execution failed")
            return False
    
    def test_get_education_content(self):
        """Test getting education content."""
        self.print_header("Get Education Content")
        
        if not self.auth_token:
            print("❌ No auth token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.get(
            f"{self.base_url}/api/v1/education/liquidity_provision?level=beginner",
            headers=headers
        )
        self.print_response(response, "Get Education Content")
        
        if response.status_code == 200:
            print("✅ Get education content successful")
            return True
        else:
            print("❌ Get education content failed")
            return False
    
    def test_explain_concept(self):
        """Test concept explanation."""
        self.print_header("Explain Concept")
        
        if not self.auth_token:
            print("❌ No auth token available")
            return False
        
        education_request = {
            "topic": "yield_farming",
            "level": "intermediate",
            "context": "I want to learn about yield farming strategies"
        }
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.post(
            f"{self.base_url}/api/v1/education/explain",
            json=education_request,
            headers=headers
        )
        self.print_response(response, "Explain Concept")
        
        if response.status_code == 200:
            print("✅ Concept explanation successful")
            return True
        else:
            print("❌ Concept explanation failed")
            return False
    
    def test_list_education_topics(self):
        """Test listing education topics."""
        self.print_header("List Education Topics")
        
        if not self.auth_token:
            print("❌ No auth token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.session.get(
            f"{self.base_url}/api/v1/education/topics/list",
            headers=headers
        )
        self.print_response(response, "List Education Topics")
        
        if response.status_code == 200:
            print("✅ List education topics successful")
            return True
        else:
            print("❌ List education topics failed")
            return False
    
    def test_logout(self):
        """Test user logout."""
        self.print_header("User Logout")
        
        response = self.session.post(f"{self.base_url}/api/v1/auth/logout")
        self.print_response(response, "User Logout")
        
        if response.status_code == 200:
            print("✅ User logout successful")
            return True
        else:
            print("❌ User logout failed")
            return False
    
    def test_error_scenarios(self):
        """Test error scenarios."""
        self.print_header("Error Scenarios")
        
        # Test unauthorized access
        print("\n1. Testing unauthorized access:")
        response = self.session.get(f"{self.base_url}/api/v1/auth/me")
        self.print_response(response, "Unauthorized Access")
        
        # Test invalid endpoint
        print("\n2. Testing invalid endpoint:")
        response = self.session.get(f"{self.base_url}/api/v1/invalid-endpoint")
        self.print_response(response, "Invalid Endpoint")
        
        # Test invalid JSON
        print("\n3. Testing invalid JSON:")
        response = self.session.post(
            f"{self.base_url}/api/v1/auth/signup",
            data="invalid json"
        )
        self.print_response(response, "Invalid JSON")
        
        print("✅ Error scenarios tested")
        return True
    
    def run_full_demo(self):
        """Run the complete API demo."""
        print("🚀 Starting Satoshi Sensei API Demo")
        print(f"Base URL: {self.base_url}")
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Root Endpoint", self.test_root_endpoint),
            ("User Signup", self.test_user_signup),
            ("User Login", self.test_user_login),
            ("Get Current User", self.test_get_current_user),
            ("Connect Wallet", self.test_connect_wallet),
            ("Get User Wallets", self.test_get_user_wallets),
            ("Get Wallet Balances", self.test_get_wallet_balances),
            ("Get Strategy Recommendation", self.test_get_strategy_recommendation),
            ("Get User Recommendations", self.test_get_user_recommendations),
            ("Get Specific Recommendation", self.test_get_specific_recommendation),
            ("Execute Strategy", self.test_execute_strategy),
            ("Get Education Content", self.test_get_education_content),
            ("Explain Concept", self.test_explain_concept),
            ("List Education Topics", self.test_list_education_topics),
            ("User Logout", self.test_logout),
            ("Error Scenarios", self.test_error_scenarios),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            try:
                print(f"\n⏳ Running: {test_name}")
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ {test_name} failed with exception: {e}")
                failed += 1
            
            # Small delay between tests
            time.sleep(0.5)
        
        # Summary
        self.print_header("Demo Summary")
        print(f"✅ Tests Passed: {passed}")
        print(f"❌ Tests Failed: {failed}")
        print(f"📊 Total Tests: {passed + failed}")
        print(f"🎯 Success Rate: {(passed / (passed + failed) * 100):.1f}%")
        
        if failed == 0:
            print("\n🎉 All tests passed! API is working correctly.")
        else:
            print(f"\n⚠️  {failed} tests failed. Check the output above for details.")
        
        return failed == 0


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Satoshi Sensei API Demo")
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL for the API (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--test",
        help="Run a specific test (e.g., 'health', 'auth', 'wallet', 'strategy', 'education')"
    )
    
    args = parser.parse_args()
    
    demo = SatoshiSenseiAPIDemo(args.url)
    
    if args.test:
        # Run specific test
        test_map = {
            "health": demo.test_health_check,
            "auth": [demo.test_user_signup, demo.test_user_login, demo.test_get_current_user],
            "wallet": [demo.test_connect_wallet, demo.test_get_user_wallets, demo.test_get_wallet_balances],
            "strategy": [demo.test_get_strategy_recommendation, demo.test_get_user_recommendations],
            "education": [demo.test_get_education_content, demo.test_explain_concept, demo.test_list_education_topics]
        }
        
        if args.test in test_map:
            tests = test_map[args.test]
            if isinstance(tests, list):
                for test in tests:
                    test()
            else:
                tests()
        else:
            print(f"Unknown test: {args.test}")
            print(f"Available tests: {', '.join(test_map.keys())}")
            sys.exit(1)
    else:
        # Run full demo
        success = demo.run_full_demo()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
