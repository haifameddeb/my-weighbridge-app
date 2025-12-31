import sqlite3
import os

def reset_db():
    # Supprime l'ancienne base pour repartir à neuf
    if os.path.exists('logistique.db'):
        os.remove('logistique.db')
    
    conn = sqlite3.connect('logistique.db')
    c = conn.cursor()
    # On respecte EXACTEMENT les noms utilisés dans vos fichiers 1_, 2_, etc.
    c.execute('''CREATE TABLE flux_camions
                 (NUM_QUIT TEXT, NUM_PESEE TEXT, CAMION TEXT, TRANSPORTUR TEXT, 
                  DH_TARE TEXT, TARE REAL, STATUT TEXT, DH_ORDRE TEXT, 
                  ARTICLE TEXT, QTE_PREV REAL, DH_DEB_CHARG TEXT, 
                  DH_FIN_CHARG TEXT, POIDS_BRUT REAL, POIDS_NET REAL)''')
    conn.commit()
    conn.close()
    print("Base de données réinitialisée avec la structure correcte.")

reset_db()
