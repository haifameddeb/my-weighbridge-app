import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Gestion Flux Camions", layout="wide")

# Initialisation de la base de données
def init_db():
    conn = sqlite3.connect('logistique.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS flux_camions
                 (NUM_QUIT TEXT, NUM_PESEE TEXT, CAMION TEXT, TRANSPORTUR TEXT, 
                  DH_TARE TEXT, TARE REAL, STATUT TEXT, DH_ORDRE TEXT, 
                  ARTICLE TEXT, QTE_PREV REAL, DH_DEB_CHARG TEXT, 
                  DH_FIN_CHARG TEXT, POIDS_BRUT REAL, POIDS_NET REAL)''')
    conn.commit()
    conn.close()

init_db()

# Authentification simplifiée
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Connexion")
    user = st.text_input("Utilisateur")
    pw = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if user == "admin" and pw == "admin":
            st.session_state.logged_in = True
            st.rerun()
else:
    st.title("📊 Tableau de Bord - Accueil")
    conn = sqlite3.connect('logistique.db')
    df = pd.read_sql("SELECT STATUT, COUNT(*) as Total FROM flux_camions GROUP BY STATUT", conn)
    conn.close()

    if not df.empty:
        cols = st.columns(len(df))
        for i, row in df.iterrows():
            cols[i].metric(label=row['STATUT'], value=row['Total'])
    else:
        st.info("Aucune donnée en base pour le moment.")
