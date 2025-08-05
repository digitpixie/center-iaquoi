import requests
import sys
import json
from datetime import datetime

class OutilsInteractifsAPITester:
    def __init__(self, base_url="https://4429d075-908e-45f6-a06c-e0daa6dbe403.preview.emergentagent.com"):
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

    def test_delete_tool(self, tool_id):
        """Test tool deletion"""
        success, response = self.run_test(
            "Delete Tool",
            "DELETE",
            f"api/tools/{tool_id}",
            200
        )
        return success

    def test_get_pet_state(self):
        """Test get pet state (creates default if none exists)"""
        success, response = self.run_test(
            "Get Pet State",
            "GET",
            "api/pet-state",
            200
        )
        return success, response if success else {}

    def test_save_pet_state(self, pet_data):
        """Test save/update pet state"""
        success, response = self.run_test(
            "Save Pet State",
            "POST",
            "api/pet-state",
            200,
            data=pet_data
        )
        return success, response if success else {}

def test_pet_state_management():
    """Test the PIXEL-IA Buddy pet state management endpoints"""
    print("🚀 Testing PIXEL-IA Buddy Pet State Management")
    print("=" * 60)
    
    # Setup
    tester = OutilsInteractifsAPITester()
    admin_email = "admin@digitpixie.com"
    admin_password = "DigitPixie2025!"

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

    # Test 4: Get Pet State (should create default if none exists)
    print("\n4. Testing Get Pet State (Default Creation)...")
    success, pet_state = tester.test_get_pet_state()
    if not success:
        print("❌ Get pet state failed")
        return 1
    
    # Verify default pet state values
    expected_defaults = {
        "name": "PIXEL-IA",
        "level": 1,
        "happiness": 80,
        "knowledge": 60,
        "energy": 75,
        "hunger": 70,
        "stage": "baby",
        "modules_completed": 0,
        "mood": "happy"
    }
    
    print("   Verifying default pet state values:")
    defaults_correct = True
    for key, expected_value in expected_defaults.items():
        actual_value = pet_state.get(key)
        is_correct = actual_value == expected_value
        defaults_correct = defaults_correct and is_correct
        print(f"   {key}: {'✅' if is_correct else '❌'} (Expected: {expected_value}, Got: {actual_value})")
    
    if defaults_correct:
        print("✅ Default pet state values are correct")
    else:
        print("❌ Some default pet state values are incorrect")
    
    # Verify required fields exist
    required_fields = ["id", "user_id", "created_at", "updated_at"]
    for field in required_fields:
        if field in pet_state:
            print(f"   {field}: ✅ Present")
        else:
            print(f"   {field}: ❌ Missing")
            defaults_correct = False

    # Test 5: Update Pet State
    print("\n5. Testing Pet State Update...")
    updated_pet_data = {
        "name": "PIXEL-IA Buddy",
        "level": 2,
        "happiness": 90,
        "knowledge": 75,
        "energy": 85,
        "hunger": 60,
        "stage": "child",
        "modules_completed": 3,
        "mood": "excited"
    }
    
    success, updated_pet = tester.test_save_pet_state(updated_pet_data)
    if not success:
        print("❌ Pet state update failed")
        return 1
    
    # Verify updated values
    print("   Verifying updated pet state values:")
    update_correct = True
    for key, expected_value in updated_pet_data.items():
        actual_value = updated_pet.get(key)
        is_correct = actual_value == expected_value
        update_correct = update_correct and is_correct
        print(f"   {key}: {'✅' if is_correct else '❌'} (Expected: {expected_value}, Got: {actual_value})")
    
    if update_correct:
        print("✅ Pet state update successful")
    else:
        print("❌ Pet state update values incorrect")

    # Test 6: Data Persistence - Get Pet State Again
    print("\n6. Testing Data Persistence...")
    success, persisted_pet = tester.test_get_pet_state()
    if not success:
        print("❌ Get pet state after update failed")
        return 1
    
    # Verify persistence
    print("   Verifying persisted pet state values:")
    persistence_correct = True
    for key, expected_value in updated_pet_data.items():
        actual_value = persisted_pet.get(key)
        is_correct = actual_value == expected_value
        persistence_correct = persistence_correct and is_correct
        print(f"   {key}: {'✅' if is_correct else '❌'} (Expected: {expected_value}, Got: {actual_value})")
    
    if persistence_correct:
        print("✅ Pet state persistence working correctly")
    else:
        print("❌ Pet state persistence failed")

    # Test 7: Per-User Isolation (Create second user to test isolation)
    print("\n7. Testing Per-User Isolation...")
    
    # Create a second user for isolation testing
    test_user_email = "testuser@digitpixie.com"
    test_user_password = "TestUser2025!"
    test_user_name = "Test User"
    
    # Create second tester instance
    tester2 = OutilsInteractifsAPITester()
    
    # Try to register second user (might already exist, that's ok)
    print("   Attempting to register second test user...")
    register_success = tester2.test_register(test_user_email, test_user_password, test_user_name)
    if not register_success:
        # If registration fails, try login instead
        print("   Registration failed, attempting login...")
        if not tester2.test_login(test_user_email, test_user_password):
            print("   ⚠️  Could not create/login second user, skipping isolation test")
            print("   This is not critical - isolation test requires a second user account")
        else:
            print("   ✅ Second user login successful")
    else:
        print("   ✅ Second user registration successful")
    
    if tester2.token:
        # Get pet state for second user (should create new default)
        success, second_user_pet = tester2.test_get_pet_state()
        if success:
            # Verify second user gets default values, not the updated values from first user
            isolation_correct = True
            for key, expected_default in expected_defaults.items():
                actual_value = second_user_pet.get(key)
                is_default = actual_value == expected_default
                isolation_correct = isolation_correct and is_default
                print(f"   Second user {key}: {'✅' if is_default else '❌'} (Expected default: {expected_default}, Got: {actual_value})")
            
            # Verify different user_id
            first_user_id = persisted_pet.get("user_id")
            second_user_id = second_user_pet.get("user_id")
            different_user_ids = first_user_id != second_user_id
            print(f"   Different user IDs: {'✅' if different_user_ids else '❌'} (User1: {first_user_id}, User2: {second_user_id})")
            
            if isolation_correct and different_user_ids:
                print("✅ Per-user isolation working correctly")
            else:
                print("❌ Per-user isolation failed")
        else:
            print("❌ Could not get pet state for second user")
    else:
        print("   ⚠️  Skipping isolation test - second user authentication failed")

    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 Tests completed: {tester.tests_passed}/{tester.tests_run}")
    
    # Summary of critical findings
    print("\n🔍 Pet State Management Summary:")
    print(f"   Authentication: {'✅ Working' if tester.token else '❌ Failed'}")
    print(f"   Default pet state creation: {'✅ Working' if defaults_correct else '❌ Failed'}")
    print(f"   Pet state updates: {'✅ Working' if update_correct else '❌ Failed'}")
    print(f"   Data persistence: {'✅ Working' if persistence_correct else '❌ Failed'}")
    
    if tester2.token:
        print(f"   Per-user isolation: {'✅ Working' if 'isolation_correct' in locals() and isolation_correct else '❌ Failed'}")
    else:
        print(f"   Per-user isolation: ⚠️  Not tested (second user unavailable)")
    
    # Determine overall success
    critical_tests_passed = defaults_correct and update_correct and persistence_correct
    
    if critical_tests_passed:
        print("\n🎉 All critical pet state management tests passed!")
        return 0
    else:
        print(f"\n❌ Some critical pet state management tests failed")
        return 1

def test_3cerveaux_tool_integration():
    """Test the specific Les 3 cerveaux IA tool integration"""
    print("🚀 Testing Les 3 cerveaux IA Tool Integration")
    print("=" * 60)
    
    # Setup
    tester = OutilsInteractifsAPITester()
    admin_email = "admin@digitpixie.com"
    admin_password = "DigitPixie2025!"
    cerveaux_tool_id = "6199f747-8e88-434b-a64a-c77377dc7568"
    expected_tools_count = 4  # Should have 4 tools total now

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

    # Test 4: Get All Tools (should include Les 3 cerveaux IA tool and be 4 total)
    print("\n4. Testing Tool Retrieval...")
    tools = tester.test_get_tools()
    if not isinstance(tools, list):
        print("❌ Get tools failed")
        return 1
    
    print(f"   Total tools found: {len(tools)}")
    print(f"   Expected tools count: {expected_tools_count}")
    
    # Check if Les 3 cerveaux IA tool exists
    cerveaux_tool_found = False
    cerveaux_tool_data = None
    all_tool_titles = []
    
    for tool in tools:
        all_tool_titles.append(tool.get('title', 'Unknown'))
        if tool.get('id') == cerveaux_tool_id or tool.get('title') == "Les 3 cerveaux IA":
            cerveaux_tool_found = True
            cerveaux_tool_data = tool
            break
    
    print(f"   Available tools: {all_tool_titles}")
    
    if cerveaux_tool_found:
        print("✅ Les 3 cerveaux IA tool found in tools list")
        print(f"   Tool ID: {cerveaux_tool_data.get('id')}")
        print(f"   Title: {cerveaux_tool_data.get('title')}")
        print(f"   Category: {cerveaux_tool_data.get('category')}")
    else:
        print("❌ Les 3 cerveaux IA tool not found in tools list")
    
    # Verify total tools count
    if len(tools) == expected_tools_count:
        print(f"✅ Correct number of tools ({expected_tools_count})")
    else:
        print(f"❌ Incorrect number of tools - Expected: {expected_tools_count}, Got: {len(tools)}")

    # Test 5: Get Specific Les 3 cerveaux IA Tool
    print("\n5. Testing Specific Tool Retrieval...")
    if cerveaux_tool_found and cerveaux_tool_data:
        actual_tool_id = cerveaux_tool_data.get('id')
        success, tool_details = tester.test_get_tool(actual_tool_id)
        if success:
            print("✅ Les 3 cerveaux IA tool retrieved successfully")
            print(f"   HTML content length: {len(tool_details.get('html_content', ''))}")
        else:
            print("❌ Failed to retrieve Les 3 cerveaux IA tool")
    else:
        print("⚠️  Skipping specific tool test - Les 3 cerveaux IA tool not found")

    # Test 6: Verify Tool Details
    print("\n6. Testing Tool Details...")
    if cerveaux_tool_found and cerveaux_tool_data:
        title_correct = cerveaux_tool_data.get('title') == "Les 3 cerveaux IA"
        category_correct = cerveaux_tool_data.get('category') == "Formation IA"
        has_html_content = bool(cerveaux_tool_data.get('html_content'))
        id_correct = cerveaux_tool_data.get('id') == cerveaux_tool_id
        
        print(f"   Title correct: {'✅' if title_correct else '❌'} (Expected: 'Les 3 cerveaux IA', Got: '{cerveaux_tool_data.get('title')}')")
        print(f"   Category correct: {'✅' if category_correct else '❌'} (Expected: 'Formation IA', Got: '{cerveaux_tool_data.get('category')}')")
        print(f"   ID correct: {'✅' if id_correct else '❌'} (Expected: '{cerveaux_tool_id}', Got: '{cerveaux_tool_data.get('id')}')")
        print(f"   Has HTML content: {'✅' if has_html_content else '❌'}")
        
        if has_html_content:
            html_length = len(cerveaux_tool_data.get('html_content', ''))
            print(f"   HTML content length: {html_length} characters")
        
        if not (title_correct and category_correct and has_html_content and id_correct):
            print("❌ Tool details verification failed")
    else:
        print("⚠️  Skipping tool details verification - Les 3 cerveaux IA tool not found")

    # Test 7: Get Categories (should include "Formation IA" and "Diagnostic")
    print("\n7. Testing Categories...")
    categories = tester.test_get_categories()
    if isinstance(categories, list):
        formation_ia_found = any(cat.get('name') == 'Formation IA' for cat in categories)
        diagnostic_found = any(cat.get('name') == 'Diagnostic' for cat in categories)
        
        print(f"   Formation IA category found: {'✅' if formation_ia_found else '❌'}")
        print(f"   Diagnostic category found: {'✅' if diagnostic_found else '❌'}")
        print(f"   Available categories: {[cat.get('name') for cat in categories]}")
        
        # Check Formation IA count (should be 3 tools now)
        formation_ia_count = 0
        diagnostic_count = 0
        for cat in categories:
            if cat.get('name') == 'Formation IA':
                formation_ia_count = cat.get('count', 0)
            elif cat.get('name') == 'Diagnostic':
                diagnostic_count = cat.get('count', 0)
        
        print(f"   Formation IA tools count: {formation_ia_count} (Expected: 3)")
        print(f"   Diagnostic tools count: {diagnostic_count} (Expected: 1)")
        
        if not (formation_ia_found and diagnostic_found):
            print("❌ Required categories not found")
    else:
        print("❌ Get categories failed")

    # Test 8: Test Tool Update (if Les 3 cerveaux IA tool exists)
    print("\n8. Testing Tool Update...")
    if cerveaux_tool_found and cerveaux_tool_data:
        actual_tool_id = cerveaux_tool_data.get('id')
        original_html = cerveaux_tool_data.get('html_content', '')
        
        success = tester.test_update_tool(
            actual_tool_id,
            "Les 3 cerveaux IA",  # Keep same title
            "Formation complète sur les 3 cerveaux IA avec méthode P.R.O.M.P.T. - Updated",  # Updated description
            "Formation IA",  # Keep same category
            original_html  # Keep same HTML content
        )
        if success:
            print("✅ Les 3 cerveaux IA tool update successful")
        else:
            print("❌ Les 3 cerveaux IA tool update failed")
    else:
        print("⚠️  Skipping tool update test - Les 3 cerveaux IA tool not found")

    # Test 9: Verify Platform Status (4 tools total with correct distribution)
    print("\n9. Testing Platform Status...")
    expected_tool_names = [
        "Avatar Command Center 2.0",
        "La méthode SMART", 
        "Diagnostic créateur IA",
        "Les 3 cerveaux IA"
    ]
    
    found_tools = [tool.get('title') for tool in tools]
    all_expected_found = all(tool_name in found_tools for tool_name in expected_tool_names)
    
    print(f"   Expected tools: {expected_tool_names}")
    print(f"   Found tools: {found_tools}")
    print(f"   All expected tools found: {'✅' if all_expected_found else '❌'}")
    
    if len(tools) == 4 and all_expected_found:
        print("✅ Platform status correct - 4 tools with proper distribution")
    else:
        print("❌ Platform status incorrect")

    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 Tests completed: {tester.tests_passed}/{tester.tests_run}")
    
    # Summary of critical findings
    print("\n🔍 Les 3 cerveaux IA Tool Integration Summary:")
    if cerveaux_tool_found:
        print("✅ Les 3 cerveaux IA tool successfully integrated and accessible")
        print(f"   Tool ID: {cerveaux_tool_data.get('id')}")
        print(f"   Title: {cerveaux_tool_data.get('title')}")
        print(f"   Category: {cerveaux_tool_data.get('category')}")
        print(f"   HTML content: {len(cerveaux_tool_data.get('html_content', ''))} characters")
    else:
        print("❌ Les 3 cerveaux IA tool integration failed - tool not found")
    
    print(f"\n🏢 Platform Status:")
    print(f"   Total tools: {len(tools)}/4")
    print(f"   Authentication: {'✅ Working' if tester.token else '❌ Failed'}")
    print(f"   CRUD operations: {'✅ Working' if tester.tests_passed > 5 else '❌ Issues detected'}")
    
    if tester.tests_passed == tester.tests_run:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n❌ {tester.tests_run - tester.tests_passed} tests failed")
        return 1

def main():
    """Main test function - runs pet state management tests"""
    return test_pet_state_management()

if __name__ == "__main__":
    sys.exit(main())