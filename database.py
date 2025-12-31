import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "pont_bascule.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Table alignée strictement sur les spécifications
    c.execute('''
        CREATE TABLE IF NOT EXISTS pesees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num_quittance TEXT,
            num_pesee TEXT,
            matricule_camion TEXT,
            transporteur TEXT,
            poids_tare REAL,
            date_heure_entree TIMESTAMP,
            statut TEXT,
            article TEXT,
            quantite_prevue REAL,
            poids_brut REAL DEFAULT 0,
            poids_net REAL DEFAULT 0,
            date_heure_sortie TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_tare(num_quittance, num_pesee, camion, transporteur, poids_tare):
    """Enregistre la prise de tare initiale (Écran 1)"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # La date et l'heure sont générées automatiquement lors de l'enregistrement
    date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO pesees (num_quittance, num_pesee, matricule_camion, transporteur, poids_tare, date_heure_entree, statut)
        VALUES (?, ?, ?, ?, ?, ?, 'Tare prise')
    ''', (num_quittance, num_pesee, camion, transporteur, poids_tare, date_heure))
    conn.commit()
    conn.close()
