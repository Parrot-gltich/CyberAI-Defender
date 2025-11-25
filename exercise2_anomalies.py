import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns
from data.sample_data import create_logs_dataset

def run_exercise2():
    print("\n" + "=" * 60)
    print("EXERCICE 2: ANALYSE DE LOGS ET DÉTECTION D'ANOMALIES")
    print("=" * 60)
    
    # Étape 2.1 : Création du dataset
    print("\n--- Étape 2.1 : Création du dataset ---")
    df_logs = create_logs_dataset()
    
    print("Aperçu des logs :")
    print(df_logs.head(10))
    
    print("\nStatistiques descriptives :")
    print(df_logs[['port_dest', 'bytes_sent', 'requests_per_min']].describe())
    
    # Question 2.1
    print(f"\n📊 QUESTION 2.1:")
    print("Caractéristiques indicatrices d'anomalies:")
    print("- Bytes envoyés anormalement élevés")
    print("- Nombre de requêtes par minute très élevé")
    print("- Ports de destination inhabituels (22, 3389, 445)")
    
    # Étape 2.2 : Feature engineering
    print("\n--- Étape 2.2 : Feature engineering ---")
    
    le_ip = LabelEncoder()
    df_logs['ip_encoded'] = le_ip.fit_transform(df_logs['ip_source'])
    
    df_logs['hour'] = df_logs['timestamp'].dt.hour
    df_logs['minute'] = df_logs['timestamp'].dt.minute
    
    features = ['ip_encoded', 'port_dest', 'bytes_sent', 'requests_per_min', 'hour']
    X_logs = df_logs[features]
    
    print("Features sélectionnées :")
    print(X_logs.head())
    
    # Étape 2.3 : Détection d'anomalies
    print("\n--- Étape 2.3 : Détection d'anomalies ---")
    
    iso_forest = IsolationForest(
        contamination=0.1,
        random_state=42
    )
    
    df_logs['anomaly'] = iso_forest.fit_predict(X_logs)
    df_logs['is_anomaly'] = (df_logs['anomaly'] == -1).astype(int)
    
    n_anomalies_detected = df_logs['is_anomaly'].sum()
    print(f"\nNombre d'anomalies détectées : {n_anomalies_detected}")
    print(f"Pourcentage d'anomalies : {n_anomalies_detected / len(df_logs) * 100:.1f}%")
    
    print("\nLogs suspects détectés :")
    print(df_logs[df_logs['is_anomaly'] == 1][['timestamp', 'ip_source', 'port_dest', 'bytes_sent', 'requests_per_min']])
    
    # Question 2.2
    print(f"\n📊 QUESTION 2.2:")
    print("contamination=0.1 signifie qu'on s'attend à 10% d'anomalies.")
    print("En contexte réel, on peut l'estimer via l'analyse historique ou le domaine métier.")
    
    # Étape 2.4 : Visualisation
    print("\n--- Étape 2.4 : Visualisation des anomalies ---")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Graphique 1
    axes[0, 0].scatter(
        df_logs[df_logs['is_anomaly'] == 0]['bytes_sent'],
        df_logs[df_logs['is_anomaly'] == 0]['requests_per_min'],
        c='blue', label='Normal', alpha=0.6, s=50
    )
    axes[0, 0].scatter(
        df_logs[df_logs['is_anomaly'] == 1]['bytes_sent'],
        df_logs[df_logs['is_anomaly'] == 1]['requests_per_min'],
        c='red', label='Anomalie', alpha=0.8, s=100, marker='X'
    )
    axes[0, 0].set_xlabel('Bytes envoyés')
    axes[0, 0].set_ylabel('Requêtes par minute')
    axes[0, 0].set_title('Détection d\'Anomalies : Volume vs Fréquence')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Graphique 2
    port_counts = df_logs.groupby(['port_dest', 'is_anomaly']).size().unstack(fill_value=0)
    port_counts.plot(kind='bar', ax=axes[0, 1], color=['blue', 'red'])
    axes[0, 1].set_xlabel('Port de destination')
    axes[0, 1].set_ylabel('Nombre de connexions')
    axes[0, 1].set_title('Distribution des ports (Normal vs Anomalie)')
    axes[0, 1].legend(['Normal', 'Anomalie'])
    axes[0, 1].tick_params(axis='x', rotation=0)
    
    # Graphique 3
    df_logs_sorted = df_logs.sort_values('timestamp')
    axes[1, 0].plot(df_logs_sorted['timestamp'], df_logs_sorted['bytes_sent'], 'o-', 
                   markersize=3, alpha=0.5, label='Tous les logs')
    anomalies_time = df_logs_sorted[df_logs_sorted['is_anomaly'] == 1]
    axes[1, 0].scatter(anomalies_time['timestamp'], anomalies_time['bytes_sent'],
                      c='red', s=100, marker='X', label='Anomalies')
    axes[1, 0].set_xlabel('Timestamp')
    axes[1, 0].set_ylabel('Bytes envoyés')
    axes[1, 0].set_title('Anomalies détectées dans le temps')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Graphique 4
    ip_counts = df_logs.groupby(['ip_source', 'is_anomaly']).size().unstack(fill_value=0)
    ip_counts.plot(kind='barh', ax=axes[1, 1], color=['blue', 'red'])
    axes[1, 1].set_xlabel('Nombre de connexions')
    axes[1, 1].set_ylabel('IP source')
    axes[1, 1].set_title('Distribution des IPs (Normal vs Anomalie)')
    axes[1, 1].legend(['Normal', 'Anomalie'])
    
    plt.tight_layout()
    plt.savefig('results/anomaly_detection_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\n✓ Visualisations sauvegardées dans 'results/anomaly_detection_analysis.png'")
    
    # Question 2.3
    print(f"\n📊 QUESTION 2.3:")
    print("Patterns détectés:")
    print("- Anomalies: volume de données élevé, ports suspects, IPs externes")
    print("- Ces informations aident l'analyste à prioriser les investigations")
