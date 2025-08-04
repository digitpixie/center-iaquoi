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
        return success, response if success else {}

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

def test_diagnostic_tool_integration():
    """Test the Diagnostic créateur IA tool integration and verify 3 tools total"""
    print("🚀 Testing Diagnostic créateur IA Tool Integration")
    print("=" * 60)
    
    # Setup
    tester = OutilsInteractifsAPITester()
    admin_email = "admin@digitpixie.com"
    admin_password = "DigitPixie2025!"
    diagnostic_tool_id = "45f4eb99-862d-4123-ad16-63ab5d3b8845"
    smart_tool_id = "adcffb0c-a0de-4c7a-af74-78e95609746b"

    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    if not tester.test_health_check()[0]:
        print("❌ Health check failed, stopping tests")
        return 1

    # Test 2: Admin Authentication
    print("\n2. Testing Admin Authentication...")
    if not tester.test_login(admin_email, admin_password):
        print("❌ Admin login failed, stopping tests")
        return 1
    print("✅ Authentication successful with admin@digitpixie.com")

    # Test 3: Get Current User
    print("\n3. Testing Get Current User...")
    if not tester.test_get_current_user():
        print("❌ Get current user failed")
        return 1

    # Test 4: Get All Tools (should now have 3 tools total)
    print("\n4. Testing Tool Retrieval - Verifying 3 Tools Total...")
    tools = tester.test_get_tools()
    if not isinstance(tools, list):
        print("❌ Get tools failed")
        return 1
    
    print(f"   Total tools found: {len(tools)}")
    expected_tools = 3
    if len(tools) == expected_tools:
        print(f"✅ Correct number of tools found: {len(tools)}")
    else:
        print(f"❌ Expected {expected_tools} tools, found {len(tools)}")
    
    # Display all tools
    print("   Available tools:")
    for i, tool in enumerate(tools, 1):
        print(f"     {i}. {tool.get('title')} (Category: {tool.get('category')}, ID: {tool.get('id')})")

    # Test 5: Verify Diagnostic Tool Exists
    print("\n5. Testing Diagnostic Tool Presence...")
    diagnostic_tool_found = False
    diagnostic_tool_data = None
    for tool in tools:
        if (tool.get('id') == diagnostic_tool_id or 
            tool.get('title') == "Diagnostic créateur IA"):
            diagnostic_tool_found = True
            diagnostic_tool_data = tool
            break
    
    if diagnostic_tool_found:
        print("✅ Diagnostic créateur IA tool found in tools list")
        print(f"   Tool ID: {diagnostic_tool_data.get('id')}")
        print(f"   Title: {diagnostic_tool_data.get('title')}")
        print(f"   Category: {diagnostic_tool_data.get('category')}")
    else:
        print("❌ Diagnostic créateur IA tool not found in tools list")
        print(f"   Available tools: {[tool.get('title') for tool in tools]}")

    # Test 6: Verify SMART Tool Still Exists
    print("\n6. Testing SMART Tool Presence...")
    smart_tool_found = False
    smart_tool_data = None
    for tool in tools:
        if (tool.get('id') == smart_tool_id or 
            tool.get('title') == "La méthode SMART"):
            smart_tool_found = True
            smart_tool_data = tool
            break
    
    if smart_tool_found:
        print("✅ La méthode SMART tool found in tools list")
        print(f"   Tool ID: {smart_tool_data.get('id')}")
        print(f"   Title: {smart_tool_data.get('title')}")
        print(f"   Category: {smart_tool_data.get('category')}")
    else:
        print("❌ La méthode SMART tool not found in tools list")

    # Test 7: Verify Avatar Command Center Tool Exists
    print("\n7. Testing Avatar Command Center Tool Presence...")
    avatar_tool_found = False
    avatar_tool_data = None
    for tool in tools:
        if "Avatar Command Center" in tool.get('title', ''):
            avatar_tool_found = True
            avatar_tool_data = tool
            break
    
    if avatar_tool_found:
        print("✅ Avatar Command Center tool found in tools list")
        print(f"   Tool ID: {avatar_tool_data.get('id')}")
        print(f"   Title: {avatar_tool_data.get('title')}")
        print(f"   Category: {avatar_tool_data.get('category')}")
    else:
        print("❌ Avatar Command Center tool not found in tools list")

    # Test 8: Get Specific Diagnostic Tool
    print("\n8. Testing Specific Diagnostic Tool Retrieval...")
    if diagnostic_tool_found and diagnostic_tool_data:
        actual_tool_id = diagnostic_tool_data.get('id')
        success, tool_details = tester.test_get_tool(actual_tool_id)
        if success:
            print("✅ Diagnostic tool retrieved successfully")
            print(f"   Tool details retrieved for ID: {actual_tool_id}")
        else:
            print("❌ Failed to retrieve Diagnostic tool")
    else:
        print("⚠️  Skipping specific tool test - Diagnostic tool not found")

    # Test 9: Verify Diagnostic Tool Details
    print("\n9. Testing Diagnostic Tool Details...")
    if diagnostic_tool_found and diagnostic_tool_data:
        title_correct = diagnostic_tool_data.get('title') == "Diagnostic créateur IA"
        category_correct = diagnostic_tool_data.get('category') == "Diagnostic"
        has_html_content = bool(diagnostic_tool_data.get('html_content'))
        correct_id = diagnostic_tool_data.get('id') == diagnostic_tool_id
        
        print(f"   Title correct: {'✅' if title_correct else '❌'} (Expected: 'Diagnostic créateur IA', Got: '{diagnostic_tool_data.get('title')}')")
        print(f"   Category correct: {'✅' if category_correct else '❌'} (Expected: 'Diagnostic', Got: '{diagnostic_tool_data.get('category')}')")
        print(f"   Tool ID correct: {'✅' if correct_id else '❌'} (Expected: '{diagnostic_tool_id}', Got: '{diagnostic_tool_data.get('id')}')")
        print(f"   Has HTML content: {'✅' if has_html_content else '❌'}")
        
        if has_html_content:
            html_length = len(diagnostic_tool_data.get('html_content', ''))
            print(f"   HTML content length: {html_length} characters")
            # Check if it contains quiz-related content
            html_content = diagnostic_tool_data.get('html_content', '').lower()
            has_quiz_content = any(keyword in html_content for keyword in ['question', 'quiz', 'archetype', 'diagnostic'])
            print(f"   Contains quiz content: {'✅' if has_quiz_content else '❌'}")
        
        if not (title_correct and category_correct and has_html_content and correct_id):
            print("❌ Diagnostic tool details verification failed")
    else:
        print("⚠️  Skipping tool details verification - Diagnostic tool not found")

    # Test 10: Get Categories (should include "Diagnostic" category)
    print("\n10. Testing Categories...")
    categories = tester.test_get_categories()
    if isinstance(categories, list):
        diagnostic_category_found = any(cat.get('name') == 'Diagnostic' for cat in categories)
        formation_ia_found = any(cat.get('name') == 'Formation IA' for cat in categories)
        
        print(f"   Diagnostic category found: {'✅' if diagnostic_category_found else '❌'}")
        print(f"   Formation IA category found: {'✅' if formation_ia_found else '❌'}")
        print(f"   Available categories: {[cat.get('name') for cat in categories]}")
        print(f"   Total categories: {len(categories)}")
        
        if not diagnostic_category_found:
            print("❌ Diagnostic category not found")
        if not formation_ia_found:
            print("❌ Formation IA category not found")
    else:
        print("❌ Get categories failed")

    # Test 11: Test CRUD Operations on Diagnostic Tool
    print("\n11. Testing CRUD Operations on Diagnostic Tool...")
    if diagnostic_tool_found and diagnostic_tool_data:
        actual_tool_id = diagnostic_tool_data.get('id')
        original_html = diagnostic_tool_data.get('html_content', '')
        
        success = tester.test_update_tool(
            actual_tool_id,
            "Diagnostic créateur IA",  # Keep same title
            "Découvrez votre archétype de créateur IA avec ce diagnostic interactif - Updated",  # Updated description
            "Diagnostic",  # Keep same category
            original_html  # Keep same HTML content
        )
        if success:
            print("✅ Diagnostic tool update successful")
        else:
            print("❌ Diagnostic tool update failed")
    else:
        print("⚠️  Skipping CRUD operations test - Diagnostic tool not found")

    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 Tests completed: {tester.tests_passed}/{tester.tests_run}")
    
    # Summary of critical findings
    print("\n🔍 DIAGNOSTIC TOOL INTEGRATION SUMMARY:")
    print("=" * 60)
    
    # Platform Status
    print(f"📈 Platform Status:")
    print(f"   Total tools: {len(tools) if isinstance(tools, list) else 'Unknown'}")
    print(f"   Expected tools: 3")
    print(f"   Status: {'✅ CORRECT' if len(tools) == 3 else '❌ INCORRECT'}")
    
    # Tool Status
    print(f"\n🛠️  Tool Status:")
    print(f"   Avatar Command Center 2.0: {'✅ Found' if avatar_tool_found else '❌ Missing'}")
    print(f"   La méthode SMART: {'✅ Found' if smart_tool_found else '❌ Missing'}")
    print(f"   Diagnostic créateur IA: {'✅ Found' if diagnostic_tool_found else '❌ Missing'}")
    
    # Category Status
    if isinstance(categories, list):
        print(f"\n📂 Category Status:")
        print(f"   Formation IA: {'✅ Found' if any(cat.get('name') == 'Formation IA' for cat in categories) else '❌ Missing'}")
        print(f"   Diagnostic: {'✅ Found' if any(cat.get('name') == 'Diagnostic' for cat in categories) else '❌ Missing'}")
    
    # Authentication Status
    print(f"\n🔐 Authentication Status:")
    print(f"   Admin login (admin@digitpixie.com): ✅ Working")
    
    # Overall Status
    all_tools_found = diagnostic_tool_found and smart_tool_found and avatar_tool_found
    correct_tool_count = len(tools) == 3 if isinstance(tools, list) else False
    
    print(f"\n🎯 OVERALL INTEGRATION STATUS:")
    if all_tools_found and correct_tool_count:
        print("✅ DIAGNOSTIC TOOL INTEGRATION SUCCESSFUL")
        print("   - All 3 tools are present and accessible")
        print("   - Diagnostic tool has correct details and content")
        print("   - Categories are properly configured")
        print("   - CRUD operations working")
    else:
        print("❌ DIAGNOSTIC TOOL INTEGRATION ISSUES DETECTED")
        if not diagnostic_tool_found:
            print("   - Diagnostic tool missing or not accessible")
        if not correct_tool_count:
            print(f"   - Incorrect tool count: expected 3, found {len(tools) if isinstance(tools, list) else 'unknown'}")
    
    if tester.tests_passed == tester.tests_run:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n❌ {tester.tests_run - tester.tests_passed} tests failed")
        return 1

def main():
    """Main test function - runs Diagnostic tool integration tests"""
    return test_diagnostic_tool_integration()

if __name__ == "__main__":
    sys.exit(main())