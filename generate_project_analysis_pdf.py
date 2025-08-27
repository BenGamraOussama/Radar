#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

def create_project_analysis_pdf():
    # Configuration du document
    filename = "Analyse_Projet_IA_Classification.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Style personnalisé pour le titre
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    # Style pour les sous-titres
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkgreen
    )
    
    # Style pour le texte normal
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY
    )
    
    # Style pour les listes
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        leftIndent=20,
        bulletIndent=10
    )
    
    # Contenu du document
    story = []
    
    # Titre principal
    story.append(Paragraph("🎯 ANALYSE DU PROJET", title_style))
    story.append(Paragraph("Système de Classification IA pour Données CAN", title_style))
    story.append(Spacer(1, 20))
    
    # Date et informations générales
    story.append(Paragraph(f"<b>Date d'analyse:</b> {datetime.now().strftime('%d/%m/%Y')}", normal_style))
    story.append(Paragraph("<b>Type de projet:</b> Intelligence Artificielle - Machine Learning", normal_style))
    story.append(Spacer(1, 20))
    
    # Objectif Principal
    story.append(Paragraph("🎯 OBJECTIF PRINCIPAL", subtitle_style))
    story.append(Paragraph(
        "Ce projet est un <b>système de classification basé sur l'intelligence artificielle</b> "
        "pour analyser et prédire des classes à partir de données CAN (Controller Area Network) - "
        "typiquement utilisées dans les systèmes automobiles ou industriels.",
        normal_style
    ))
    story.append(Spacer(1, 15))
    
    # Composants du Projet
    story.append(Paragraph("📋 COMPOSANTS DU PROJET", subtitle_style))
    
    # 1. Analyse et Comparaison
    story.append(Paragraph("<b>1. Analyse et Comparaison de Modèles IA</b>", normal_style))
    story.append(Paragraph("• Notebook Jupyter (IA_Model_Comparison.ipynb) pour comparer différents algorithmes", bullet_style))
    story.append(Paragraph("• Utilisation de Random Forest et XGBoost pour la classification", bullet_style))
    story.append(Paragraph("• Optimisation des hyperparamètres avec des outils comme Optuna", bullet_style))
    story.append(Spacer(1, 10))
    
    # 2. API Web
    story.append(Paragraph("<b>2. API Web de Prédiction</b>", normal_style))
    story.append(Paragraph("• Application Flask (app.py) qui expose une API REST", bullet_style))
    story.append(Paragraph("• Interface web (client.html) pour tester les prédictions en temps réel", bullet_style))
    story.append(Paragraph("• Endpoint /predict qui accepte 8 valeurs numériques (D0 à D7)", bullet_style))
    story.append(Spacer(1, 10))
    
    # 3. Pipeline de Données
    story.append(Paragraph("<b>3. Pipeline de Données</b>", normal_style))
    story.append(Paragraph("• Prétraitement des données hexadécimales CAN (conversion en entiers)", bullet_style))
    story.append(Paragraph("• Normalisation avec StandardScaler", bullet_style))
    story.append(Paragraph("• Gestion des valeurs manquantes", bullet_style))
    story.append(Spacer(1, 10))
    
    # 4. Modèles Entraînés
    story.append(Paragraph("<b>4. Modèles Entraînés</b>", normal_style))
    story.append(Paragraph("• Modèle XGBoost optimisé (xgb_optimized.pkl)", bullet_style))
    story.append(Paragraph("• Modèle Random Forest (random_forest_model.pkl)", bullet_style))
    story.append(Paragraph("• Scaler pré-entraîné pour la normalisation", bullet_style))
    story.append(Spacer(1, 15))
    
    # Fonctionnalités
    story.append(Paragraph("🔧 FONCTIONNALITÉS", subtitle_style))
    story.append(Paragraph("• <b>Prédiction en temps réel:</b> Interface web pour saisir des données et obtenir des prédictions", bullet_style))
    story.append(Paragraph("• <b>API REST:</b> Service web pour intégrer les prédictions dans d'autres applications", bullet_style))
    story.append(Paragraph("• <b>Script de prédiction:</b> Outil en ligne de commande pour traiter des fichiers CSV", bullet_style))
    story.append(Paragraph("• <b>Tests:</b> Validation des fonctionnalités de l'API", bullet_style))
    story.append(Spacer(1, 15))
    
    # Cas d'Usage
    story.append(Paragraph("💡 CAS D'USAGE PROBABLE", subtitle_style))
    story.append(Paragraph("Ce projet semble être conçu pour:", normal_style))
    story.append(Paragraph("• <b>Détection d'anomalies</b> dans les réseaux CAN", bullet_style))
    story.append(Paragraph("• <b>Classification de messages</b> automobiles ou industriels", bullet_style))
    story.append(Paragraph("• <b>Surveillance en temps réel</b> de systèmes embarqués", bullet_style))
    story.append(Paragraph("• <b>Analyse prédictive</b> de données IoT ou véhiculaires", bullet_style))
    story.append(Spacer(1, 15))
    
    # Architecture Technique
    story.append(Paragraph("🏗️ ARCHITECTURE TECHNIQUE", subtitle_style))
    
    # Tableau des fichiers principaux
    data = [
        ['Fichier', 'Description', 'Technologie'],
        ['app.py', 'API Flask principale', 'Python/Flask'],
        ['client.html', 'Interface utilisateur web', 'HTML/CSS/JavaScript'],
        ['predict.py', 'Script de prédiction CLI', 'Python'],
        ['IA_Model_Comparison.ipynb', 'Notebook d\'analyse', 'Jupyter/Python'],
        ['models/xgb_optimized.pkl', 'Modèle XGBoost entraîné', 'Pickle/Scikit-learn'],
        ['models/scaler.pkl', 'Normalisateur de données', 'Pickle/Scikit-learn'],
        ['requirements.txt', 'Dépendances Python', 'pip']
    ]
    
    table = Table(data, colWidths=[2.5*inch, 2.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 15))
    
    # Technologies Utilisées
    story.append(Paragraph("⚙️ TECHNOLOGIES UTILISÉES", subtitle_style))
    story.append(Paragraph("• <b>Backend:</b> Flask, Python", bullet_style))
    story.append(Paragraph("• <b>Machine Learning:</b> Scikit-learn, XGBoost, Pandas, NumPy", bullet_style))
    story.append(Paragraph("• <b>Visualisation:</b> Matplotlib, Seaborn", bullet_style))
    story.append(Paragraph("• <b>Optimisation:</b> Optuna, GridSearchCV", bullet_style))
    story.append(Paragraph("• <b>Frontend:</b> HTML, CSS, JavaScript", bullet_style))
    story.append(Paragraph("• <b>Validation:</b> Pydantic", bullet_style))
    story.append(Spacer(1, 15))
    
    # Conclusion
    story.append(Paragraph("📝 CONCLUSION", subtitle_style))
    story.append(Paragraph(
        "Ce projet combine <b>recherche</b> (notebook), <b>développement</b> (API) et "
        "<b>déploiement</b> (interface web) dans un workflow complet de machine learning. "
        "Il représente une solution complète pour la classification automatisée de données "
        "CAN avec une approche moderne et des outils de pointe en intelligence artificielle.",
        normal_style
    ))
    
    # Construction du PDF
    doc.build(story)
    return filename

if __name__ == "__main__":
    try:
        pdf_file = create_project_analysis_pdf()
        print(f"✅ PDF généré avec succès: {pdf_file}")
        print(f"📁 Emplacement: {os.path.abspath(pdf_file)}")
    except Exception as e:
        print(f"❌ Erreur lors de la génération du PDF: {e}")
        print("💡 Assurez-vous d'avoir installé reportlab: pip install reportlab")
