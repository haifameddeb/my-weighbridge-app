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

# ÉTAPE 1 : Arrivée Camion
def add_tare(q, p, m, t, pr, w):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO pesees (num_quittance_tare, num_pesee, matricule_camion, transporteur, produit, poids_tare, date_heure_entree, statut)
                 VALUES (?, ?, ?, ?, ?, ?, ?, 'Tare prise')''', (q, p, m, t, pr, w, datetime.now()))
    conn.commit()
    conn.close()

# ÉTAPE 2 : Affectation Silo
def update_to_ordre(id_p, silo):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE pesees SET statut = 'Ordre de chargement', silo_affecte = ? WHERE id = ?", (silo, id_p))
    conn.commit()
    conn.close()

# ÉTAPE 3 : Début Chargement
def update_to_loading(id_p):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE pesees SET statut = 'En cours de chargement' WHERE id = ?", (id_p,))
    conn.commit()
    conn.close()

# ÉTAPE 4 : Fin Chargement
def update_to_loaded(id_p):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE pesees SET statut = 'Chargé' WHERE id = ?", (id_p,))
    conn.commit()
    conn.close()

# ÉTAPE 5 : Pesée Finale
def finalize_pese(id_p, pb):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT poids_tare FROM pesees WHERE id = ?", (id_p,))
    pt = c.fetchone()[0]
    pn = pb - pt
    c.execute("UPDATE pesees SET poids_brut = ?, poids_net = ?, statut = 'Pesé', date_heure_sortie = ? WHERE id = ?", (pb, pn, datetime.now(), id_p))
    conn.commit()
    conn.close()
    return pn

def get_dashboard_metrics():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM pesees", conn)
    conn.close()
    if df.empty: return {"tare":0, "ordre":0, "cours":0, "charge":0, "pese":0}
    return {
        "tare": len(df[df['statut'] == 'Tare prise']),
        "ordre": len(df[df['statut'] == 'Ordre de chargement']),
        "cours": len(df[df['statut'] == 'En cours de chargement']),
        "charge": len(df[df['statut'] == 'Chargé']),
        "pese": len(df[df['statut'] == 'Pesé'])
    }

def get_all_pesees():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM pesees ORDER BY date_heure_entree DESC", conn)
    conn.close()
    return df

def get_trucks_by_status(st):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM pesees WHERE statut = ?", conn, params=(st,))
    conn.close()
    return df
