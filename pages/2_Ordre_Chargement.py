import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Contrôle d'accès
if 'auth' not in st.session_state or not st.session_state.auth:
    st.warning("⚠️ Accès refusé. Veuillez vous connecter.")
    st.stop()

st.title("📝 Ordre de Chargement")

conn = sqlite3.connect('logistique.db')
camions_dispo = pd.read_sql("SELECT CAMION FROM flux_camions WHERE STATUT='Tare prise'", conn)

if not camions_dispo.empty:
    camion_sel = st.selectbox("Sélectionner un camion", camions_dispo['CAMION'])
    # Pas d'initialisation (champs vides)
    article = st.text_input("Article", value="")
    qte = st.number_input("Quantité prévue", min_value=0.0, value=0.0)
    
    if st.button("Valider l'ordre"):
        dh_now = datetime.now().strftime("%d/%m/%Y %H:%M")
        conn.execute("UPDATE flux_camions SET ARTICLE=?, QTE_PREV=?, DH_ORDRE=?, STATUT='Ordre de chargement' WHERE CAMION=?", 
                     (article, qte, dh_now, camion_sel))
        conn.commit()
        st.success("Ordre de chargement créé.")
        st.rerun()
else:
    st.warning("Aucun camion en attente d'ordre.")
conn.close()
