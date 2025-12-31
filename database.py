import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "pont_bascule.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Table principale basée sur les champs identifiés dans le CDC [cite: 4, 8, 97-99]
    c.execute('''
        CREATE TABLE IF NOT EXISTS pesees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_quittance_tare TEXT,
            numero_pesee TEXT,
            matricule_camion TEXT,
            transporteur TEXT,
            chauffeur TEXT,
            produit TEXT,
            poids_tare REAL,
            date_heure_entree TIMESTAMP,
            statut TEXT DEFAULT 'En cours', -- En cours, Chargé, Pesé, Sorti
            poids_brut REAL,
            poids_net REAL,
            date_heure_sortie TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_tare(quittance, pesee, matricule, transporteur, produit, poids, date_heure):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO pesees (numero_quittance_tare, numero_pesee, matricule_camion, transporteur, produit, poids_tare, date_heure_entree, statut)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Tare prise')
    ''', (quittance, pesee, matricule, transporteur, produit, poids, date_heure))
    conn.commit()
    conn.close()

def get_all_pesees():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM pesees ORDER BY date_heure_entree DESC", conn)
    conn.close()
    return df

def get_dashboard_metrics():
    df = get_all_pesees()
    return {
        "tare_prise": len(df[df['statut'] == 'Tare prise']),
        "en_cours": len(df[df['statut'] == 'En cours de chargement']),
        "termine": len(df[df['statut'] == 'Pesé']),
        "total": len(df)
    }