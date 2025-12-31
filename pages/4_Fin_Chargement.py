import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

if 'auth' not in st.session_state or not st.session_state.auth:
    st.warning("⚠️ Accès refusé.")
    st.stop()

st.title("✅ Fin de Chargement")

conn = sqlite3.connect('logistique.db')
# Correction : TRANSPORTEUR (avec S)
query = "SELECT CAMION, TRANSPORTEUR, TARE, ARTICLE, DH_DEB_CHARG FROM flux_camions WHERE STATUT='En cours de chargement'"
df_en_cours = pd.read_sql(query, conn)

if not df_en_cours.empty:
    camion_sel = st.selectbox("Sélectionnez le camion", df_en_cours['CAMION'])
    infos = df_en_cours[df_en_cours['CAMION'] == camion_sel].iloc[0]
    
    st.success(f"**Article :** {infos['ARTICLE']} | **Début :** {infos['DH_DEB_CHARG']}")

    if st.button("Confirmer la FIN", use_container_width=True):
        dh_now = datetime.now().strftime("%d/%m/%Y %H:%M")
        conn.execute("UPDATE flux_camions SET DH_FIN_CHARG=?, STATUT='Fin de chargement' WHERE CAMION=?", (dh_now, camion_sel))
        conn.commit()
        st.success(f"Terminé pour {camion_sel}")
        st.rerun()
else:
    st.info("Aucun camion en cours de chargement.")
conn.close()
