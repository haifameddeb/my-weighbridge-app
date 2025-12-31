import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

if 'auth' not in st.session_state or not st.session_state.auth:
    st.warning("⚠️ Accès refusé.")
    st.stop()

st.title("⏳ Début de Chargement")

conn = sqlite3.connect('logistique.db')
# Correction : TRANSPORTEUR (avec S)
query = "SELECT CAMION, TRANSPORTEUR, TARE, ARTICLE, DH_ORDRE FROM flux_camions WHERE STATUT='Ordre de chargement'"
df_dispo = pd.read_sql(query, conn)

if not df_dispo.empty:
    camion_sel = st.selectbox("Sélectionnez le camion", df_dispo['CAMION'])
    infos = df_dispo[df_dispo['CAMION'] == camion_sel].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Transporteur :** {infos['TRANSPORTEUR']}")
        st.info(f"**Article :** {infos['ARTICLE']}")
    with col2:
        st.info(f"**Tare :** {infos['TARE']} kg")

    if st.button("Confirmer le DÉBUT", use_container_width=True):
        dh_now = datetime.now().strftime("%d/%m/%Y %H:%M")
        conn.execute("UPDATE flux_camions SET DH_DEB_CHARG=?, STATUT='En cours de chargement' WHERE CAMION=?", (dh_now, camion_sel))
        conn.commit()
        st.success(f"Démarré pour {camion_sel}")
        st.rerun()
else:
    st.warning("Aucun camion en attente.")
conn.close()
