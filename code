#!/usr/bin/env python3
"""
TP : Intelligence Artificielle et Cybersécurité
Programme principal unifié regroupant les 3 exercices
"""

import warnings
warnings.filterwarnings('ignore')

from exercises.exercise1_phishing import run_exercise1
from exercises.exercise2_anomalies import run_exercise2
from exercises.exercise3_malware import run_exercise3

def main():
    print("=" * 70)
    print("TP : INTELLIGENCE ARTIFICIELLE ET CYBERSÉCURITÉ")
    print("=" * 70)
    
    while True:
        print("\n" + "=" * 50)
        print("MENU PRINCIPAL")
        print("=" * 50)
        print("1. Exercice 1 - Détection de phishing par analyse de texte")
        print("2. Exercice 2 - Analyse de logs et détection d'anomalies")
        print("3. Exercice 3 - Classification de malware")
        print("4. Exécuter tous les exercices")
        print("5. Quitter")
        
        choix = input("\nChoisissez une option (1-5): ").strip()
        
        if choix == "1":
            run_exercise1()
        elif choix == "2":
            run_exercise2()
        elif choix == "3":
            run_exercise3()
        elif choix == "4":
            print("\n" + "=" * 50)
            print("EXÉCUTION DE TOUS LES EXERCICES")
            print("=" * 50)
            run_exercise1()
            run_exercise2()
            run_exercise3()
        elif choix == "5":
            print("\nMerci d'avoir utilisé ce programme !")
            break
        else:
            print("Option invalide. Veuillez choisir entre 1 et 5.")

if __name__ == "__main__":
    main()
