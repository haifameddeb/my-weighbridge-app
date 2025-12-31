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
            num_quittance_tare TEXT,
            num_pesee TEXT,
            matricule_camion TEXT,
            transporteur TEXT,
            produit TEXT,
            poids_tare REAL,
            poids_brut REAL DEFAULT 0,
            poids_net REAL DEFAULT 0,
            silo_affecte TEXT,
            statut TEXT,
            date_heure_entree TIMESTAMP,
            date_heure_sortie TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_tare(quittance, pesee, matricule, transporteur, produit, poids, date_heure):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO pesees (num_quittance_tare, num_pesee, matricule_camion, transporteur, produit, poids_tare, date_heure_entree, statut)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Tare prise')
    ''', (quittance, pesee, matricule, transporteur, produit, poids, date_heure))
    conn.commit()
    conn.close()

def update_to_loading(id_pesee, silo):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE pesees SET statut = 'En cours de chargement', silo_affecte = ? WHERE id = ?", (silo, id_pesee))
    conn.commit()
    conn.close()

def update_to_loaded(id_pesee):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE pesees SET statut = 'Chargé' WHERE id = ?", (id_pesee,))
    conn.commit()
    conn.close()

def finalize_weighing(id_pesee, poids_brut):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT poids_tare FROM pesees WHERE id = ?", (id_pesee,))
    poids_tare = c.fetchone()[0]
    poids_net = poids_brut - poids_tare
    c.execute('''
        UPDATE pesees SET poids_brut = ?, poids_net = ?, statut = 'Pesé', date_heure_sortie = ?
        WHERE id = ?
    ''', (poids_brut, poids_net, datetime.now(), id_pesee))
    conn.commit()
    conn.close()
    return poids_net

def get_all_pesees():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM pesees ORDER BY date_heure_entree DESC", conn)
    conn.close()
    return df

def get_dashboard_metrics():
    df = get_all_pesees()
    if df.empty:
        return {"tare": 0, "chargement": 0, "charge": 0, "pese": 0, "total": 0}
    return {
        "tare": len(df[df['statut'] == 'Tare prise']),
        "chargement": len(df[df['statut'] == 'En cours de chargement']),
        "charge": len(df[df['statut'] == 'Chargé']),
        "pese": len(df[df['statut'] == 'Pesé']),
        "total": len(df)
    }

def get_trucks_by_status(status):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM pesees WHERE statut = ?", conn, params=(status,))
    conn.close()
    return df
