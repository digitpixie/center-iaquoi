import asyncio
import os
import requests

def update_promptiq_header():
    """Update PromptiQ tool to remove header title"""
    
    # Get backend URL from environment
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
    
    # PromptiQ HTML content WITHOUT header title
    promptiq_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PromptiQ™</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            overflow: hidden;
        }
        
        .container {
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        
        .iframe-container {
            flex: 1;
            position: relative;
            background: white;
        }
        
        iframe {
            width: 100%;
            height: 100%;
            border: none;
            background: white;
        }
        
        .loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #666;
            font-size: 18px;
            z-index: 1;
        }
        
        .error-message {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: #666;
            z-index: 2;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            max-width: 400px;
        }
        
        .error-message h3 {
            color: #e74c3c;
            margin-bottom: 15px;
        }
        
        .external-link {
            display: inline-block;
            margin-top: 15px;
            padding: 10px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .external-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="iframe-container">
            <div class="loading" id="loading">Chargement de PromptiQ™...</div>
            <div class="error-message" id="errorMessage" style="display: none;">
                <h3>🔒 Accès iframe restreint</h3>
                <p>PromptiQ™ ne peut pas être affiché dans cette iframe pour des raisons de sécurité.</p>
                <a href="https://www.digitpixie.fr" target="_blank" class="external-link">
                    🌐 Ouvrir PromptiQ™ dans un nouvel onglet
                </a>
            </div>
            <iframe 
                id="promptiqFrame"
                src="https://www.digitpixie.fr"
                title="PromptiQ™ - Générateur de prompts IA"
                loading="lazy">
            </iframe>
        </div>
    </div>
    
    <script>
        const iframe = document.getElementById('promptiqFrame');
        const loading = document.getElementById('loading');
        const errorMessage = document.getElementById('errorMessage');
        
        let loadTimeout;
        
        // Hide loading after iframe loads
        iframe.onload = function() {
            loading.style.display = 'none';
            clearTimeout(loadTimeout);
        };
        
        // Handle iframe load errors
        iframe.onerror = function() {
            loading.style.display = 'none';
            errorMessage.style.display = 'block';
            clearTimeout(loadTimeout);
        };
        
        // Timeout fallback (if site blocks iframe)
        loadTimeout = setTimeout(function() {
            // Check if iframe loaded successfully
            try {
                // This will throw an error if the iframe is blocked
                iframe.contentDocument;
                loading.style.display = 'none';
            } catch (e) {
                loading.style.display = 'none';
                errorMessage.style.display = 'block';
            }
        }, 10000); // 10 second timeout
        
        // Additional check for X-Frame-Options blocking
        window.addEventListener('message', function(event) {
            if (event.data === 'iframe-blocked') {
                loading.style.display = 'none';
                errorMessage.style.display = 'block';
            }
        });
    </script>
</body>
</html>"""
    
    # Tool data for update
    tool_data = {
        "title": "PromptiQ™",
        "description": "Générateur de prompts IA professionnel pour optimiser vos interactions avec l'intelligence artificielle",
        "category": "Générateur IA",
        "html_content": promptiq_html,
        "preview_image": ""
    }
    
    # Update tool - we need to use the tool ID
    tool_id = "5eac3cab-12da-4d79-91e0-1c7ef53b9ca3"
    update_url = f"{backend_url}/api/tools/{tool_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        print("🔄 Updating PromptiQ™ header...")
        update_response = requests.put(update_url, json=tool_data, headers=headers)
        
        if update_response.status_code == 200:
            tool_info = update_response.json()
            print(f"✅ PromptiQ™ header updated successfully!")
            print(f"   Tool ID: {tool_info['id']}")
            print(f"   Title: {tool_info['title']}")
            print(f"   Updated at: {tool_info['updated_at']}")
            print()
            print("🎯 PromptiQ™ now displays without the header title!")
            print("   The iframe loads directly without the decorative header.")
            
        else:
            print(f"❌ Failed to update tool: {update_response.text}")
            
    except Exception as e:
        print(f"❌ Update tool error: {e}")

if __name__ == "__main__":
    update_promptiq_header()