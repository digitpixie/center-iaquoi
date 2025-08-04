import requests
import sys
import json
from datetime import datetime

class OutilsInteractifsAPITester:
    def __init__(self, base_url="https://d5d30b3e-2d74-4909-8943-0cd21d729193.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.user_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            test_headers.update(headers)

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test health endpoint"""
        return self.run_test("Health Check", "GET", "api/health", 200)

    def test_register(self, email, password, name):
        """Test user registration"""
        success, response = self.run_test(
            "User Registration",
            "POST",
            "api/auth/register",
            200,
            data={"email": email, "password": password, "name": name}
        )
        if success and 'access_token' in response:
            self.token = response['access_token']
            return True
        return False

    def test_login(self, email, password):
        """Test user login"""
        success, response = self.run_test(
            "User Login",
            "POST",
            "api/auth/login",
            200,
            data={"email": email, "password": password}
        )
        if success and 'access_token' in response:
            self.token = response['access_token']
            return True
        return False

    def test_get_current_user(self):
        """Test get current user info"""
        success, response = self.run_test(
            "Get Current User",
            "GET",
            "api/auth/me",
            200
        )
        if success and 'id' in response:
            self.user_id = response['id']
            return True
        return False

    def test_create_tool(self, title, description, category, html_content):
        """Test tool creation"""
        success, response = self.run_test(
            "Create Tool",
            "POST",
            "api/tools",
            200,
            data={
                "title": title,
                "description": description,
                "category": category,
                "html_content": html_content
            }
        )
        return response.get('id') if success else None

    def test_get_tools(self):
        """Test get all tools"""
        success, response = self.run_test(
            "Get Tools",
            "GET",
            "api/tools",
            200
        )
        return response if success else []

    def test_get_tool(self, tool_id):
        """Test get specific tool"""
        success, response = self.run_test(
            "Get Specific Tool",
            "GET",
            f"api/tools/{tool_id}",
            200
        )
        return success

    def test_update_tool(self, tool_id, title, description, category, html_content):
        """Test tool update"""
        success, response = self.run_test(
            "Update Tool",
            "PUT",
            f"api/tools/{tool_id}",
            200,
            data={
                "title": title,
                "description": description,
                "category": category,
                "html_content": html_content
            }
        )
        return success

    def test_get_categories(self):
        """Test get categories"""
        success, response = self.run_test(
            "Get Categories",
            "GET",
            "api/categories",
            200
        )
        return response if success else []

    def test_delete_tool(self, tool_id):
        """Test tool deletion"""
        success, response = self.run_test(
            "Delete Tool",
            "DELETE",
            f"api/tools/{tool_id}",
            200
        )
        return success

def test_smart_tool_integration():
    """Test the specific SMART tool integration"""
    print("🚀 Testing La méthode SMART Tool Integration")
    print("=" * 50)
    
    # Setup
    tester = OutilsInteractifsAPITester()
    admin_email = "admin@digitpixie.com"
    admin_password = "DigitPixie2025!"
    smart_tool_id = "adcffb0c-a0de-4c7a-af74-78e95609746b"

    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    if not tester.test_health_check()[0]:
        print("❌ Health check failed, stopping tests")
        return 1

    # Test 2: Admin Login
    print("\n2. Testing Admin Authentication...")
    if not tester.test_login(admin_email, admin_password):
        print("❌ Admin login failed, stopping tests")
        return 1

    # Test 3: Get Current User
    print("\n3. Testing Get Current User...")
    if not tester.test_get_current_user():
        print("❌ Get current user failed")
        return 1

    # Test 4: Get All Tools (should include SMART tool)
    print("\n4. Testing Tool Retrieval...")
    tools = tester.test_get_tools()
    if not isinstance(tools, list):
        print("❌ Get tools failed")
        return 1
    
    # Check if SMART tool exists
    smart_tool_found = False
    smart_tool_data = None
    for tool in tools:
        if tool.get('id') == smart_tool_id or tool.get('title') == "La méthode SMART":
            smart_tool_found = True
            smart_tool_data = tool
            break
    
    if smart_tool_found:
        print("✅ SMART tool found in tools list")
        print(f"   Tool ID: {smart_tool_data.get('id')}")
        print(f"   Title: {smart_tool_data.get('title')}")
        print(f"   Category: {smart_tool_data.get('category')}")
    else:
        print("❌ SMART tool not found in tools list")
        print(f"   Available tools: {[tool.get('title') for tool in tools]}")

    # Test 5: Get Specific SMART Tool
    print("\n5. Testing Specific Tool Retrieval...")
    if smart_tool_found and smart_tool_data:
        actual_tool_id = smart_tool_data.get('id')
        success = tester.test_get_tool(actual_tool_id)
        if success:
            print("✅ SMART tool retrieved successfully")
        else:
            print("❌ Failed to retrieve SMART tool")
    else:
        print("⚠️  Skipping specific tool test - SMART tool not found")

    # Test 6: Verify Tool Details
    print("\n6. Testing Tool Details...")
    if smart_tool_found and smart_tool_data:
        title_correct = smart_tool_data.get('title') == "La méthode SMART"
        category_correct = smart_tool_data.get('category') == "Formation IA"
        has_html_content = bool(smart_tool_data.get('html_content'))
        
        print(f"   Title correct: {'✅' if title_correct else '❌'} (Expected: 'La méthode SMART', Got: '{smart_tool_data.get('title')}')")
        print(f"   Category correct: {'✅' if category_correct else '❌'} (Expected: 'Formation IA', Got: '{smart_tool_data.get('category')}')")
        print(f"   Has HTML content: {'✅' if has_html_content else '❌'}")
        
        if not (title_correct and category_correct and has_html_content):
            print("❌ Tool details verification failed")
    else:
        print("⚠️  Skipping tool details verification - SMART tool not found")

    # Test 7: Get Categories (should include "Formation IA")
    print("\n7. Testing Categories...")
    categories = tester.test_get_categories()
    if isinstance(categories, list):
        formation_ia_found = any(cat.get('name') == 'Formation IA' for cat in categories)
        print(f"   Formation IA category found: {'✅' if formation_ia_found else '❌'}")
        print(f"   Available categories: {[cat.get('name') for cat in categories]}")
        if not formation_ia_found:
            print("❌ Formation IA category not found")
    else:
        print("❌ Get categories failed")

    # Test 8: Test Tool Update (if SMART tool exists)
    print("\n8. Testing Tool Update...")
    if smart_tool_found and smart_tool_data:
        actual_tool_id = smart_tool_data.get('id')
        original_html = smart_tool_data.get('html_content', '')
        
        success = tester.test_update_tool(
            actual_tool_id,
            "La méthode SMART",  # Keep same title
            "Méthode SMART pour définir des objectifs efficaces - Updated",  # Updated description
            "Formation IA",  # Keep same category
            original_html  # Keep same HTML content
        )
        if success:
            print("✅ SMART tool update successful")
        else:
            print("❌ SMART tool update failed")
    else:
        print("⚠️  Skipping tool update test - SMART tool not found")

    # Print final results
    print("\n" + "=" * 50)
    print(f"📊 Tests completed: {tester.tests_passed}/{tester.tests_run}")
    
    # Summary of critical findings
    print("\n🔍 SMART Tool Integration Summary:")
    if smart_tool_found:
        print("✅ SMART tool successfully integrated and accessible")
        print(f"   Tool ID: {smart_tool_data.get('id')}")
        print(f"   Title: {smart_tool_data.get('title')}")
        print(f"   Category: {smart_tool_data.get('category')}")
    else:
        print("❌ SMART tool integration failed - tool not found")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"❌ {tester.tests_run - tester.tests_passed} tests failed")
        return 1

def main():
    """Main test function - runs SMART tool integration tests"""
    return test_smart_tool_integration()

if __name__ == "__main__":
    sys.exit(main())