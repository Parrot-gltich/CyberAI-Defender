import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_phishing_dataset():
    """Crée un dataset d'exemple pour la détection de phishing"""
    emails_data = {
        'text': [
            "Congratulations! You have won $1,000,000. Click here to claim your prize now!",
            "Your account has been compromised. Verify your identity immediately by clicking this link.",
            "Hi team, please find attached the quarterly report for review.",
            "Meeting scheduled for tomorrow at 10 AM in conference room B.",
            "URGENT: Your bank account will be closed. Update your information now!",
            "Dear customer, your package is ready for delivery. Track your shipment here.",
            "Hello, I hope this email finds you well. Let's schedule a call next week.",
            "You have inherited $5 million from a distant relative. Contact us immediately!",
            "Reminder: Project deadline is next Friday. Please submit your work on time.",
            "Your password will expire today. Reset it now to avoid account suspension!",
            "Thank you for your purchase. Your order #12345 will arrive in 3-5 business days.",
            "WINNER ALERT! You are the lucky winner of our lottery. Claim your prize!",
            "Can you please review the attached document and provide your feedback?",
            "Your Netflix subscription has expired. Update payment information to continue.",
            "Team lunch tomorrow at 12:30 PM. Please confirm your attendance.",
            "FINAL NOTICE: Your account will be deleted unless you verify your email now!",
            "Please find the meeting notes from yesterday's discussion attached.",
            "You have received a secure message. Click to view your encrypted document.",
            "Quarterly performance review scheduled for next Monday at 2 PM.",
            "Act now! Limited time offer. Get 90% discount on all products today!"
        ],
        'label': [1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # 1 = phishing, 0 = légitime
    }
    
    return pd.DataFrame(emails_data)

def create_logs_dataset():
    """Crée un dataset de logs simulés pour la détection d'anomalies"""
    np.random.seed(42)
    
    # Génération de logs normaux
    n_normal = 180
    normal_logs = {
        'timestamp': [datetime.now() - timedelta(minutes=i) for i in range(n_normal)],
        'ip_source': np.random.choice(['192.168.1.10', '192.168.1.15', '192.168.1.20'], n_normal),
        'port_dest': np.random.choice([80, 443, 8080], n_normal),
        'bytes_sent': np.random.normal(5000, 1000, n_normal).astype(int),
        'requests_per_min': np.random.normal(10, 3, n_normal).astype(int)
    }
    
    # Génération de logs anormaux
    n_anomalies = 20
    anomaly_logs = {
        'timestamp': [datetime.now() - timedelta(minutes=i) for i in range(n_anomalies)],
        'ip_source': np.random.choice(['10.0.0.50', '172.16.0.100'], n_anomalies),
        'port_dest': np.random.choice([22, 3389, 445], n_anomalies),
        'bytes_sent': np.random.normal(50000, 10000, n_anomalies).astype(int),
        'requests_per_min': np.random.normal(100, 20, n_anomalies).astype(int)
    }
    
    # Combinaison et mélange
    df_logs = pd.concat([
        pd.DataFrame(normal_logs),
        pd.DataFrame(anomaly_logs)
    ], ignore_index=True)
    
    return df_logs.sample(frac=1, random_state=42).reset_index(drop=True)

def create_malware_dataset():
    """Crée un dataset simulé pour la classification de malware"""
    np.random.seed(42)
    n_samples = 200
    
    # Fichiers bénins
    benign_data = {
        'file_size': np.random.normal(50000, 20000, n_samples // 2).astype(int),
        'entropy': np.random.normal(5.5, 0.8, n_samples // 2),
        'num_imports': np.random.normal(30, 10, n_samples // 2).astype(int),
        'num_exports': np.random.normal(5, 3, n_samples // 2).astype(int),
        'num_sections': np.random.normal(4, 1, n_samples // 2).astype(int),
        'has_signature': np.random.choice([0, 1], n_samples // 2, p=[0.2, 0.8]),
        'label': 0  # 0 = bénin
    }
    
    # Fichiers malveillants
    malware_data = {
        'file_size': np.random.normal(150000, 50000, n_samples // 2).astype(int),
        'entropy': np.random.normal(7.2, 0.5, n_samples // 2),
        'num_imports': np.random.normal(80, 20, n_samples // 2).astype(int),
        'num_exports': np.random.normal(2, 2, n_samples // 2).astype(int),
        'num_sections': np.random.normal(6, 2, n_samples // 2).astype(int),
        'has_signature': np.random.choice([0, 1], n_samples // 2, p=[0.9, 0.1]),
        'label': 1  # 1 = malware
    }
    
    # Combinaison et mélange
    df_malware = pd.concat([
        pd.DataFrame(benign_data),
        pd.DataFrame(malware_data)
    ], ignore_index=True)
    
    return df_malware.sample(frac=1, random_state=42).reset_index(drop=True)
