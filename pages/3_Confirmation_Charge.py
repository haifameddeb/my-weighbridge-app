import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.title("⏳ Confirmation de Chargement")

conn = sqlite3.connect('logistique.db')
col1, col2 = st.columns(2)

with col1:
    st.subheader("Début")
    dispo_deb = pd.read_sql("SELECT CAMION FROM flux_camions WHERE STATUT='Ordre de chargement'", conn)
    if not dispo_deb.empty:
        cam_deb = st.selectbox("Camion à charger", dispo_deb['CAMION'])
        if st.button("Démarrer Chargement"):
            dh = datetime.now().strftime("%d/%m/%Y %H:%M")
            conn.execute("UPDATE flux_camions SET DH_DEB_CHARG=?, STATUT='En cours de chargement' WHERE CAMION=?", (dh, cam_deb))
            conn.commit()
            st.rerun()

with col2:
    st.subheader("Fin")
    dispo_fin = pd.read_sql("SELECT CAMION FROM flux_camions WHERE STATUT='En cours de chargement'", conn)
    if not dispo_fin.empty:
        cam_fin = st.selectbox("Camion chargé", dispo_fin['CAMION'])
        if st.button("Terminer Chargement"):
            dh = datetime.now().strftime("%d/%m/%Y %H:%M")
            conn.execute("UPDATE flux_camions SET DH_FIN_CHARG=?, STATUT='Fin de chargement' WHERE CAMION=?", (dh, cam_fin))
            conn.commit()
            st.rerun()
conn.close()
