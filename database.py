import sqlite3

def init_db():
    # Connexion à la base de données (crée le fichier s'il n'existe pas)
    conn = sqlite3.connect('logistique.db')
    cursor = conn.cursor()

    # Création de la table selon la structure fournie dans les spécifications
    # Type Alpha -> TEXT
    # Type Numérique -> REAL ou INTEGER
    # Type Date/Heure -> TEXT (Format ISO ou DD/MM/YYYY HH:MM)
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flux_camions (
            NUM_QUIT TEXT,          -- Alpha : Numéro de quittance
            NUM_PESEE TEXT,         -- Alpha : Numéro de pesée
            CAMION TEXT,            -- Alpha : Matricule du camion
            TRANSPORTUR TEXT,       -- Alpha : Nom du transporteur
            DH_TARE TEXT,           -- Date/Heure : Date et heure de la prise de tare
            TARE REAL,              -- Numérique : Poids de la tare
            STATUT TEXT,            -- Alpha : État actuel du camion (ex: 'Tare prise')
            DH_ORDRE TEXT,          -- Date/Heure : Date et heure de l'ordre
            ARTICLE TEXT,           -- Alpha : Désignation de l'article
            QTE_PREV REAL,          -- Numérique : Quantité prévue
            DH_DEB_CHARG TEXT,      -- Date/Heure : Début du chargement
            DH_FIN_CHARG TEXT,      -- Date/Heure : Fin du chargement
            POIDS_BRUT REAL,        -- Numérique : Poids total à la sortie
            POIDS_NET REAL          -- Numérique : Poids chargé (Calculé)
        )
    ''')

    conn.commit()
    conn.close()
    print("Base de données initialisée avec succès.")

if __name__ == "__main__":
    init_db()
