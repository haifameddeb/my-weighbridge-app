import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from database import init_db

init_db()

st.title("⏳ Début de Chargement")

conn = sqlite3.connect('logistique.db')
# On récupère les camions qui ont un ordre mais n'ont pas encore commencé
query = "SELECT CAMION, TRANPORTEUR, TARE, ARTICLE, DH_ORDRE FROM flux_camions WHERE STATUT='Ordre de chargement'"
df_dispo = pd.read_sql(query, conn)

if not df_dispo.empty:
    camion_sel = st.selectbox("Sélectionnez le camion qui commence le chargement", df_dispo['CAMION'])
    
    # Récupération des infos du camion choisi
    infos = df_dispo[df_dispo['CAMION'] == camion_sel].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Transporteur :** {infos['TRANPORTEUR']}")
        st.info(f"**Article :** {infos['ARTICLE']}")
    with col2:
        st.info(f"**Tare :** {infos['TARE']} kg")
        st.info(f"**Heure Ordre :** {infos['DH_ORDRE']}")

    if st.button("Confirmer le DÉBUT du chargement", use_container_width=True):
        dh_now = datetime.now().strftime("%d/%m/%Y %H:%M")
        conn.execute("""UPDATE flux_camions 
                     SET DH_DEB_CHARG=?, STATUT='En cours de chargement' 
                     WHERE CAMION=?""", (dh_now, camion_sel))
        conn.commit()
        st.success(f"Chargement démarré pour {camion_sel} à {dh_now}")
        st.rerun()
else:
    st.warning("Aucun camion en attente de début de chargement.")

conn.close()
