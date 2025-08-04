#!/usr/bin/env python3
"""
Script to integrate the "Diagnostic créateur IA" tool into the platform
"""
import requests
import json

# The complete HTML content for the Diagnostic tool
DIAGNOSTIC_TOOL_HTML = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quel Créateur IA es-tu ? - Diagnostic Complet - Digit Pixie</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            color: #ffffff;
            background: #0a0a0a;
            background-image: 
                radial-gradient(circle at 20% 50%, rgba(255, 0, 255, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(0, 255, 255, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 80%, rgba(255, 255, 0, 0.2) 0%, transparent 50%);
            min-height: 100vh;
            position: relative;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                linear-gradient(45deg, transparent 40%, rgba(255, 0, 255, 0.1) 50%, transparent 60%),
                linear-gradient(-45deg, transparent 40%, rgba(0, 255, 255, 0.1) 50%, transparent 60%);
            animation: neonPulse 4s ease-in-out infinite;
            pointer-events: none;
            z-index: -1;
        }
        
        @keyframes neonPulse {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
        }
        
        @keyframes glow {
            0%, 100% { 
                box-shadow: 
                    0 0 5px #ff00ff,
                    0 0 10px #ff00ff,
                    0 0 15px #ff00ff,
                    0 0 20px #ff00ff;
            }
            50% { 
                box-shadow: 
                    0 0 10px #00ffff,
                    0 0 20px #00ffff,
                    0 0 30px #00ffff,
                    0 0 40px #00ffff;
            }
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
            padding: 40px 0;
        }
        
        .header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 16px;
            background: linear-gradient(45deg, #8a2be2, #ff00ff, #4169e1, #ff00ff);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradientShift 3s ease-in-out infinite;
        }
        
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        }
        
        .quiz-container {
            background: rgba(20, 20, 20, 0.9);
            border: 2px solid #ff00ff;
            border-radius: 20px;
            box-shadow: 
                0 0 20px rgba(255, 0, 255, 0.5),
                inset 0 0 20px rgba(255, 0, 255, 0.1);
            overflow: hidden;
            margin-bottom: 40px;
            backdrop-filter: blur(10px);
        }
        
        .progress-container {
            background: rgba(20, 20, 20, 0.9);
            border: 2px solid #00ffff;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 
                0 0 20px rgba(0, 255, 255, 0.3),
                inset 0 0 20px rgba(0, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .progress-bar {
            height: 16px;
            background: #1a1a1a;
            position: relative;
            border: 1px solid #333;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 10px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #8a2be2, #ff00ff, #4169e1, #ff00ff);
            background-size: 200% 200%;
            width: 0%;
            transition: width 0.3s ease;
            box-shadow: 
                0 0 15px rgba(255, 0, 255, 0.6),
                inset 0 0 10px rgba(255, 255, 255, 0.2);
            border-radius: 7px;
            position: relative;
            animation: fluidFlow 3s ease-in-out infinite;
        }
        
        @keyframes fluidFlow {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .progress-text {
            text-align: center;
            color: #00ffff;
            font-weight: 600;
            font-size: 1rem;
            text-shadow: 0 0 10px #00ffff;
        }
        
        .quiz-content {
            padding: 40px 40px 20px 40px;
        }
        
        .section-header {
            background: linear-gradient(135deg, rgba(255, 0, 255, 0.2), rgba(0, 255, 255, 0.2));
            border: 1px solid #00ffff;
            color: white;
            padding: 20px 40px;
            margin: -40px -40px 30px -40px;
            box-shadow: 
                0 0 15px rgba(0, 255, 255, 0.3),
                inset 0 0 15px rgba(0, 255, 255, 0.1);
        }
        
        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 8px;
            text-shadow: 0 0 10px #00ffff;
        }
        
        .section-subtitle {
            opacity: 0.9;
            font-size: 1rem;
            text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
        }
        
        .question {
            margin-bottom: 40px;
            display: none;
        }
        
        .question.active {
            display: block;
            animation: fadeInGlow 0.5s ease-in-out;
        }
        
        @keyframes fadeInGlow {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        
        .question h3 {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 24px;
            color: #ffffff;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        }
        
        .answers {
            display: grid;
            gap: 12px;
        }
        
        .answer {
            background: rgba(30, 30, 30, 0.8);
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            backdrop-filter: blur(5px);
        }
        
        .answer:hover {
            border-color: #00ffff;
            background: rgba(40, 40, 40, 0.9);
            transform: translateY(-2px);
            box-shadow: 
                0 5px 15px rgba(0, 255, 255, 0.3),
                inset 0 0 20px rgba(0, 255, 255, 0.1);
        }
        
        .answer.selected {
            border-color: #ff00ff;
            background: rgba(50, 50, 50, 0.9);
            box-shadow: 
                0 0 20px rgba(255, 0, 255, 0.5),
                inset 0 0 20px rgba(255, 0, 255, 0.2);
            animation: selectedGlow 2s ease-in-out infinite;
        }
        
        @keyframes selectedGlow {
            0%, 100% { 
                box-shadow: 
                    0 0 20px rgba(255, 0, 255, 0.5),
                    inset 0 0 20px rgba(255, 0, 255, 0.2);
            }
            50% { 
                box-shadow: 
                    0 0 30px rgba(255, 0, 255, 0.8),
                    inset 0 0 30px rgba(255, 0, 255, 0.3);
            }
        }
        
        .answer-text {
            font-weight: 500;
            color: #ffffff;
            text-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
        }
        
        .navigation {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 30px;
            margin-bottom: 20px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 0, 255, 0.3);
        }
        
        .btn {
            padding: 12px 32px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid;
            font-size: 1rem;
            position: relative;
            overflow: hidden;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s ease;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn-primary {
            background: linear-gradient(45deg, #ff00ff, #00ffff);
            color: white;
            border-color: #ff00ff;
            box-shadow: 0 0 15px rgba(255, 0, 255, 0.4);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 5px 20px rgba(255, 0, 255, 0.6),
                0 0 30px rgba(0, 255, 255, 0.4);
        }
        
        .btn-secondary {
            background: rgba(40, 40, 40, 0.8);
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(5px);
        }
        
        .btn-secondary:hover {
            background: rgba(60, 60, 60, 0.9);
            border-color: #00ffff;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
        }
        
        .question-counter {
            color: #ffffff;
            font-weight: 500;
            text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
        }
        
        .results-container {
            display: none;
            background: rgba(20, 20, 20, 0.9);
            border: 2px solid #00ffff;
            border-radius: 20px;
            box-shadow: 
                0 0 30px rgba(0, 255, 255, 0.5),
                inset 0 0 30px rgba(0, 255, 255, 0.1);
            overflow: hidden;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        
        .results-header {
            background: linear-gradient(135deg, rgba(255, 0, 255, 0.3), rgba(0, 255, 255, 0.3));
            border-bottom: 1px solid rgba(255, 255, 0, 0.3);
            color: white;
            padding: 40px;
            position: relative;
        }
        
        .results-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 30% 30%, rgba(255, 0, 255, 0.2) 0%, transparent 50%),
                radial-gradient(circle at 70% 70%, rgba(0, 255, 255, 0.2) 0%, transparent 50%);
            animation: resultsPulse 3s ease-in-out infinite;
        }
        
        @keyframes resultsPulse {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
        }
        
        .results-title {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 16px;
            text-shadow: 0 0 15px #ffff00;
            position: relative;
            z-index: 1;
        }
        
        .archetype-badge {
            display: inline-block;
            font-size: 3rem;
            margin-bottom: 16px;
            filter: drop-shadow(0 0 10px #ffff00);
            position: relative;
            z-index: 1;
        }
        
        .archetype-name {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 8px;
            background: linear-gradient(45deg, #ff00ff, #00ffff, #ffff00);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradientShift 2s ease-in-out infinite;
            position: relative;
            z-index: 1;
        }
        
        .archetype-score {
            font-size: 1.1rem;
            opacity: 0.9;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
            position: relative;
            z-index: 1;
        }
        
        .results-content {
            padding: 40px;
            text-align: left;
        }
        
        .result-section {
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(30, 30, 30, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            backdrop-filter: blur(5px);
        }
        
        .result-section h4 {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 12px;
            color: #ffffff;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        }
        
        .strengths, .challenges {
            list-style: none;
            padding: 0;
        }
        
        .strengths li, .challenges li {
            padding: 8px 0;
            padding-left: 24px;
            position: relative;
            color: #ffffff;
            text-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
        }
        
        .strengths li::before {
            content: "✅";
            position: absolute;
            left: 0;
            filter: drop-shadow(0 0 5px #00ff00);
        }
        
        .challenges li::before {
            content: "⚠️";
            position: absolute;
            left: 0;
            filter: drop-shadow(0 0 5px #ffff00);
        }
        
        .cta-section {
            background: linear-gradient(135deg, rgba(255, 0, 255, 0.2), rgba(0, 255, 255, 0.2));
            border: 2px solid #ffff00;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            margin-top: 30px;
            box-shadow: 
                0 0 20px rgba(255, 255, 0, 0.3),
                inset 0 0 20px rgba(255, 255, 0, 0.1);
        }
        
        .cta-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 16px;
            color: #ffffff;
            text-shadow: 0 0 10px #ffff00;
        }
        
        .cta-btn {
            display: inline-block;
            background: linear-gradient(45deg, #ff00ff, #00ffff, #ffff00, #ff00ff);
            background-size: 300% 300%;
            color: #000000;
            padding: 16px 40px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            border: 2px solid #ffff00;
            box-shadow: 0 0 20px rgba(255, 255, 0, 0.5);
            animation: gradientShift 2s ease-in-out infinite;
            text-shadow: none;
        }
        
        .cta-btn:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 
                0 10px 30px rgba(255, 255, 0, 0.6),
                0 0 40px rgba(255, 0, 255, 0.4);
            text-decoration: none;
            color: #000000;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .quiz-content {
                padding: 20px;
            }
            
            .section-header {
                padding: 20px;
                margin: -20px -20px 20px -20px;
            }
            
            .navigation {
                flex-direction: column;
                gap: 16px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>Quel Créateur IA es-tu ?</h1>
            <p>Découvre ton profil de créateur IA et obtiens ton plan d'action personnalisé pour maîtriser l'IA créative !</p>
        </div>

        <!-- Progress Bar Standalone -->
        <div class="progress-container">
            <div class="progress-bar">
                <div class="progress-fill" id="progressBar"></div>
            </div>
            <div class="progress-text">
                <span id="currentQuestion">1</span> / 20 questions
            </div>
        </div>

        <!-- Quiz Container -->
        <div class="quiz-container" id="quizContainer">
            <div class="quiz-content">
                <!-- Section 1: Profil Créatif -->
                <div class="section-header">
                    <div class="section-title">🎨 Section 1/4 : Ton Profil Créatif Actuel</div>
                    <div class="section-subtitle">Comprendre où tu en es aujourd'hui</div>
                </div>

                <!-- Question 1 -->
                <div class="question active" data-section="1">
                    <h3>Comment décrirais-tu ton niveau actuel en création de contenu ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="pragmatique" data-points="2">
                            <div class="answer-text">Je débute, j'apprends les bases</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="2">
                            <div class="answer-text">Je maîtrise les outils classiques (Canva, etc.)</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="2">
                            <div class="answer-text">Je suis créatif mais cherche de nouveaux moyens d'expression</div>
                        </div>
                        <div class="answer" data-archetype="stratege" data-points="2">
                            <div class="answer-text">Je crée régulièrement et cherche l'efficacité</div>
                        </div>
                    </div>
                </div>

                <!-- Question 2 -->
                <div class="question" data-section="1">
                    <h3>Quelle est ta plus grande frustration actuelle ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="pragmatique" data-points="2">
                            <div class="answer-text">Manque de temps pour créer</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="2">
                            <div class="answer-text">Résultats pas assez professionnels</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="2">
                            <div class="answer-text">Manque d'inspiration/créativité</div>
                        </div>
                        <div class="answer" data-archetype="stratege" data-points="2">
                            <div class="answer-text">Process trop lent/inefficace</div>
                        </div>
                        <div class="answer" data-archetype="explorateur" data-points="2">
                            <div class="answer-text">Je ne sais pas par où commencer</div>
                        </div>
                    </div>
                </div>

                <!-- Question 3 -->
                <div class="question" data-section="1">
                    <h3>Combien de temps passes-tu actuellement sur la création de contenu par semaine ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="pragmatique" data-points="1">
                            <div class="answer-text">Moins de 2 heures</div>
                        </div>
                        <div class="answer" data-archetype="stratege" data-points="2">
                            <div class="answer-text">2 à 5 heures</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="2">
                            <div class="answer-text">5 à 10 heures</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="3">
                            <div class="answer-text">Plus de 10 heures</div>
                        </div>
                    </div>
                </div>

                <!-- Question 4 -->
                <div class="question" data-section="1">
                    <h3>Quel type de contenu te prend le plus de temps ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="artiste" data-points="2">
                            <div class="answer-text">Visuels et design graphique</div>
                        </div>
                        <div class="answer" data-archetype="stratege" data-points="2">
                            <div class="answer-text">Rédaction et copywriting</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="2">
                            <div class="answer-text">Vidéos et montage</div>
                        </div>
                        <div class="answer" data-archetype="explorateur" data-points="2">
                            <div class="answer-text">Tout me prend du temps</div>
                        </div>
                    </div>
                </div>

                <!-- Question 5 -->
                <div class="question" data-section="1">
                    <h3>Comment te sens-tu face aux nouvelles technologies ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="explorateur" data-points="3">
                            <div class="answer-text">Excité(e), j'adore découvrir</div>
                        </div>
                        <div class="answer" data-archetype="pragmatique" data-points="2">
                            <div class="answer-text">Prudent(e), je teste d'abord</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="2">
                            <div class="answer-text">Méthodique, j'apprends tout</div>
                        </div>
                        <div class="answer" data-archetype="stratege" data-points="2">
                            <div class="answer-text">Sélectif(ve), si c'est rentable</div>
                        </div>
                    </div>
                </div>

                <!-- Section 2: Mindset IA -->
                <div class="section-header" style="display: none;">
                    <div class="section-title">🧠 Section 2/4 : Ton Mindset IA</div>
                    <div class="section-subtitle">Comment tu vois l'intelligence artificielle</div>
                </div>

                <!-- Question 6 -->
                <div class="question" data-section="2">
                    <h3>Face à un nouvel outil IA, ta première réaction ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="explorateur" data-points="3">
                            <div class="answer-text">"Wahou ! Je teste immédiatement"</div>
                        </div>
                        <div class="answer" data-archetype="stratege" data-points="3">
                            <div class="answer-text">"Quel ROI je peux en attendre ?"</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="3">
                            <div class="answer-text">"Est-ce que ça va m'aider créativement ?"</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="3">
                            <div class="answer-text">"Je vais d'abord lire toute la doc"</div>
                        </div>
                        <div class="answer" data-archetype="pragmatique" data-points="3">
                            <div class="answer-text">"Si ça marche et que c'est simple, ok"</div>
                        </div>
                    </div>
                </div>

                <!-- Question 7 -->
                <div class="question" data-section="2">
                    <h3>Ton objectif principal avec l'IA créative ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="explorateur" data-points="2">
                            <div class="answer-text">Maîtriser tous les outils tendance</div>
                        </div>
                        <div class="answer" data-archetype="stratege" data-points="2">
                            <div class="answer-text">Augmenter mon chiffre d'affaires</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="2">
                            <div class="answer-text">Développer mon style unique</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="2">
                            <div class="answer-text">Créer du contenu parfait</div>
                        </div>
                        <div class="answer" data-archetype="pragmatique" data-points="2">
                            <div class="answer-text">Gagner du temps au quotidien</div>
                        </div>
                    </div>
                </div>

                <!-- Question 8 -->
                <div class="question" data-section="2">
                    <h3>Qu'est-ce qui te freine le plus avec l'IA ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="perfectionniste" data-points="2">
                            <div class="answer-text">Peur de ne pas tout maîtriser</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="2">
                            <div class="answer-text">Crainte de perdre mon côté créatif</div>
                        </div>
                        <div class="answer" data-archetype="pragmatique" data-points="2">
                            <div class="answer-text">Trop d'outils, je m'y perds</div>
                        </div>
                        <div class="answer" data-archetype="stratege" data-points="2">
                            <div class="answer-text">Coût des abonnements</div>
                        </div>
                        <div class="answer" data-archetype="explorateur" data-points="2">
                            <div class="answer-text">Rien, j'y vais à fond !</div>
                        </div>
                    </div>
                </div>

                <!-- Question 9 -->
                <div class="question" data-section="2">
                    <h3>Si tu devais choisir UN super-pouvoir IA ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="pragmatique" data-points="3">
                            <div class="answer-text">Créer 10x plus vite</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="3">
                            <div class="answer-text">Des visuels impossibles à faire autrement</div>
                        </div>
                        <div class="answer" data-archetype="stratege" data-points="3">
                            <div class="answer-text">Automatiser tout mon workflow</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="3">
                            <div class="answer-text">Qualité studio à chaque fois</div>
                        </div>
                        <div class="answer" data-archetype="explorateur" data-points="3">
                            <div class="answer-text">Tester toutes les possibilités</div>
                        </div>
                    </div>
                </div>

                <!-- Question 10 -->
                <div class="question" data-section="2">
                    <h3>Comment vois-tu l'IA dans ton business ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="stratege" data-points="2">
                            <div class="answer-text">Un levier de croissance indispensable</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="2">
                            <div class="answer-text">Un pinceau numérique pour ma créativité</div>
                        </div>
                        <div class="answer" data-archetype="pragmatique" data-points="2">
                            <div class="answer-text">Un assistant qui me fait gagner du temps</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="2">
                            <div class="answer-text">Un moyen d'atteindre l'excellence</div>
                        </div>
                        <div class="answer" data-archetype="explorateur" data-points="2">
                            <div class="answer-text">Un terrain de jeu infini</div>
                        </div>
                    </div>
                </div>

                <!-- Section 3: Style d'Apprentissage -->
                <div class="section-header" style="display: none;">
                    <div class="section-title">📚 Section 3/4 : Ton Style d'Apprentissage</div>
                    <div class="section-subtitle">Comment tu assimiles le mieux</div>
                </div>

                <!-- Question 11 -->
                <div class="question" data-section="3">
                    <h3>Comment préfères-tu apprendre ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="explorateur" data-points="2">
                            <div class="answer-text">En testant directement</div>
                        </div>
                        <div class="answer" data-archetype="stratege" data-points="2">
                            <div class="answer-text">Études de cas et ROI</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="2">
                            <div class="answer-text">Exemples créatifs inspirants</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="2">
                            <div class="answer-text">Tutorials étape par étape</div>
                        </div>
                        <div class="answer" data-archetype="pragmatique" data-points="2">
                            <div class="answer-text">Méthodes simples et rapides</div>
                        </div>
                    </div>
                </div>

                <!-- Question 12 -->
                <div class="question" data-section="3">
                    <h3>Quand tu bloques sur un outil, tu fais quoi ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="perfectionniste" data-points="2">
                            <div class="answer-text">Je lis toute la documentation</div>
                        </div>
                        <div class="answer" data-archetype="explorateur" data-points="2">
                            <div class="answer-text">Je teste toutes les options</div>
                        </div>
                        <div class="answer" data-archetype="pragmatique" data-points="2">
                            <div class="answer-text">Je cherche un tuto rapide</div>
                        </div>
                        <div class="answer" data-archetype="stratege" data-points="2">
                            <div class="answer-text">Je demande à quelqu'un qui sait</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="2">
                            <div class="answer-text">Je contourne créativement</div>
                        </div>
                    </div>
                </div>

                <!-- Question 13 -->
                <div class="question" data-section="3">
                    <h3>Ton format préféré pour apprendre ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="pragmatique" data-points="2">
                            <div class="answer-text">Vidéos courtes et pratiques</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="2">
                            <div class="answer-text">Formations complètes structurées</div>
                        </div>
                        <div class="answer" data-archetype="explorateur" data-points="2">
                            <div class="answer-text">Lives interactifs avec Q&A</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="2">
                            <div class="answer-text">Exemples visuels et inspiration</div>
                        </div>
                        <div class="answer" data-archetype="stratege" data-points="2">
                            <div class="answer-text">Templates et frameworks prêts</div>
                        </div>
                    </div>
                </div>

                <!-- Question 14 -->
                <div class="question" data-section="3">
                    <h3>À quelle vitesse intègres-tu de nouveaux outils ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="explorateur" data-points="3">
                            <div class="answer-text">Ultra rapide, je suis early adopter</div>
                        </div>
                        <div class="answer" data-archetype="pragmatique" data-points="2">
                            <div class="answer-text">Rapide si c'est simple</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="2">
                            <div class="answer-text">Lentement mais sûrement</div>
                        </div>
                        <div class="answer" data-archetype="stratege" data-points="2">
                            <div class="answer-text">Selon le ROI potentiel</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="2">
                            <div class="answer-text">Si ça m'inspire, très vite</div>
                        </div>
                    </div>
                </div>

                <!-- Question 15 -->
                <div class="question" data-section="3">
                    <h3>Qu'est-ce qui te motive le plus à apprendre ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="stratege" data-points="3">
                            <div class="answer-text">Les résultats business concrets</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="3">
                            <div class="answer-text">Les possibilités créatives infinies</div>
                        </div>
                        <div class="answer" data-archetype="pragmatique" data-points="3">
                            <div class="answer-text">Le gain de temps au quotidien</div>
                        </div>
                        <div class="answer" data-archetype="explorateur" data-points="3">
                            <div class="answer-text">La découverte de nouveautés</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="3">
                            <div class="answer-text">La maîtrise complète du sujet</div>
                        </div>
                    </div>
                </div>

                <!-- Section 4: Vision Future -->
                <div class="section-header" style="display: none;">
                    <div class="section-title">🚀 Section 4/4 : Ta Vision Future</div>
                    <div class="section-subtitle">Où tu veux être dans 6 mois</div>
                </div>

                <!-- Question 16 -->
                <div class="question" data-section="4">
                    <h3>Dans 6 mois, tu te vois comment avec l'IA ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="stratege" data-points="2">
                            <div class="answer-text">Business automatisé et scalable</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="2">
                            <div class="answer-text">Style unique reconnaissable</div>
                        </div>
                        <div class="answer" data-archetype="pragmatique" data-points="2">
                            <div class="answer-text">Plus de temps libre grâce à l'IA</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="2">
                            <div class="answer-text">Expert reconnu en IA créative</div>
                        </div>
                        <div class="answer" data-archetype="explorateur" data-points="2">
                            <div class="answer-text">À la pointe de toutes les nouveautés</div>
                        </div>
                    </div>
                </div>

                <!-- Question 17 -->
                <div class="question" data-section="4">
                    <h3>Ton plus grand rêve créatif avec l'IA ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="artiste" data-points="3">
                            <div class="answer-text">Créer des œuvres impossibles autrement</div>
                        </div>
                        <div class="answer" data-archetype="stratege" data-points="3">
                            <div class="answer-text">Avoir une équipe d'IA qui travaille pour moi</div>
                        </div>
                        <div class="answer" data-archetype="pragmatique" data-points="3">
                            <div class="answer-text">Ne plus jamais manquer de contenu</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="3">
                            <div class="answer-text">Qualité irréprochable à chaque fois</div>
                        </div>
                        <div class="answer" data-archetype="explorateur" data-points="3">
                            <div class="answer-text">Inventer de nouvelles utilisations</div>
                        </div>
                    </div>
                </div>

                <!-- Question 18 -->
                <div class="question" data-section="4">
                    <h3>Qu'est-ce qui te ferait dire "J'ai réussi" ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="stratege" data-points="2">
                            <div class="answer-text">ROI multiplié par 10</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="2">
                            <div class="answer-text">Ma créativité décuplée</div>
                        </div>
                        <div class="answer" data-archetype="pragmatique" data-points="2">
                            <div class="answer-text">Workflow simplifié et efficace</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="2">
                            <div class="answer-text">Maîtrise totale de tous les outils</div>
                        </div>
                        <div class="answer" data-archetype="explorateur" data-points="2">
                            <div class="answer-text">Toujours en avance sur les tendances</div>
                        </div>
                    </div>
                </div>

                <!-- Question 19 -->
                <div class="question" data-section="4">
                    <h3>Quel serait ton avatar IA idéal ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="perfectionniste" data-points="2">
                            <div class="answer-text">Indistinguable d'une vraie photo</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="2">
                            <div class="answer-text">Artistique et unique</div>
                        </div>
                        <div class="answer" data-archetype="pragmatique" data-points="2">
                            <div class="answer-text">Simple mais efficace</div>
                        </div>
                        <div class="answer" data-archetype="stratege" data-points="2">
                            <div class="answer-text">Professionnel et versatile</div>
                        </div>
                        <div class="answer" data-archetype="explorateur" data-points="2">
                            <div class="answer-text">Futuriste et innovant</div>
                        </div>
                    </div>
                </div>

                <!-- Question 20 -->
                <div class="question" data-section="4">
                    <h3>Si tu devais choisir UN module prioritaire ?</h3>
                    <div class="answers">
                        <div class="answer" data-archetype="pragmatique" data-points="3">
                            <div class="answer-text">Module 1 : Les bases solides</div>
                        </div>
                        <div class="answer" data-archetype="artiste" data-points="3">
                            <div class="answer-text">Module 2 : Avatar créatif</div>
                        </div>
                        <div class="answer" data-archetype="perfectionniste" data-points="3">
                            <div class="answer-text">Module 3 : Animation pro</div>
                        </div>
                        <div class="answer" data-archetype="explorateur" data-points="3">
                            <div class="answer-text">Module 4 : Outils custom</div>
                        </div>
                        <div class="answer" data-archetype="stratege" data-points="3">
                            <div class="answer-text">Module 5 : Studio complet</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Navigation -->
            <div class="navigation">
                <button class="btn btn-secondary" id="prevBtn" onclick="previousQuestion()" style="visibility: hidden;">Précédent</button>
                <div class="question-counter">
                    Question <span id="currentQuestionNav">1</span> / 20
                </div>
                <button class="btn btn-primary" id="nextBtn" onclick="nextQuestion()" disabled>Suivant</button>
            </div>
        </div>

        <!-- Results Container -->
        <div class="results-container" id="resultsContainer">
            <div class="results-header">
                <div class="archetype-badge" id="archetypeBadge">🚀</div>
                <div class="results-title">Ton Profil Créateur IA</div>
                <div class="archetype-name" id="archetypeName">Explorateur Digital</div>
                <div class="archetype-score" id="archetypeScore">Score : 15/15 points</div>
            </div>
            
            <div class="results-content">
                <div class="result-section">
                    <h4>🎯 Tes Super-Pouvoirs</h4>
                    <ul class="strengths" id="strengths">
                        <li>Adaptabilité et ouverture d'esprit</li>
                        <li>Curiosité naturelle pour les nouveautés</li>
                        <li>Capacité d'apprentissage rapide</li>
                    </ul>
                </div>
                
                <div class="result-section">
                    <h4>⚠️ Tes Défis à Relever</h4>
                    <ul class="challenges" id="challenges">
                        <li>Tendance à se disperser entre trop d'outils</li>
                        <li>Besoin de structurer ton approche</li>
                    </ul>
                </div>
                
                <div class="result-section">
                    <h4>💡 Conseils Pour Maximiser Ton Potentiel</h4>
                    <div id="personalTips">
                        <p>Des conseils adaptés à ton profil pour tirer le meilleur de la formation</p>
                    </div>
                </div>
                
                <div class="cta-section">
                    <div class="cta-title">🚀 Félicitations !</div>
                    <p style="margin-bottom: 20px;">Tu connais maintenant ton profil créateur IA ! Utilise ces insights pour maximiser ton potentiel avec l'intelligence artificielle.</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Quiz Logic
        let currentQuestionIndex = 0;
        let scores = {
            explorateur: 0,
            stratege: 0,
            artiste: 0,
            perfectionniste: 0,
            pragmatique: 0
        };
        
        const questions = document.querySelectorAll('.question');
        const totalQuestions = questions.length;
        
        // Archetype definitions
        const archetypes = {
            explorateur: {
                name: "Explorateur Digital",
                badge: "🚀",
                strengths: [
                    "Adaptabilité et ouverture d'esprit exceptionnelles",
                    "Curiosité naturelle qui te pousse toujours plus loin",
                    "Capacité d'apprentissage ultra-rapide",
                    "Early adopter qui voit les tendances avant tout le monde"
                ],
                challenges: [
                    "Tendance à te disperser entre trop d'outils",
                    "Besoin de structurer ton approche pour maximiser l'impact",
                    "Risque de ne pas approfondir assez chaque outil"
                ],
                tips: `
                    <p><strong>💡 Pour toi, explorateur :</strong></p>
                    <p>• Dans le Module 2, tu vas adorer découvrir les 3 IA principales (ChatGPT, Claude, GenSpark). Mais attention : force-toi à maîtriser chaque IA avant de passer à la suivante !</p>
                    <p>• Ton défi : Utilise chaque IA pendant au moins 1 semaine avant d'en tester une nouvelle.</p>
                    <p>• Astuce : Tiens un journal de tes découvertes pour ne pas oublier les pépites que tu trouves.</p>
                `
            },
            stratege: {
                name: "Stratège Efficace",
                badge: "🎯",
                strengths: [
                    "Vision business claire et orientée résultats",
                    "Capacité d'optimisation et d'organisation redoutable",
                    "Focus laser sur le ROI et l'impact mesurable",
                    "Talent pour transformer l'IA en machine à cash"
                ],
                challenges: [
                    "Peut négliger la créativité pour la productivité",
                    "Impatience si les résultats ne sont pas immédiats",
                    "Tendance à sous-estimer l'importance de l'esthétique"
                ],
                tips: `
                    <p><strong>💡 Pour toi, stratège :</strong></p>
                    <p>• Le Module 2 est parfait pour toi : tu vas apprendre à orchestrer ChatGPT, Claude et GenSpark comme une vraie équipe qui travaille pour toi 24/7.</p>
                    <p>• Focus sur l'automatisation : chaque IA a sa spécialité, utilise-les stratégiquement.</p>
                    <p>• ROI immédiat : Tu vas gagner minimum 2h par jour dès la première semaine.</p>
                `
            },
            artiste: {
                name: "Artiste Augmenté",
                badge: "🎨",
                strengths: [
                    "Sens esthétique et créativité naturelle extraordinaires",
                    "Capacité unique à émouvoir et inspirer",
                    "Vision artistique qui te démarque de la masse",
                    "Intuition créative que l'IA va décupler"
                ],
                challenges: [
                    "Peut être réticent à l'aspect technique de l'IA",
                    "Perfectionnisme qui peut ralentir la production",
                    "Peur que l'IA uniformise ta créativité unique"
                ],
                tips: `
                    <p><strong>💡 Pour toi, artiste :</strong></p>
                    <p>• Le Module 2 te montre comment ChatGPT devient ton assistant créatif, Claude ton conseiller stratégique, et GenSpark ton veilleur d'inspiration.</p>
                    <p>• Ne vois pas ces IA comme des robots mais comme des muses digitales qui nourrissent ta créativité.</p>
                    <p>• Challenge : Utilise ChatGPT pour générer 20 idées créatives par jour pendant une semaine.</p>
                `
            },
            perfectionniste: {
                name: "Perfectionniste Technique",
                badge: "🔧",
                strengths: [
                    "Qualité irréprochable dans chaque création",
                    "Maîtrise technique qui impressionne",
                    "Attention aux détails qui fait la différence",
                    "Capacité à exploiter 100% du potentiel des outils"
                ],
                challenges: [
                    "Peut se perdre dans les détails techniques",
                    "Perfectionnisme parfois paralysant",
                    "Difficulté à publier si ce n'est pas 'parfait'"
                ],
                tips: `
                    <p><strong>💡 Pour toi, perfectionniste :</strong></p>
                    <p>• Le Module 2 va satisfaire ton besoin de maîtrise : tu vas comprendre TOUTES les subtilités de ChatGPT, Claude et GenSpark.</p>
                    <p>• Ma méthode P.R.O.M.P.T.™ est faite pour toi : structure parfaite pour des résultats parfaits.</p>
                    <p>• Rappel : Mieux vaut utiliser une IA à 80% tous les jours qu'à 100% jamais !</p>
                `
            },
            pragmatique: {
                name: "Pragmatique Pressé",
                badge: "⚡",
                strengths: [
                    "Action immédiate et résultats rapides",
                    "Focus sur l'essentiel sans fioritures",
                    "Adaptation éclair aux nouvelles méthodes",
                    "Efficacité redoutable dans l'exécution"
                ],
                challenges: [
                    "Peut brûler des étapes importantes",
                    "Impatience face aux concepts théoriques",
                    "Risque de passer à côté de fonctions puissantes"
                ],
                tips: `
                    <p><strong>💡 Pour toi, pragmatique :</strong></p>
                    <p>• Module 2 = gains rapides ! Tu vas directement aux techniques qui fonctionnent avec ChatGPT, Claude et GenSpark.</p>
                    <p>• Focus sur les prompts prêts à l'emploi et les workflows qui te font gagner du temps immédiatement.</p>
                    <p>• En 1 semaine, tu auras automatisé 50% de tes tâches répétitives. C'est ça l'efficacité !</p>
                `
            }
        };
        
        // Sections tracking
        let currentSection = 1;
        const sections = {
            1: { start: 0, end: 4, header: "🎨 Section 1/4 : Ton Profil Créatif Actuel" },
            2: { start: 5, end: 9, header: "🧠 Section 2/4 : Ton Mindset IA" },
            3: { start: 10, end: 14, header: "📚 Section 3/4 : Ton Style d'Apprentissage" },
            4: { start: 15, end: 19, header: "🚀 Section 4/4 : Ta Vision Future" }
        };
        
        // Answer selection
        document.addEventListener('click', function(e) {
            if (e.target.closest('.answer')) {
                const answer = e.target.closest('.answer');
                const question = answer.closest('.question');
                
                // Remove previous selection
                question.querySelectorAll('.answer').forEach(a => a.classList.remove('selected'));
                
                // Add selection
                answer.classList.add('selected');
                
                // Enable next button
                document.getElementById('nextBtn').disabled = false;
            }
        });
        
        function updateProgress() {
            const progress = ((currentQuestionIndex + 1) / totalQuestions) * 100;
            document.getElementById('progressBar').style.width = progress + '%';
            document.getElementById('currentQuestion').textContent = currentQuestionIndex + 1;
            document.getElementById('currentQuestionNav').textContent = currentQuestionIndex + 1;
        }
        
        function updateSectionHeader() {
            // Determine current section
            for (const [sectionNum, sectionData] of Object.entries(sections)) {
                if (currentQuestionIndex >= sectionData.start && currentQuestionIndex <= sectionData.end) {
                    if (parseInt(sectionNum) !== currentSection) {
                        currentSection = parseInt(sectionNum);
                        // Update all section headers
                        document.querySelectorAll('.section-header').forEach((header, index) => {
                            if (index === currentSection - 1) {
                                header.style.display = 'block';
                                header.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                            } else {
                                header.style.display = 'none';
                            }
                        });
                    }
                    break;
                }
            }
        }
        
        function nextQuestion() {
            const currentQuestion = questions[currentQuestionIndex];
            const selectedAnswer = currentQuestion.querySelector('.answer.selected');
            
            if (!selectedAnswer && currentQuestionIndex < totalQuestions - 1) {
                alert('Veuillez sélectionner une réponse');
                return;
            }
            
            // Save answer
            if (selectedAnswer) {
                const archetype = selectedAnswer.dataset.archetype;
                const points = parseInt(selectedAnswer.dataset.points);
                scores[archetype] += points;
            }
            
            if (currentQuestionIndex < totalQuestions - 1) {
                // Hide current question
                currentQuestion.classList.remove('active');
                
                // Show next question
                currentQuestionIndex++;
                questions[currentQuestionIndex].classList.add('active');
                
                updateProgress();
                updateNavigation();
                updateSectionHeader();
                
                // Reset next button
                document.getElementById('nextBtn').disabled = true;
                
                // Scroll to top of quiz container
                document.getElementById('quizContainer').scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                // Show results
                showResults();
            }
        }
        
        function previousQuestion() {
            if (currentQuestionIndex > 0) {
                questions[currentQuestionIndex].classList.remove('active');
                currentQuestionIndex--;
                questions[currentQuestionIndex].classList.add('active');
                
                updateProgress();
                updateNavigation();
                updateSectionHeader();
                
                // Check if answer is already selected
                const currentQuestion = questions[currentQuestionIndex];
                const selectedAnswer = currentQuestion.querySelector('.answer.selected');
                document.getElementById('nextBtn').disabled = !selectedAnswer;
            }
        }
        
        function updateNavigation() {
            const prevBtn = document.getElementById('prevBtn');
            const nextBtn = document.getElementById('nextBtn');
            
            if (currentQuestionIndex === 0) {
                prevBtn.style.visibility = 'hidden';
            } else {
                prevBtn.style.visibility = 'visible';
            }
            
            if (currentQuestionIndex === totalQuestions - 1) {
                nextBtn.textContent = 'Voir mes résultats';
            } else {
                nextBtn.textContent = 'Suivant';
            }
            
            // Check if answer is selected
            const currentQuestion = questions[currentQuestionIndex];
            const selectedAnswer = currentQuestion.querySelector('.answer.selected');
            nextBtn.disabled = !selectedAnswer;
        }
        
        function calculateSecondaryArchetype(scores, dominantArchetype) {
            let secondHighest = 0;
            let secondaryArchetype = null;
            
            for (const [archetype, score] of Object.entries(scores)) {
                if (archetype !== dominantArchetype && score > secondHighest) {
                    secondHighest = score;
                    secondaryArchetype = archetype;
                }
            }
            
            return { archetype: secondaryArchetype, score: secondHighest };
        }
        
        function showResults() {
            // Calculate dominant archetype
            let maxScore = 0;
            let dominantArchetype = 'explorateur';
            
            for (const [archetype, score] of Object.entries(scores)) {
                if (score > maxScore) {
                    maxScore = score;
                    dominantArchetype = archetype;
                }
            }
            
            // Calculate secondary archetype
            const secondary = calculateSecondaryArchetype(scores, dominantArchetype);
            
            const result = archetypes[dominantArchetype];
            
            // Update UI
            document.getElementById('archetypeBadge').textContent = result.badge;
            document.getElementById('archetypeName').textContent = result.name;
            
            // Show both primary and secondary scores
            let scoreText = `Score principal : ${maxScore}/${totalQuestions * 3} points`;
            if (secondary.score > 0) {
                const secondaryName = archetypes[secondary.archetype].name;
                scoreText += `\nProfil secondaire : ${secondaryName} (${secondary.score} points)`;
            }
            document.getElementById('archetypeScore').innerHTML = scoreText.replace('\n', '<br>');
            
            // Update strengths
            const strengthsList = document.getElementById('strengths');
            strengthsList.innerHTML = '';
            result.strengths.forEach(strength => {
                const li = document.createElement('li');
                li.textContent = strength;
                strengthsList.appendChild(li);
            });
            
            // Update challenges
            const challengesList = document.getElementById('challenges');
            challengesList.innerHTML = '';
            result.challenges.forEach(challenge => {
                const li = document.createElement('li');
                li.textContent = challenge;
                challengesList.appendChild(li);
            });
            
            // Update personal tips
            document.getElementById('personalTips').innerHTML = result.tips;
            
            // Show results
            document.getElementById('quizContainer').style.display = 'none';
            document.getElementById('resultsContainer').style.display = 'block';
            
            // Hide progress bar
            document.querySelector('.progress-container').style.display = 'none';
            
            // Scroll to top
            window.scrollTo(0, 0);
            
            // Log scores for debugging
            console.log('Scores finaux:', scores);
            console.log('Profil dominant:', dominantArchetype, 'avec', maxScore, 'points');
            if (secondary.archetype) {
                console.log('Profil secondaire:', secondary.archetype, 'avec', secondary.score, 'points');
            }
        }
        
        // Initialize
        updateProgress();
        updateNavigation();
        updateSectionHeader();
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
        "title": "Diagnostic créateur IA",
        "description": "Découvre ton profil de créateur IA et obtiens ton plan d'action personnalisé avec ce quiz interactif de 20 questions",
        "category": "Diagnostic",
        "html_content": DIAGNOSTIC_TOOL_HTML,
        "preview_image": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400&h=240&fit=crop&q=80"
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
        print("🧠 Creating AI Creator Diagnostic tool...")
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
            diagnostic_tools = [t for t in tools if "Diagnostic" in t['title']]
            print(f"✅ Verification successful! Found {len(diagnostic_tools)} diagnostic tool(s)")
            for tool in diagnostic_tools:
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