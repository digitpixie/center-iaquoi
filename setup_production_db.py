"""
Configuration MongoDB pour la production
Utilise MongoDB Atlas (cloud) pour que l'app fonctionne en production
"""

import os

def setup_production_mongodb():
    """Setup MongoDB Atlas connection string"""
    
    # MongoDB Atlas connection string (cluster gratuit)
    # Cette URL sera accessible depuis n'importe où sur internet
    atlas_url = "mongodb+srv://admin:DigitPixie2025@cluster0.mongodb.net/ia_quoi?retryWrites=true&w=majority"
    
    # Pour le développement local, on garde localhost
    # Pour la production, on utilise Atlas
    
    print("🔧 Configuration MongoDB pour production:")
    print(f"Local: mongodb://localhost:27017")  
    print(f"Production: MongoDB Atlas Cloud")
    print()
    print("⚠️  IMPORTANT: Créez un cluster MongoDB Atlas gratuit à:")
    print("   https://www.mongodb.com/cloud/atlas")
    print("   Username: admin")  
    print("   Password: DigitPixie2025")
    print("   Database: ia_quoi")
    print()
    print("Puis remplacez l'URL dans backend/.env.production")

if __name__ == "__main__":
    setup_production_mongodb()