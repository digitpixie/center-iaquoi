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

def main():
    print("🚀 Starting Outils Interactifs API Tests")
    print("=" * 50)
    
    # Setup
    tester = OutilsInteractifsAPITester()
    test_timestamp = datetime.now().strftime('%H%M%S')
    test_email = f"test_{test_timestamp}@example.com"
    test_password = "testpass123"
    test_name = "Test User"

    # Test 1: Health Check
    if not tester.test_health_check()[0]:
        print("❌ Health check failed, stopping tests")
        return 1

    # Test 2: User Registration
    if not tester.test_register(test_email, test_password, test_name):
        print("❌ Registration failed, stopping tests")
        return 1

    # Test 3: Get Current User
    if not tester.test_get_current_user():
        print("❌ Get current user failed")
        return 1

    # Test 4: Create Tool
    calculator_html = """<!DOCTYPE html><html><head><title>Calculateur</title></head><body><h2>Calculateur Simple</h2><input type='number' id='a' placeholder='Nombre 1'><input type='number' id='b' placeholder='Nombre 2'><button onclick='calculate()'>Calculer</button><p id='result'></p><script>function calculate(){const a=document.getElementById('a').value;const b=document.getElementById('b').value;document.getElementById('result').innerHTML='Résultat: '+(parseFloat(a)+parseFloat(b));}</script></body></html>"""
    
    tool_id = tester.test_create_tool(
        "Calculateur Simple",
        "Un calculateur HTML simple pour tester",
        "Calculateur",
        calculator_html
    )
    if not tool_id:
        print("❌ Tool creation failed")
        return 1

    # Test 5: Get Tools
    tools = tester.test_get_tools()
    if not tools:
        print("❌ Get tools failed")
        return 1

    # Test 6: Get Specific Tool
    if not tester.test_get_tool(tool_id):
        print("❌ Get specific tool failed")
        return 1

    # Test 7: Get Categories
    categories = tester.test_get_categories()
    if not isinstance(categories, list):
        print("❌ Get categories failed")
        return 1

    # Test 8: Update Tool
    if not tester.test_update_tool(
        tool_id,
        "Calculateur Simple Modifié",
        "Un calculateur HTML simple modifié",
        "Calculateur",
        calculator_html
    ):
        print("❌ Tool update failed")
        return 1

    # Test 9: Delete Tool
    if not tester.test_delete_tool(tool_id):
        print("❌ Tool deletion failed")
        return 1

    # Test 10: Test Login with existing user
    # Reset token to test login
    tester.token = None
    if not tester.test_login(test_email, test_password):
        print("❌ Login failed")
        return 1

    # Print final results
    print("\n" + "=" * 50)
    print(f"📊 Tests completed: {tester.tests_passed}/{tester.tests_run}")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"❌ {tester.tests_run - tester.tests_passed} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())