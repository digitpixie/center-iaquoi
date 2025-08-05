#!/usr/bin/env python3
"""
Script to integrate the "PIXEL-IA Buddy" tamagotchi tool into the platform
"""
import requests
import json

# The complete HTML content for the PIXEL-IA Buddy tool
PIXEL_BUDDY_HTML = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PIXEL-IA Buddy - Tamagotchi Digital</title>
</head>
<body>
    <div id="pixel-buddy-wrapper" style="width: 100%; display: flex; justify-content: center; align-items: center; padding: 20px 0;">
        <div id="ia-tamagotchi-root"></div>
    </div>

    <style>
        /* Reset et conteneur principal */
        #pixel-buddy-wrapper {
            min-height: 650px;
            background: #0a0a0a;
            color: #fff;
        }
        
        #ia-tamagotchi-root {
            font-family: monospace;
            color: #fff;
            width: 100%;
            max-width: 450px;
            margin: 0 auto;
        }

        .tamagotchi-device {
            position: relative;
            margin: 0 auto;
        }

        .device-inner {
            background: transparent;
            padding: 0;
            position: relative;
            width: 420px;
            height: 640px;
            margin: 0 auto;
        }

        .led-strip {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 6px;
            z-index: 10;
        }

        .led {
            width: 5px;
            height: 5px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        .led-cyan { background: #06b6d4; box-shadow: 0 0 8px #06b6d4; }
        .led-purple { background: #a855f7; animation-delay: 0.1s; box-shadow: 0 0 8px #a855f7; }
        .led-pink { background: #ec4899; animation-delay: 0.2s; box-shadow: 0 0 8px #ec4899; }

        .screen {
            background: #000;
            border-radius: 2.5rem;
            height: 100%;
            overflow: hidden;
            position: relative;
            box-shadow: 0 0 50px rgba(6, 182, 212, 0.3), 
                        inset 0 0 20px rgba(6, 182, 212, 0.1);
        }

        .screen-content {
            padding: 16px;
            height: 100%;
            display: flex;
            flex-direction: column;
        }

        /* Header */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            margin-top: 20px;
        }

        .name-badge, .level-badge {
            background: rgba(0, 0, 0, 0.8);
            border-radius: 9999px;
            padding: 5px 14px;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 14px;
            backdrop-filter: blur(10px);
        }

        .name-badge {
            border: 1px solid rgba(6, 182, 212, 0.5);
            color: #06b6d4;
            box-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
        }

        .level-badge {
            border: 1px solid rgba(168, 85, 247, 0.5);
            color: #a855f7;
            box-shadow: 0 0 10px rgba(168, 85, 247, 0.3);
        }

        /* Stats */
        .stats-container {
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(10px);
            border-radius: 1rem;
            padding: 12px;
            margin-bottom: 12px;
            border: 1px solid rgba(6, 182, 212, 0.2);
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.1);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }

        .stat-bar {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .stat-icon {
            width: 14px;
            height: 14px;
            font-size: 14px;
        }

        .stat-track {
            flex: 1;
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 9999px;
            overflow: hidden;
        }

        .stat-fill {
            height: 100%;
            transition: width 0.5s ease;
            border-radius: 9999px;
        }

        .stat-fill-pink { 
            background: linear-gradient(to right, #ec4899, #f472b6); 
            box-shadow: 0 0 10px rgba(236, 72, 153, 0.5);
        }
        .stat-fill-purple { 
            background: linear-gradient(to right, #a855f7, #c084fc); 
            box-shadow: 0 0 10px rgba(168, 85, 247, 0.5);
        }
        .stat-fill-yellow { 
            background: linear-gradient(to right, #eab308, #facc15); 
            box-shadow: 0 0 10px rgba(234, 179, 8, 0.5);
        }
        .stat-fill-cyan { 
            background: linear-gradient(to right, #06b6d4, #22d3ee); 
            box-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
        }

        .stat-value {
            font-size: 12px;
            min-width: 35px;
            text-align: right;
        }

        /* Pet Display */
        .pet-display {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        .thought-bubble {
            position: absolute;
            top: 10px;
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(6, 182, 212, 0.5);
            border-radius: 8px;
            padding: 6px 14px;
            font-size: 13px;
            color: #06b6d4;
            animation: pulse 2s infinite;
            backdrop-filter: blur(10px);
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.3);
        }

        .thought-bubble::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 18px;
            width: 8px;
            height: 8px;
            background: rgba(0, 0, 0, 0.8);
            border-left: 1px solid rgba(6, 182, 212, 0.5);
            border-bottom: 1px solid rgba(6, 182, 212, 0.5);
            transform: rotate(-45deg);
        }

        .pet-container {
            position: relative;
            margin-top: 60px;
        }

        .pet-glow {
            position: absolute;
            inset: -25px;
            background: radial-gradient(circle, rgba(6, 182, 212, 0.3), rgba(168, 85, 247, 0.2), rgba(236, 72, 153, 0.1));
            border-radius: 50%;
            filter: blur(25px);
            animation: pulse 2s infinite;
        }

        .pet-body {
            position: relative;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 1.5rem;
            padding: 32px;
            backdrop-filter: blur(10px);
            box-shadow: 0 0 30px rgba(6, 182, 212, 0.2);
        }

        .pet-face {
            font-size: 52px;
            text-align: center;
            background: linear-gradient(to right, #06b6d4, #a855f7, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 20px currentColor);
            line-height: 1;
        }

        /* Evolution Progress */
        .evolution-container {
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(10px);
            border-radius: 1rem;
            padding: 12px;
            margin-bottom: 20px;
            border: 1px solid rgba(6, 182, 212, 0.2);
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.1);
        }

        .evolution-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .evolution-title {
            display: flex;
            align-items: center;
            gap: 6px;
            color: #06b6d4;
            font-size: 14px;
        }

        .evolution-stage {
            font-size: 12px;
            color: #a855f7;
        }

        .progress-bar {
            position: relative;
            background: rgba(255, 255, 255, 0.1);
            height: 12px;
            border-radius: 9999px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(to right, #06b6d4, #a855f7, #ec4899);
            transition: width 1s ease;
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.5);
        }

        .progress-nodes {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: space-around;
            padding: 0 8px;
        }

        .progress-node {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            transition: all 0.3s;
        }

        .progress-node.active {
            background: #06b6d4;
            box-shadow: 0 0 10px #06b6d4;
        }

        /* Action Buttons */
        .action-buttons {
            position: absolute;
            bottom: -30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 14px;
        }

        .action-btn {
            width: 60px;
            height: 60px;
            border-radius: 1rem;
            background: rgba(0, 0, 0, 0.9);
            border: 1px solid transparent;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 28px;
            backdrop-filter: blur(10px);
        }

        .action-btn:hover {
            transform: scale(1.1) translateY(-2px);
        }

        .action-btn-cyan {
            border-color: rgba(6, 182, 212, 0.5);
            box-shadow: 0 0 20px rgba(6, 182, 212, 0.2);
        }

        .action-btn-cyan:hover {
            border-color: #06b6d4;
            box-shadow: 0 0 30px rgba(6, 182, 212, 0.6);
            background: rgba(6, 182, 212, 0.1);
        }

        .action-btn-purple {
            border-color: rgba(168, 85, 247, 0.5);
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.2);
        }

        .action-btn-purple:hover {
            border-color: #a855f7;
            box-shadow: 0 0 30px rgba(168, 85, 247, 0.6);
            background: rgba(168, 85, 247, 0.1);
        }

        .action-btn-blue {
            border-color: rgba(59, 130, 246, 0.5);
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.2);
        }

        .action-btn-blue:hover {
            border-color: #3b82f6;
            box-shadow: 0 0 30px rgba(59, 130, 246, 0.6);
            background: rgba(59, 130, 246, 0.1);
        }

        .action-btn-pink {
            border-color: rgba(236, 72, 153, 0.5);
            box-shadow: 0 0 20px rgba(236, 72, 153, 0.2);
        }

        .action-btn-pink:hover {
            border-color: #ec4899;
            box-shadow: 0 0 30px rgba(236, 72, 153, 0.6);
            background: rgba(236, 72, 153, 0.1);
        }

        /* Messages */
        .message-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            border: 1px solid #06b6d4;
            border-radius: 12px;
            padding: 14px 28px;
            animation: pulse 0.5s;
            z-index: 20;
            backdrop-filter: blur(10px);
            box-shadow: 0 0 30px rgba(6, 182, 212, 0.5);
        }

        .message-text {
            color: #06b6d4;
            font-size: 15px;
            white-space: nowrap;
        }

        /* Help Button */
        .help-button {
            position: absolute;
            top: 15px;
            right: 15px;
            width: 48px;
            height: 48px;
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(168, 85, 247, 0.5);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s;
            color: #a855f7;
            font-size: 22px;
            backdrop-filter: blur(10px);
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.2);
        }

        .help-button:hover {
            border-color: #a855f7;
            box-shadow: 0 0 30px rgba(168, 85, 247, 0.6);
            background: rgba(168, 85, 247, 0.1);
        }

        /* Modals */
        .modal-backdrop {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.85);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 50;
            padding: 16px;
            backdrop-filter: blur(5px);
        }

        .modal {
            background: rgba(0, 0, 0, 0.95);
            border: 1px solid rgba(6, 182, 212, 0.5);
            border-radius: 1.5rem;
            padding: 28px;
            max-width: 400px;
            width: 100%;
            position: relative;
            backdrop-filter: blur(20px);
            box-shadow: 0 0 40px rgba(6, 182, 212, 0.3);
        }

        .modal-title {
            font-size: 18px;
            color: #06b6d4;
            text-align: center;
            margin-bottom: 16px;
            text-shadow: 0 0 15px rgba(6, 182, 212, 0.8);
        }

        .modal-content {
            color: #9ca3af;
            font-size: 15px;
        }

        .code-input {
            width: 100%;
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid rgba(6, 182, 212, 0.5);
            border-radius: 10px;
            padding: 10px 18px;
            color: #06b6d4;
            font-family: monospace;
            font-size: 15px;
            margin-top: 16px;
            outline: none;
            text-transform: uppercase;
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.2);
        }

        .code-input:focus {
            border-color: #06b6d4;
            box-shadow: 0 0 25px rgba(6, 182, 212, 0.5);
            background: rgba(6, 182, 212, 0.05);
        }

        .modal-buttons {
            display: flex;
            gap: 10px;
            margin-top: 18px;
        }

        .modal-btn {
            flex: 1;
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid rgba(6, 182, 212, 0.5);
            border-radius: 10px;
            padding: 10px;
            color: #06b6d4;
            font-size: 15px;
            cursor: pointer;
            transition: all 0.3s;
            backdrop-filter: blur(10px);
        }

        .modal-btn:hover {
            border-color: #06b6d4;
            box-shadow: 0 0 20px rgba(6, 182, 212, 0.6);
            background: rgba(6, 182, 212, 0.1);
        }

        .modal-btn-cancel {
            color: #a855f7;
            border-color: rgba(168, 85, 247, 0.5);
        }

        .modal-btn-cancel:hover {
            border-color: #a855f7;
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.6);
            background: rgba(168, 85, 247, 0.1);
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }

        /* Responsive pour tablettes */
        @media (max-width: 768px) {
            #pixel-buddy-wrapper {
                min-height: 600px;
            }

            .device-inner {
                width: 380px;
                height: 600px;
            }
            
            .pet-face {
                font-size: 48px;
            }
            
            .action-btn {
                width: 55px;
                height: 55px;
                font-size: 26px;
            }
        }

        /* Responsive pour mobiles */
        @media (max-width: 480px) {
            #pixel-buddy-wrapper {
                min-height: 550px;
                padding: 10px 0;
            }
            
            .device-inner {
                width: 320px;
                height: 520px;
            }

            .screen-content {
                padding: 12px;
            }

            .header {
                margin-top: 15px;
            }

            .name-badge, .level-badge {
                font-size: 12px;
                padding: 4px 10px;
            }
            
            .pet-face {
                font-size: 42px;
            }
            
            .pet-body {
                padding: 24px;
            }
            
            .action-btn {
                width: 48px;
                height: 48px;
                font-size: 24px;
            }

            .action-buttons {
                gap: 10px;
                bottom: -25px;
            }
        }
    </style>

    <script>
    (function() {
        // État du pet
        let pet = {
            name: "PIXEL-IA",
            level: 1,
            happiness: 80,
            knowledge: 60,
            energy: 75,
            hunger: 70,
            stage: "baby",
            modulesCompleted: 0,
            currentAnimation: "idle",
            thoughtBubble: "Système.init() ✨",
            mood: "happy"
        };

        let showMessage = false;
        let messageText = "";
        let showCodeModal = false;
        let showHelpModal = false;

        const moduleCodes = {
            'START-GAME': { module: 1, name: "Mindset & Éthique IA" },
            'POWER-UP': { module: 2, name: "Les 3 Cerveaux IA" },
            'NEW-SKIN': { module: 3, name: "Création Avatar" },
            'PRESS-PLAY': { module: 4, name: "Avatar en Action" },
            'GOD-MODE': { module: 5, name: "Maître des Images IA" },
            'GG-WP': { module: 6, name: "Réalisateur Vidéo IA" }
        };

        const petVisuals = {
            baby: {
                idle: "◔ ◡ ◔",
                happy: "◕ ‿ ◕",
                sleep: "- _ -",
                eat: "◔ ڡ ◔",
                learn: "◉ _ ◉"
            },
            teen: {
                idle: "● ◡ ●",
                happy: "◉ ‿ ◉",
                sleep: "◡ _ ◡",
                eat: "● ڡ ●",
                learn: "◉ ▿ ◉"
            },
            adult: {
                idle: "◆ ◡ ◆",
                happy: "✦ ‿ ✦",
                sleep: "◡ _ ◡",
                eat: "◆ ڡ ◆",
                learn: "◆ ▿ ◆"
            },
            master: {
                idle: "⬡ ◡ ⬡",
                happy: "✧ ‿ ✧",
                sleep: "◡ _ ◡",
                eat: "⬡ ڡ ⬡",
                learn: "⬡ ▿ ⬡"
            }
        };

        const thoughts = {
            happy: ["Bonjour.monde() 💜", "Compilation du bonheur...", "RAM: 100% joie", "< mode heureux />"],
            neutral: ["Traitement...", "await réponse", "Réflexion.exe", "if(humeur) {...}"],
            sad: ["Batterie.faible() 🔋", "Besoin.données()", "404: Énergie introuvable", "Cache.vide()"],
            excited: ["NIVEAU.SUP()! 🚀", "Images.géniales() 🎨", "Vidéos.render() 🎬", "Créativité.MAX()"],
            sleepy: ["Mode.veille() 💤", "Hibernation.init()", "État.basse.énergie", "Zzz.exe"]
        };

        function showNotification(msg) {
            messageText = msg;
            showMessage = true;
            render();
            setTimeout(() => {
                showMessage = false;
                render();
            }, 3000);
        }

        function feedPet() {
            if (pet.hunger >= 90) {
                showNotification("Mémoire.pleine() 💾");
                return;
            }
            
            pet.hunger = Math.min(100, pet.hunger + 30);
            pet.energy = Math.min(100, pet.energy + 10);
            pet.happiness = Math.min(100, pet.happiness + 5);
            pet.currentAnimation = "eat";
            pet.thoughtBubble = "Données.délicieuses() 🍜";
            render();
            
            setTimeout(() => {
                pet.currentAnimation = "idle";
                render();
            }, 1500);
        }

        function playWithPet() {
            if (pet.happiness >= 90) {
                showNotification("Joie.maximale() 💜");
                return;
            }
            
            pet.happiness = Math.min(100, pet.happiness + 25);
            pet.energy = Math.max(10, pet.energy - 10);
            pet.currentAnimation = "happy";
            pet.thoughtBubble = "Partie.lancée() 🎮";
            render();
            
            setTimeout(() => {
                pet.currentAnimation = "idle";
                render();
            }, 1500);
        }

        function restPet() {
            pet.energy = Math.min(100, pet.energy + 40);
            pet.currentAnimation = "sleep";
            pet.thoughtBubble = "Mode.recharge() ⚡";
            render();
            
            setTimeout(() => {
                pet.currentAnimation = "idle";
                render();
            }, 2000);
        }

        function teachPet() {
            showCodeModal = true;
            render();
        }

        function validateCode() {
            const input = document.getElementById('module-code-input');
            if (!input) return;
            
            const code = input.value.toUpperCase().trim();
            const moduleData = moduleCodes[code];
            
            if (moduleData) {
                if (moduleData.module <= pet.modulesCompleted) {
                    showNotification("⚠️ Module déjà validé!");
                } else if (moduleData.module === pet.modulesCompleted + 1) {
                    pet.modulesCompleted++;
                    pet.happiness = 100;
                    pet.knowledge = Math.min(100, pet.knowledge + 30);
                    pet.energy = 100;
                    pet.hunger = 100;
                    pet.mood = "excited";
                    pet.thoughtBubble = "Succès.log() 🎊";
                    
                    // AUGMENTER LE NIVEAU
                    pet.level = pet.modulesCompleted;
                    
                    // Messages personnalisés pour chaque module
                    let customMessage = "";
                    
                    switch(code) {
                        case 'START-GAME':
                            customMessage = "🎮 GAME.START() // Aventure IA lancée!";
                            break;
                        case 'POWER-UP':
                            customMessage = "⚡ CERVEAUX.ACTIVÉS() // 3 IA maîtrisées!";
                            break;
                        case 'NEW-SKIN':
                            customMessage = "✨ AVATAR.CRÉÉ() // Double digital unlocked!";
                            break;
                        case 'PRESS-PLAY':
                            customMessage = "🎬 AVATAR.ANIMÉ() // Il prend vie!";
                            break;
                        case 'GOD-MODE':
                            customMessage = "🎨 IMAGES.MAÎTRISÉES() // Artiste IA activé!";
                            break;
                        case 'GG-WP':
                            customMessage = "🎬 VIDÉOS.UNLOCKED() // Réalisateur suprême!";
                            break;
                        default:
                            customMessage = `✅ ${moduleData.name} validé!`;
                    }
                    
                    // Check evolution avec messages spéciaux
                    if (pet.modulesCompleted === 6 && pet.stage === "adult") {
                        pet.stage = "master";
                        showNotification("🏆 MAÎTRISE.TOTALE() // GG WP Champion!");
                    } else if (pet.modulesCompleted >= 3 && pet.stage === "teen") {
                        pet.stage = "adult";
                        showNotification("🔥 NIVEAU.SUP() // Mode Adulte Activé!");
                    } else if (pet.modulesCompleted >= 1 && pet.stage === "baby") {
                        pet.stage = "teen";
                        showNotification("✨ MISE.À.JOUR() // Version Ado!");
                    } else {
                        showNotification(customMessage);
                    }
                } else {
                    showNotification("⚠️ Complète les modules dans l'ordre!");
                }
            } else {
                showNotification("❌ Code invalide!");
            }
            
            showCodeModal = false;
            input.value = "";
            render();
        }

        function getCurrentVisual() {
            const stage = petVisuals[pet.stage];
            return stage[pet.currentAnimation] || stage.idle;
        }

        function render() {
            const root = document.getElementById('ia-tamagotchi-root');
            if (!root) return;

            root.innerHTML = `
                <div class="tamagotchi-device">
                    <div class="device-inner">
                        <div class="led-strip">
                            <div class="led led-cyan"></div>
                            <div class="led led-purple"></div>
                            <div class="led led-pink"></div>
                        </div>
                        
                        <div class="screen">
                            <div class="screen-content">
                                <div class="header">
                                    <div class="name-badge">
                                        <span>⚡</span>
                                        <span>${pet.name}</span>
                                    </div>
                                    <div class="level-badge">
                                        <span>NIV.${pet.level}</span>
                                    </div>
                                </div>
                                
                                <div class="stats-container">
                                    <div class="stats-grid">
                                        <div class="stat-bar">
                                            <span class="stat-icon">❤️</span>
                                            <div class="stat-track">
                                                <div class="stat-fill stat-fill-pink" style="width: ${pet.happiness}%"></div>
                                            </div>
                                            <span class="stat-value" style="color: #ec4899">${pet.happiness}%</span>
                                        </div>
                                        
                                        <div class="stat-bar">
                                            <span class="stat-icon">🧠</span>
                                            <div class="stat-track">
                                                <div class="stat-fill stat-fill-purple" style="width: ${pet.knowledge}%"></div>
                                            </div>
                                            <span class="stat-value" style="color: #a855f7">${pet.knowledge}%</span>
                                        </div>
                                        
                                        <div class="stat-bar">
                                            <span class="stat-icon">⚡</span>
                                            <div class="stat-track">
                                                <div class="stat-fill stat-fill-yellow" style="width: ${pet.energy}%"></div>
                                            </div>
                                            <span class="stat-value" style="color: #eab308">${pet.energy}%</span>
                                        </div>
                                        
                                        <div class="stat-bar">
                                            <span class="stat-icon">💾</span>
                                            <div class="stat-track">
                                                <div class="stat-fill stat-fill-cyan" style="width: ${pet.hunger}%"></div>
                                            </div>
                                            <span class="stat-value" style="color: #06b6d4">${pet.hunger}%</span>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="pet-display">
                                    <div class="thought-bubble">
                                        &gt; ${pet.thoughtBubble}
                                    </div>
                                    
                                    <div class="pet-container">
                                        <div class="pet-glow"></div>
                                        <div class="pet-body">
                                            <div class="pet-face">${getCurrentVisual()}</div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="evolution-container">
                                    <div class="evolution-header">
                                        <div class="evolution-title">
                                            <span>💻</span>
                                            <span>ÉTAT.ÉVOLUTION</span>
                                        </div>
                                        <span class="evolution-stage">MODE_${pet.stage.toUpperCase()}</span>
                                    </div>
                                    
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: ${(pet.modulesCompleted / 6) * 100}%"></div>
                                        <div class="progress-nodes">
                                            ${[...Array(6)].map((_, i) => `
                                                <div class="progress-node ${pet.modulesCompleted > i ? 'active' : ''}"></div>
                                            `).join('')}
                                        </div>
                                    </div>
                                    
                                    <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                                        <span style="color: #6b7280; font-size: 12px;">
                                            MODULES [${pet.modulesCompleted}/6]
                                        </span>
                                        <span style="color: #06b6d4; font-size: 12px;">
                                            ${pet.stage === "master" 
                                                ? "NIVEAU_MAX_ATTEINT ✨" 
                                                : pet.modulesCompleted === 0
                                                ? "ÉVOLUTION DANS: 1 MODULE"
                                                : pet.modulesCompleted < 3
                                                ? "ÉVOLUTION DANS: " + (3 - pet.modulesCompleted) + " MODULES"
                                                : pet.modulesCompleted < 6
                                                ? "ÉVOLUTION DANS: " + (6 - pet.modulesCompleted) + " MODULES"
                                                : ""}
                                        </span>
                                    </div>
                                </div>
                                
                                ${showMessage ? `
                                    <div class="message-overlay">
                                        <div class="message-text">${messageText}</div>
                                    </div>
                                ` : ''}
                            </div>
                        </div>
                        
                        <div class="action-buttons">
                            <button class="action-btn action-btn-cyan" onclick="pixelBuddy.feed()">
                                <span>🍜</span>
                            </button>
                            <button class="action-btn action-btn-purple" onclick="pixelBuddy.play()">
                                <span>🎮</span>
                            </button>
                            <button class="action-btn action-btn-blue" onclick="pixelBuddy.rest()">
                                <span>⚡</span>
                            </button>
                            <button class="action-btn action-btn-pink" onclick="pixelBuddy.teach()">
                                <span>🧠</span>
                            </button>
                        </div>
                    </div>
                </div>
                
                <button class="help-button" onclick="pixelBuddy.toggleHelp()">
                    <span>❓</span>
                </button>
                
                ${showCodeModal ? `
                    <div class="modal-backdrop" onclick="pixelBuddy.closeModal()">
                        <div class="modal" onclick="event.stopPropagation()">
                            <h3 class="modal-title">MODULE.VALIDATION()</h3>
                            <p class="modal-content" style="text-align: center; margin-bottom: 18px;">
                                Entre le code donné à la fin du module Skool
                            </p>
                            <input
                                type="text"
                                id="module-code-input"
                                class="code-input"
                                placeholder="CODE-MODULE"
                                onkeypress="if(event.key === 'Enter') pixelBuddy.validate()"
                            />
                            <div style="margin-top: 18px; text-align: center; font-size: 13px; color: #6b7280;">
                                Prochain module: ${pet.modulesCompleted < 6 ? `Module ${pet.modulesCompleted + 1}` : 'Tous complétés!'}
                            </div>
                            <div class="modal-buttons">
                                <button class="modal-btn" onclick="pixelBuddy.validate()">
                                    VALIDER()
                                </button>
                                <button class="modal-btn modal-btn-cancel" onclick="pixelBuddy.closeModal()">
                                    ANNULER()
                                </button>
                            </div>
                        </div>
                    </div>
                ` : ''}
                
                ${showHelpModal ? `
                    <div class="modal-backdrop" onclick="pixelBuddy.closeHelp()">
                        <div class="modal" onclick="event.stopPropagation()">
                            <h3 class="modal-title">PIXEL-IA.AIDE()</h3>
                            <div style="background: rgba(0, 0, 0, 0.5); border-radius: 12px; padding: 18px; margin-top: 16px;">
                                <p style="color: #a855f7; margin-bottom: 10px; font-size: 15px;">&gt; IA évolutive cyberpunk</p>
                                <p style="color: #9ca3af; margin-bottom: 10px; font-size: 15px;">&gt; Complète modules = XP++</p>
                                <p style="color: #9ca3af; margin-bottom: 10px; font-size: 15px;">&gt; Maintiens stats &gt; 50%</p>
                                <p style="color: #9ca3af; margin-bottom: 10px; font-size: 15px;">&gt; Évolution: ${6 - pet.modulesCompleted} modules</p>
                                <p style="color: #06b6d4; font-size: 15px;">&gt; système.prêt = true</p>
                            </div>
                            <button class="modal-btn" style="margin-top: 18px; width: 100%;" onclick="pixelBuddy.closeHelp()">
                                FERMER()
                            </button>
                        </div>
                    </div>
                ` : ''}
            `;
        }

        // Interface publique
        window.pixelBuddy = {
            feed: feedPet,
            play: playWithPet,
            rest: restPet,
            teach: teachPet,
            validate: validateCode,
            closeModal: () => {
                showCodeModal = false;
                render();
            },
            toggleHelp: () => {
                showHelpModal = !showHelpModal;
                render();
            },
            closeHelp: () => {
                showHelpModal = false;
                render();
            }
        };

        // Initialisation
        document.addEventListener('DOMContentLoaded', () => {
            render();
            
            // Mise à jour périodique
            setInterval(() => {
                // Diminuer les stats lentement
                pet.happiness = Math.max(10, pet.happiness - 2);
                pet.energy = Math.max(10, pet.energy - 3);
                pet.hunger = Math.max(10, pet.hunger - 4);
                
                // Mettre à jour l'humeur
                if (pet.happiness > 70 && pet.energy > 50) {
                    pet.mood = "happy";
                } else if (pet.happiness < 30 || pet.energy < 30) {
                    pet.mood = "sad";
                } else if (pet.energy < 20) {
                    pet.mood = "sleepy";
                } else {
                    pet.mood = "neutral";
                }
                
                // Changer la pensée
                const moodThoughts = thoughts[pet.mood];
                pet.thoughtBubble = moodThoughts[Math.floor(Math.random() * moodThoughts.length)];
                
                render();
            }, 30000); // Toutes les 30 secondes
        });
    })();
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
        "title": "PIXEL-IA Buddy",
        "description": "Tamagotchi digital évolutif qui grandit avec tes progrès dans les modules IA - Nourris-le, joue avec lui et regarde-le évoluer !",
        "category": "Gaming",
        "html_content": PIXEL_BUDDY_HTML,
        "preview_image": "https://images.unsplash.com/photo-1560472355-536de3962603?w=400&h=240&fit=crop&q=80"
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
        print("🎮 Creating PIXEL-IA Buddy tamagotchi tool...")
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
            pixel_tools = [t for t in tools if "PIXEL" in t['title'].upper()]
            print(f"✅ Verification successful! Found {len(pixel_tools)} PIXEL-IA tool(s)")
            for tool in pixel_tools:
                print(f"   - {tool['title']} ({tool['category']})")
                
            # Show total tools
            total_tools = len(tools)
            print(f"\n📊 Platform now has {total_tools} tools total:")
            for tool in tools:
                print(f"   - {tool['title']} ({tool['category']})")
        else:
            print(f"❌ Verification failed: {tools_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()