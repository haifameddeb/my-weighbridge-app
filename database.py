import sqlite3
import os

def init_db():
    conn = sqlite3.connect('logistique.db')
    c = conn.cursor()
    
    # 1. Gestion de la table flux_camions
    try:
        c.execute("SELECT TRANSPORTEUR FROM flux_camions LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("DROP TABLE IF EXISTS flux_camions")
        c.execute('''CREATE TABLE flux_camions
                     (NUM_QUIT TEXT, NUM_PESEE TEXT, CAMION TEXT, 
                      TRANSPORTEUR TEXT, DH_TARE TEXT, TARE REAL, 
                      STATUT TEXT, DH_ORDRE TEXT, ARTICLE TEXT, 
                      QTE_PREV REAL, DH_DEB_CHARG TEXT, DH_FIN_CHARG TEXT, 
                      POIDS_BRUT REAL, POIDS_NET REAL)''')
        conn.commit()

    # 2. AJOUT STRICT : Création de la table documents_generes
    c.execute('''CREATE TABLE IF NOT EXISTS documents_generes
                 (ID_DOC INTEGER PRIMARY KEY AUTOINCREMENT,
                  CAMION TEXT,
                  FOURNISSEUR TEXT,
                  NUM_CMD_FOURN TEXT,
                  IS_BL_CLIENT INTEGER,
                  CODE_CLIENT TEXT,
                  RAISON_SOCIALE TEXT,
                  NUM_CMD_CLIENT TEXT,
                  DH_GENERATION TEXT)''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
