import asyncio
import os
import sys
import uuid
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient

# Add the backend directory to the path to import from server.py
sys.path.append('/app/backend')

# Database connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')

async def create_default_modules():
    """Create default Skool modules for testing"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.outils_interactifs
    skool_modules_collection = db.skool_modules
    
    # Clear existing modules (for clean start)
    await skool_modules_collection.delete_many({})
    
    # Default modules to create
    modules = [
        {
            "title": "Module 1: Introduction à l'IA",
            "description": "Découvrez les bases de l'intelligence artificielle et ses applications dans le monde moderne.",
            "skool_module_id": "intro-ai-001",
            "completion_code": "START-AI",
            "reward_points": 30,
            "required_for_evolution": True
        },
        {
            "title": "Module 2: ChatGPT Fundamentals",
            "description": "Maîtrisez les techniques de prompting avec ChatGPT pour optimiser vos interactions.",
            "skool_module_id": "chatgpt-101",
            "completion_code": "CHAT-MASTER",
            "reward_points": 30,
            "required_for_evolution": True
        },
        {
            "title": "Module 3: Claude AI Mastery",
            "description": "Explorez les capacités avancées de Claude AI et ses applications spécialisées.",
            "skool_module_id": "claude-advanced",
            "completion_code": "CLAUDE-PRO",
            "reward_points": 30,
            "required_for_evolution": True
        },
        {
            "title": "Module 4: Création de Contenu IA",
            "description": "Apprenez à créer du contenu engageant avec l'aide de l'intelligence artificielle.",
            "skool_module_id": "content-creation",
            "completion_code": "CREATE-AI",
            "reward_points": 30,
            "required_for_evolution": True
        },
        {
            "title": "Module 5: Automatisation IA",
            "description": "Automatisez vos tâches répétitives grâce aux outils d'IA et aux workflows intelligents.",
            "skool_module_id": "ai-automation",
            "completion_code": "AUTO-AI",
            "reward_points": 30,
            "required_for_evolution": True
        },
        {
            "title": "Module 6: IA Créative Avancée",
            "description": "Explorez les frontières de la créativité avec les outils d'IA générative les plus avancés.",
            "skool_module_id": "creative-ai",
            "completion_code": "CREATE-MASTER",
            "reward_points": 30,
            "required_for_evolution": True
        }
    ]
    
    # Insert modules into database
    created_modules = []
    for module_data in modules:
        module_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        
        module_doc = {
            "id": module_id,
            "title": module_data["title"],
            "description": module_data["description"],
            "skool_module_id": module_data["skool_module_id"],
            "completion_code": module_data["completion_code"],
            "reward_points": module_data["reward_points"],
            "required_for_evolution": module_data["required_for_evolution"],
            "created_at": now,
            "updated_at": now
        }
        
        await skool_modules_collection.insert_one(module_doc)
        created_modules.append(module_doc)
        print(f"✓ Created module: {module_data['title']}")
    
    print(f"\n🎉 Successfully created {len(created_modules)} Skool modules!")
    
    # Print summary
    print("\n📚 Available modules:")
    for module in created_modules:
        print(f"  - {module['title']}")
        print(f"    Code: {module['completion_code']}")
        print(f"    Reward: +{module['reward_points']} points")
        print()
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_default_modules())