import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "pont_bascule.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
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
            statut TEXT DEFAULT 'Tare prise',
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
    if df.empty:
        return {"tare_prise": 0, "en_cours": 0, "termine": 0, "total": 0}
    
    return {
        "tare_prise": len(df[df['statut'] == 'Tare prise']),
        "en_cours": len(df[df['statut'] == 'En cours']),
        "termine": len(df[df['statut'] == 'Pesé']),
        "total": len(df)
    }

def get_waiting_trucks():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM pesees WHERE statut = 'Tare prise'", conn)
    conn.close()
    return df

def update_to_loading(id_pesee, silo):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # On harmonise le statut sur 'En cours' pour correspondre au dashboard
    c.execute("UPDATE pesees SET statut = 'En cours', transporteur = transporteur || ' (Silo: ' || ? || ')' WHERE id = ?", (silo, id_pesee))
    conn.commit()
    conn.close()
