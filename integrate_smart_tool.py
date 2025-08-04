#!/usr/bin/env python3
"""
Script to integrate the "La méthode SMART" tool into the platform
"""
import requests
import json
import os

# Read the HTML content for the SMART tool
SMART_TOOL_HTML = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Méthode SMART Complète - Formation IA Digit Pixie</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0a0a0a;
            color: #ffffff;
            min-height: 100vh;
            padding: 20px;
            background-image: 
                radial-gradient(circle at 20% 50%, rgba(255, 0, 255, 0.2) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(0, 255, 255, 0.2) 0%, transparent 50%);
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        
        .worksheet-header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .worksheet-header h1 {
            font-size: 2.5rem;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #ff00ff, #00ffff, #ff00ff);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradientShift 3s ease-in-out infinite;
        }
        
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .section {
            background: rgba(20, 20, 20, 0.95);
            border: 2px solid #ff00ff;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 
                0 0 30px rgba(255, 0, 255, 0.3),
                inset 0 0 20px rgba(255, 0, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .section-title {
            font-size: 1.8rem;
            margin-bottom: 25px;
            text-align: center;
            color: #00ffff;
            text-shadow: 0 0 10px #00ffff;
        }
        
        .smart-letter {
            background: rgba(30, 30, 30, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        
        .smart-letter:hover {
            border-color: #00ffff;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
        }
        
        .letter-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .letter-big {
            font-size: 2.5rem;
            font-weight: bold;
            color: #ff00ff;
            margin-right: 20px;
            text-shadow: 0 0 15px #ff00ff;
        }
        
        .letter-meaning {
            flex: 1;
        }
        
        .letter-meaning h3 {
            font-size: 1.3rem;
            color: #ffffff;
            margin-bottom: 5px;
        }
        
        .letter-meaning p {
            opacity: 0.8;
            font-size: 0.95rem;
        }
        
        .input-field {
            width: 100%;
            background: rgba(40, 40, 40, 0.9);
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 8px;
            padding: 12px 15px;
            color: white;
            font-size: 16px;
            font-family: inherit;
            transition: all 0.3s ease;
            margin-top: 10px;
        }
        
        .input-field:focus {
            outline: none;
            border-color: #ff00ff;
            box-shadow: 
                0 0 15px rgba(255, 0, 255, 0.3),
                inset 0 0 10px rgba(255, 0, 255, 0.1);
        }
        
        textarea.input-field {
            min-height: 100px;
            resize: vertical;
        }
        
        .example {
            background: rgba(0, 255, 255, 0.1);
            border-left: 3px solid #00ffff;
            padding: 10px 15px;
            margin: 10px 0;
            font-size: 0.9rem;
            font-style: italic;
            opacity: 0.9;
        }
        
        .template-section {
            background: rgba(255, 255, 0, 0.05);
            border: 2px solid rgba(255, 255, 0, 0.5);
            padding: 25px;
            border-radius: 15px;
            margin-top: 30px;
        }
        
        .template-box {
            background: rgba(40, 40, 40, 0.9);
            padding: 20px;
            border-radius: 10px;
            margin-top: 15px;
            font-size: 1.1rem;
            text-align: center;
        }
        
        .template-input {
            display: inline-block;
            min-width: 150px;
            border-bottom: 2px solid #ffff00;
            padding: 2px 5px;
            margin: 0 5px;
            background: transparent;
            color: #ffff00;
            font-weight: bold;
        }
        
        .goal-box {
            background: rgba(30, 30, 30, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
        }
        
        .goal-box h3 {
            font-size: 1.3rem;
            margin-bottom: 15px;
            color: #ffffff;
        }
        
        .actions-container {
            margin-top: 30px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .save-button {
            background: linear-gradient(45deg, #ff00ff, #00ffff);
            color: white;
            border: none;
            padding: 18px 40px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .save-button:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 10px 30px rgba(255, 0, 255, 0.4),
                0 5px 15px rgba(0, 255, 255, 0.3);
        }
        
        .secondary-actions {
            display: flex;
            gap: 15px;
            justify-content: center;
        }
        
        .secondary-button {
            background: none;
            border: 1px solid #00ffff;
            color: #00ffff;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
            flex: 1;
        }
        
        .secondary-button:hover {
            background: rgba(0, 255, 255, 0.1);
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
        }
        
        .success-message {
            display: none;
            background: rgba(0, 255, 0, 0.1);
            border: 1px solid #00ff00;
            padding: 20px;
            border-radius: 10px;
            margin-top: 25px;
            text-align: center;
            color: #00ff00;
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @media (max-width: 768px) {
            .section {
                padding: 20px;
            }
            
            .worksheet-header h1 {
                font-size: 2rem;
            }
            
            .letter-big {
                font-size: 2rem;
            }
            
            .secondary-actions {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="worksheet-header">
            <h1>🎯 Ta Méthode SMART Complète</h1>
            <p style="font-size: 1.2rem; opacity: 0.9;">Transforme tes rêves IA en objectifs concrets et atteignables</p>
        </div>

        <!-- Section 1: Décomposition SMART -->
        <div class="section">
            <h2 class="section-title">📝 Étape 1 : Comprendre Chaque Lettre</h2>
            
            <!-- S - Spécifique -->
            <div class="smart-letter">
                <div class="letter-header">
                    <div class="letter-big">S</div>
                    <div class="letter-meaning">
                        <h3>SPÉCIFIQUE</h3>
                        <p>Précis et détaillé, pas vague</p>
                    </div>
                </div>
                <div class="example">
                    ❌ "Être meilleur avec l'IA"<br>
                    ✅ "Créer mon avatar professionnel qui me ressemble avec Flux AI"
                </div>
                <input type="text" class="input-field" id="specific" 
                    placeholder="Mon objectif spécifique : Je veux...">
            </div>

            <!-- M - Mesurable -->
            <div class="smart-letter">
                <div class="letter-header">
                    <div class="letter-big">M</div>
                    <div class="letter-meaning">
                        <h3>MESURABLE</h3>
                        <p>Avec des chiffres concrets pour tracker</p>
                    </div>
                </div>
                <div class="example">
                    Comment mesurer : Nombre de contenus créés, temps gagné, argent économisé...<br>
                    ✅ "Générer 30 visuels d'avatar différents"
                </div>
                <input type="text" class="input-field" id="measurable" 
                    placeholder="Je mesurerai mon succès par...">
            </div>

            <!-- A - Atteignable -->
            <div class="smart-letter">
                <div class="letter-header">
                    <div class="letter-big">A</div>
                    <div class="letter-meaning">
                        <h3>ATTEIGNABLE</h3>
                        <p>Avec tes contraintes actuelles</p>
                    </div>
                </div>
                <div class="example">
                    Sois honnête sur : Ton niveau tech, ton temps dispo, ton budget<br>
                    ✅ "Avec 30 min par jour pendant 4 semaines"
                </div>
                <input type="text" class="input-field" id="achievable" 
                    placeholder="C'est atteignable car j'ai...">
            </div>

            <!-- R - Réaliste -->
            <div class="smart-letter">
                <div class="letter-header">
                    <div class="letter-big">R</div>
                    <div class="letter-meaning">
                        <h3>RÉALISTE (Pertinent)</h3>
                        <p>Aligné avec tes besoins réels</p>
                    </div>
                </div>
                <div class="example">
                    ❌ "Devenir viral en 1 semaine"<br>
                    ✅ "Doubler ma production de contenu visuel"
                </div>
                <input type="text" class="input-field" id="realistic" 
                    placeholder="C'est important pour moi car...">
            </div>

            <!-- T - Temporel -->
            <div class="smart-letter">
                <div class="letter-header">
                    <div class="letter-big">T</div>
                    <div class="letter-meaning">
                        <h3>TEMPOREL</h3>
                        <p>Avec une deadline claire</p>
                    </div>
                </div>
                <div class="example">
                    ✅ "D'ici le 15 mars" (pas "bientôt" ou "un jour")<br>
                    ✅ "En 6 semaines maximum"
                </div>
                <input type="text" class="input-field" id="temporal" 
                    placeholder="Ma deadline est...">
            </div>
        </div>

        <!-- Section 2: Template Magique -->
        <div class="section">
            <h2 class="section-title">✨ Étape 2 : Utilise le Template Magique</h2>
            
            <div class="template-section">
                <p style="text-align: center; margin-bottom: 20px; font-size: 1.1rem;">
                    Assemble tous les éléments dans cette phrase puissante :
                </p>
                
                <div class="template-box">
                    "D'ici <span class="template-input" contenteditable="true">[QUAND]</span>, 
                    je veux <span class="template-input" contenteditable="true">[QUOI PRÉCISÉMENT]</span> 
                    pour <span class="template-input" contenteditable="true">[POURQUOI]</span>, 
                    mesurable par <span class="template-input" contenteditable="true">[COMMENT]</span>"
                </div>
                
                <div class="example" style="margin-top: 20px;">
                    Exemple : "D'ici 6 semaines, je veux maîtriser la création d'avatars hyperréalistes 
                    pour économiser sur les shootings photo, mesurable par 20 visuels créés et 300€ économisés"
                </div>
            </div>
        </div>

        <!-- Section 3: Tes 3 Objectifs -->
        <div class="section">
            <h2 class="section-title">🚀 Étape 3 : Définis Tes 3 Objectifs Prioritaires</h2>
            
            <div class="goal-box">
                <h3>🔧 Objectif 1 : Compétence Technique</h3>
                <p style="opacity: 0.8; margin-bottom: 10px;">Quelle compétence IA veux-tu maîtriser ?</p>
                <textarea class="input-field" id="goal1" 
                    placeholder="D'ici [QUAND], je veux [maîtriser quelle technique IA] pour [RAISON], mesurable par [MÉTRIQUE]"></textarea>
            </div>
            
            <div class="goal-box">
                <h3>🎨 Objectif 2 : Production Créative</h3>
                <p style="opacity: 0.8; margin-bottom: 10px;">Quel contenu veux-tu produire ?</p>
                <textarea class="input-field" id="goal2" 
                    placeholder="D'ici [QUAND], je veux [créer quel type de contenu] pour [RAISON], mesurable par [MÉTRIQUE]"></textarea>
            </div>
            
            <div class="goal-box">
                <h3>💰 Objectif 3 : Impact Business</h3>
                <p style="opacity: 0.8; margin-bottom: 10px;">Quel résultat concret pour ton activité ?</p>
                <textarea class="input-field" id="goal3" 
                    placeholder="D'ici [QUAND], je veux [quel impact business] pour [RAISON], mesurable par [MÉTRIQUE]"></textarea>
            </div>
        </div>

        <!-- Actions -->
        <div class="actions-container">
            <button class="save-button" onclick="saveAll()">
                💾 Sauvegarder Ma Méthode SMART Complète
            </button>
            
            <div class="secondary-actions">
                <button class="secondary-button" onclick="downloadAll()">
                    📥 Télécharger mon plan
                </button>
                <button class="secondary-button" onclick="emailAll()">
                    📧 M'envoyer par email
                </button>
            </div>
        </div>
        
        <div class="success-message" id="successMessage">
            ✅ Méthode SMART sauvegardée avec succès !
            <br><small>Tu peux la retrouver à chaque connexion. Imprime-la aussi pour l'avoir sous les yeux !</small>
        </div>
    </div>

    <script>
        // Charger les données sauvegardées
        window.onload = function() {
            const saved = localStorage.getItem('digitpixie_smart_complete');
            if (saved) {
                const data = JSON.parse(saved);
                // Charger les lettres SMART
                document.getElementById('specific').value = data.specific || '';
                document.getElementById('measurable').value = data.measurable || '';
                document.getElementById('achievable').value = data.achievable || '';
                document.getElementById('realistic').value = data.realistic || '';
                document.getElementById('temporal').value = data.temporal || '';
                // Charger les objectifs
                document.getElementById('goal1').value = data.goal1 || '';
                document.getElementById('goal2').value = data.goal2 || '';
                document.getElementById('goal3').value = data.goal3 || '';
                // Charger le template
                const templateInputs = document.querySelectorAll('.template-input');
                if (data.template) {
                    templateInputs[0].textContent = data.template.when || '[QUAND]';
                    templateInputs[1].textContent = data.template.what || '[QUOI PRÉCISÉMENT]';
                    templateInputs[2].textContent = data.template.why || '[POURQUOI]';
                    templateInputs[3].textContent = data.template.how || '[COMMENT]';
                }
            }
        }

        function saveAll() {
            // Collecter toutes les données
            const templateInputs = document.querySelectorAll('.template-input');
            const data = {
                // Lettres SMART
                specific: document.getElementById('specific').value,
                measurable: document.getElementById('measurable').value,
                achievable: document.getElementById('achievable').value,
                realistic: document.getElementById('realistic').value,
                temporal: document.getElementById('temporal').value,
                // Template
                template: {
                    when: templateInputs[0].textContent,
                    what: templateInputs[1].textContent,
                    why: templateInputs[2].textContent,
                    how: templateInputs[3].textContent
                },
                // Objectifs
                goal1: document.getElementById('goal1').value,
                goal2: document.getElementById('goal2').value,
                goal3: document.getElementById('goal3').value,
                // Meta
                date: new Date().toLocaleDateString('fr-FR'),
                timestamp: new Date().getTime()
            };
            
            // Sauvegarder
            localStorage.setItem('digitpixie_smart_complete', JSON.stringify(data));
            
            // Afficher le message
            document.getElementById('successMessage').style.display = 'block';
            setTimeout(() => {
                document.getElementById('successMessage').style.display = 'none';
            }, 5000);
            
            // Analytics
            if (typeof gtag !== 'undefined') {
                gtag('event', 'smart_complete_saved', {
                    'event_category': 'engagement',
                    'event_label': 'formation_ia'
                });
            }
        }

        function downloadAll() {
            const data = collectData();
            const content = `MÉTHODE SMART COMPLÈTE - FORMATION IA DIGIT PIXIE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Date : ${new Date().toLocaleDateString('fr-FR')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 MA DÉCOMPOSITION SMART
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

S - SPÉCIFIQUE : ${data.specific || '[À définir]'}
M - MESURABLE : ${data.measurable || '[À définir]'}
A - ATTEIGNABLE : ${data.achievable || '[À définir]'}
R - RÉALISTE : ${data.realistic || '[À définir]'}
T - TEMPOREL : ${data.temporal || '[À définir]'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ MA PHRASE SMART COMPLÈTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"D'ici ${data.template.when}, je veux ${data.template.what} 
pour ${data.template.why}, mesurable par ${data.template.how}"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 MES 3 OBJECTIFS PRIORITAIRES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 OBJECTIF TECHNIQUE :
${data.goal1 || '[À définir]'}
Progress : ⬜ 0% ⬜ 25% ⬜ 50% ⬜ 75% ⬜ 100%

🎨 OBJECTIF CRÉATIF :
${data.goal2 || '[À définir]'}
Progress : ⬜ 0% ⬜ 25% ⬜ 50% ⬜ 75% ⬜ 100%

💰 OBJECTIF BUSINESS :
${data.goal3 || '[À définir]'}
Progress : ⬜ 0% ⬜ 25% ⬜ 50% ⬜ 75% ⬜ 100%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💪 AFFICHE CE DOCUMENT OÙ TU LE VOIS CHAQUE JOUR !
#DigitPixieIA #ObjectifsSMART`;

            const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `methode-smart-complete-${new Date().getTime()}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }

        function emailAll() {
            const data = collectData();
            const subject = "Ma Méthode SMART Complète - Formation IA";
            const body = `Ma méthode SMART pour la formation IA :

📝 DÉCOMPOSITION SMART :
S - ${data.specific || '[À définir]'}
M - ${data.measurable || '[À définir]'}
A - ${data.achievable || '[À définir]'}
R - ${data.realistic || '[À définir]'}
T - ${data.temporal || '[À définir]'}

✨ MA PHRASE COMPLÈTE :
"D'ici ${data.template.when}, je veux ${data.template.what} pour ${data.template.why}, mesurable par ${data.template.how}"

🎯 MES 3 OBJECTIFS :

🔧 TECHNIQUE : ${data.goal1 || '[À définir]'}
🎨 CRÉATIF : ${data.goal2 || '[À définir]'}
💰 BUSINESS : ${data.goal3 || '[À définir]'}

--
Formation IA by Digit Pixie
#ObjectifsSMART`;

            window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
        }

        function collectData() {
            const templateInputs = document.querySelectorAll('.template-input');
            return {
                specific: document.getElementById('specific').value,
                measurable: document.getElementById('measurable').value,
                achievable: document.getElementById('achievable').value,
                realistic: document.getElementById('realistic').value,
                temporal: document.getElementById('temporal').value,
                template: {
                    when: templateInputs[0].textContent,
                    what: templateInputs[1].textContent,
                    why: templateInputs[2].textContent,
                    how: templateInputs[3].textContent
                },
                goal1: document.getElementById('goal1').value,
                goal2: document.getElementById('goal2').value,
                goal3: document.getElementById('goal3').value
            };
        }

        // Auto-save
        setInterval(() => {
            const data = collectData();
            localStorage.setItem('digitpixie_smart_complete', JSON.stringify({
                ...data,
                date: new Date().toLocaleDateString('fr-FR'),
                timestamp: new Date().getTime()
            }));
        }, 30000);
    </script>
</body>
</html>'''

def main():
    # Configuration
    API_URL = "http://localhost:8001"
    
    # User credentials
    login_data = {
        "email": "admin@digitpixie.com",
        "password": "DigitPixie2025!"
    }
    
    # Tool data
    tool_data = {
        "title": "La méthode SMART",
        "description": "Transforme tes rêves IA en objectifs concrets et atteignables avec la méthode SMART complète",
        "category": "Formation IA",
        "html_content": SMART_TOOL_HTML,
        "preview_image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=240&fit=crop&q=80"
    }
    
    try:
        # Step 1: Login to get token
        print("🔐 Logging in...")
        login_response = requests.post(f"{API_URL}/api/auth/login", json=login_data)
        
        if not login_response.ok:
            print(f"❌ Login failed: {login_response.text}")
            return
            
        token = login_response.json()["access_token"]
        print("✅ Login successful!")
        
        # Step 2: Create the tool
        print("🔧 Creating SMART method tool...")
        headers = {"Authorization": f"Bearer {token}"}
        tool_response = requests.post(f"{API_URL}/api/tools", json=tool_data, headers=headers)
        
        if tool_response.ok:
            tool = tool_response.json()
            print(f"✅ Tool created successfully!")
            print(f"   ID: {tool['id']}")
            print(f"   Title: {tool['title']}")
            print(f"   Category: {tool['category']}")
            print(f"   Created: {tool['created_at']}")
        else:
            print(f"❌ Tool creation failed: {tool_response.text}")
            return
            
        # Step 3: Verify the tool was created
        print("🔍 Verifying tool creation...")
        tools_response = requests.get(f"{API_URL}/api/tools", headers=headers)
        
        if tools_response.ok:
            tools = tools_response.json()
            smart_tools = [t for t in tools if "SMART" in t['title']]
            print(f"✅ Verification successful! Found {len(smart_tools)} SMART tool(s)")
            for tool in smart_tools:
                print(f"   - {tool['title']} ({tool['category']})")
        else:
            print(f"❌ Verification failed: {tools_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()