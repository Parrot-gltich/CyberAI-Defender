import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from data.sample_data import create_phishing_dataset

def run_exercise1():
    print("\n" + "=" * 60)
    print("EXERCICE 1: DÉTECTION DE PHISHING PAR ANALYSE DE TEXTE")
    print("=" * 60)
    
    # Étape 1.1 : Création du dataset
    print("\n--- Étape 1.1 : Création du dataset ---")
    df = create_phishing_dataset()
    
    print("Aperçu du dataset :")
    print(df.head())
    
    print("\nDistribution des classes :")
    distribution = df['label'].value_counts()
    print(distribution)
    
    # Question 1.1
    print(f"\n📊 QUESTION 1.1:")
    print(f"Le dataset contient {distribution[1]} emails de phishing et {distribution[0]} emails légitimes.")
    print("Cette distribution est équilibrée." if distribution[0] == distribution[1] else "Cette distribution n'est pas équilibrée.")
    
    # Étape 1.2 : Prétraitement et vectorisation
    print("\n--- Étape 1.2 : Prétraitement et vectorisation ---")
    
    X = df['text']
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Taille de l'ensemble d'entraînement : {len(X_train)}")
    print(f"Taille de l'ensemble de test : {len(X_test)}")
    
    vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"Dimensions de la matrice TF-IDF : {X_train_tfidf.shape}")
    
    # Question 1.2
    print(f"\n📊 QUESTION 1.2:")
    print("max_features=100 limite le nombre de mots (features) à 100 les plus fréquents.")
    print("fit_transform sur l'entraînement pour apprendre le vocabulaire et transformer les données.")
    print("transform sur le test pour utiliser le même vocabulaire sans réapprentissage.")
    
    # Étape 1.3 : Entraînement du modèle
    print("\n--- Étape 1.3 : Entraînement du modèle ---")
    
    model = MultinomialNB()
    model.fit(X_train_tfidf, y_train)
    print("✔ Modèle Naive Bayes entraîné avec succès !")
    
    # Étape 1.4 : Évaluation du modèle
    print("\n--- Étape 1.4 : Évaluation du modèle ---")
    
    y_pred = model.predict(X_test_tfidf)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy : {accuracy:.2%}")
    
    print("\nRapport de classification :")
    print(classification_report(y_test, y_pred, target_names=['Légitime', 'Phishing']))
    
    # Matrice de confusion
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Légitime', 'Phishing'],
                yticklabels=['Légitime', 'Phishing'])
    plt.title('Matrice de confusion - Détection de phishing')
    plt.ylabel('Vraie classe')
    plt.xlabel('Classe prédite')
    plt.tight_layout()
    plt.savefig('results/confusion_matrix_phishing.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\n✓ Matrice de confusion sauvegardée dans 'results/confusion_matrix_phishing.png'")
    
    # Question 1.3
    print(f"\n📊 QUESTION 1.3:")
    print("Précision: capacité à ne pas classer comme positif un échantillon négatif")
    print("Recall: capacité à trouver tous les échantillons positifs")
    print("F1-Score: moyenne harmonique de précision et recall")
    print("Dans le contexte phishing, le recall est crucial pour ne pas manquer d'attaques.")
    
    # Étape 1.5 : Test sur nouveaux emails
    print("\n--- Étape 1.5 : Test sur nouveaux emails ---")
    
    nouveaux_emails = [
        "Your Amazon order has been shipped. Track your package here.",
        "URGENT! Your account has been locked. Verify now to unlock!",
        "Meeting rescheduled to Thursday at 3 PM. Please update your calendar."
    ]
    
    nouveaux_emails_tfidf = vectorizer.transform(nouveaux_emails)
    predictions = model.predict(nouveaux_emails_tfidf)
    
    print("\nRésultats de classification :")
    for email, pred in zip(nouveaux_emails, predictions):
        label = "🔍 PHISHING" if pred == 1 else "✓ LÉGITIME"
        print(f"\n{label}")
        print(f"Email : {email}")
    
    print(f"\n📊 Analyse des prédictions:")
    print("Le modèle peut faire des erreurs sur des emails ambigus.")
    print("Les faux négatifs (phishing non détecté) sont les plus dangereux.")
