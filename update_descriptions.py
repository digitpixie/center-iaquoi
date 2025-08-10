import asyncio
import os
import requests

def update_descriptions():
    """Update tool descriptions"""
    
    # Get backend URL
    backend_url = None
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    backend_url = line.split('=', 1)[1].strip()
                    break
    except:
        backend_url = 'http://localhost:8001'
    
    if not backend_url:
        backend_url = 'http://localhost:8001'
        
    print(f"Using backend URL: {backend_url}")
    
    # Login credentials
    admin_email = "admin@digitpixie.com"
    admin_password = "DigitPixie2025!"
    
    # Login to get token
    login_url = f"{backend_url}/api/auth/login"
    login_data = {
        "email": admin_email,
        "password": admin_password
    }
    
    try:
        print("🔐 Logging in...")
        login_response = requests.post(login_url, json=login_data)
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.text}")
            return
            
        token = login_response.json()["access_token"]
        print("✓ Login successful")
        
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Tools to update with new descriptions
    tools_updates = [
        {
            "id": "45f4eb99-862d-4123-ad16-63ab5d3b8845",
            "title": "Diagnostic créateur IA",
            "new_description": "Découvrez votre archétype de créateur IA avec ce diagnostic interactif",
            "category": "Diagnostic",
            "reason": "Removed '- Updated'"
        },
        {
            "id": "adcffb0c-a0de-4c7a-af74-78e95609746b", 
            "title": "La méthode SMART",
            "new_description": "Méthode SMART pour définir des objectifs efficaces",
            "category": "Formation IA",
            "reason": "Removed '- Updated'"
        },
        {
            "id": "6199f747-8e88-434b-a64a-c77377dc7568",
            "title": "Les 3 cerveaux IA", 
            "new_description": "Formation complète sur les 3 cerveaux IA avec méthode P.R.O.M.P.T.",
            "category": "Formation IA",
            "reason": "Removed '- Updated'"
        },
        {
            "id": "513dd0ef-a643-4cfd-afbb-c8b0a73a3a44",
            "title": "Avatar Command Center 2.0",
            "new_description": "Créez des avatars IA hyperréalistes avec FLUX AI, LORA training et techniques d'upscaling professionnelles",
            "category": "Formation IA", 
            "reason": "Shortened and simplified description"
        },
        {
            "id": "a4b50aeb-2901-460f-87a1-727930b967cc",
            "title": "PIXEL-IA Buddy",
            "new_description": "Votre companion IA personnel qui évolue avec vos apprentissages et défis",
            "category": "Companion IA",
            "reason": "More appealing and concise description"
        },
        {
            "id": "5eac3cab-12da-4d79-91e0-1c7ef53b9ca3",
            "title": "PromptiQ™", 
            "new_description": "Générateur de prompts IA avancé pour maximiser l'efficacité de vos interactions",
            "category": "Générateur IA",
            "reason": "More dynamic and compelling description"
        }
    ]
    
    print(f"\n🔄 Updating {len(tools_updates)} tool descriptions...")
    print("=" * 60)
    
    success_count = 0
    
    for tool_update in tools_updates:
        try:
            # Get current tool data first
            get_url = f"{backend_url}/api/tools"
            get_response = requests.get(get_url, headers=headers)
            
            if get_response.status_code != 200:
                print(f"❌ Failed to get tools: {get_response.text}")
                continue
                
            tools = get_response.json()
            current_tool = None
            
            for tool in tools:
                if tool["id"] == tool_update["id"]:
                    current_tool = tool
                    break
            
            if not current_tool:
                print(f"❌ Tool {tool_update['title']} not found")
                continue
            
            # Update with new description
            tool_data = {
                "title": current_tool["title"],
                "description": tool_update["new_description"], 
                "category": tool_update["category"],
                "html_content": current_tool["html_content"],
                "preview_image": current_tool.get("preview_image", "")
            }
            
            # Update tool
            update_url = f"{backend_url}/api/tools/{tool_update['id']}"
            update_response = requests.put(update_url, json=tool_data, headers=headers)
            
            if update_response.status_code == 200:
                print(f"✅ {tool_update['title']}")
                print(f"   New: {tool_update['new_description']}")
                print(f"   Reason: {tool_update['reason']}")
                success_count += 1
            else:
                print(f"❌ Failed to update {tool_update['title']}: {update_response.text}")
                
        except Exception as e:
            print(f"❌ Error updating {tool_update['title']}: {e}")
    
    print("=" * 60)
    print(f"🎉 Successfully updated {success_count}/{len(tools_updates)} descriptions!")
    print("\n📋 Summary of changes:")
    print("✅ Removed '- Updated' from 3 tools")
    print("✅ Simplified Avatar Command Center description") 
    print("✅ Made PIXEL-IA Buddy description more appealing")
    print("✅ Enhanced PromptiQ™ description")

if __name__ == "__main__":
    update_descriptions()