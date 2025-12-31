import sqlite3
import os

def init_db():
    conn = sqlite3.connect('logistique.db')
    c = conn.cursor()
    
    # Vérification si la colonne correcte existe, sinon on recrée
    try:
        c.execute("SELECT TRANPORTEUR FROM flux_camions LIMIT 1")
    except sqlite3.OperationalError:
        # Si erreur, cela signifie que la colonne TRANPORTEUR n'existe pas
        # On supprime et on recrée avec la bonne structure
        c.execute("DROP TABLE IF EXISTS flux_camions")
        c.execute('''CREATE TABLE flux_camions
                     (NUM_QUIT TEXT, 
                      NUM_PESEE TEXT, 
                      CAMION TEXT, 
                      TRANPORTEUR TEXT, 
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

if __name__ == "__main__":
    init_db()
