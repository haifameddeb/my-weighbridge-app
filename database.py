import sqlite3
import os

def init_db():
    db_path = 'logistique.db'
    
    # Optionnel : Décommentez la ligne suivante si vous voulez forcer la remise à zéro
    # if os.path.exists(db_path): os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Création de la table avec l'orthographe correcte : TRANSPORTEUR
    c.execute('''CREATE TABLE IF NOT EXISTS flux_camions
                 (NUM_QUIT TEXT, 
                  NUM_PESEE TEXT, 
                  CAMION TEXT, 
                  TRANSPORTEUR TEXT, 
                  DH_TARE TEXT, 
                  TARE REAL, 
                  STATUT TEXT, 
                  DH_ORDRE TEXT, 
                  ARTICLE TEXT, 
                  QTE_PREV REAL, 
                  DH_DEB_CHARG TEXT, 
                  DH_FIN_CHARG TEXT, 
                  POIDS_BRUT REAL, 
                  POIDS_NET REAL)''')
    
    conn.commit()
    conn.close()
    print("Base de données initialisée avec le champ TRANSPORTEUR.")

if __name__ == "__main__":
    init_db()
