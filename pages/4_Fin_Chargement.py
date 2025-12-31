import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from database import init_db

init_db()

st.title("✅ Fin de Chargement")

conn = sqlite3.connect('logistique.db')
# On récupère uniquement les camions en cours de chargement
query = "SELECT CAMION, TRANSPORTEUR, TARE, ARTICLE, DH_DEB_CHARG FROM flux_camions WHERE STATUT='En cours de chargement'"
df_en_cours = pd.read_sql(query, conn)

if not df_en_cours.empty:
    camion_sel = st.selectbox("Sélectionnez le camion qui a fini de charger", df_en_cours['CAMION'])
    
    # Récupération des infos
    infos = df_en_cours[df_en_cours['CAMION'] == camion_sel].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"**Transporteur :** {infos['TRANSPORTEUR']}")
        st.success(f"**Article :** {infos['ARTICLE']}")
    with col2:
        st.success(f"**Tare :** {infos['TARE']} kg")
        st.success(f"**Débuté le :** {infos['DH_DEB_CHARG']}")

    if st.button("Confirmer la FIN du chargement", use_container_width=True):
        dh_now = datetime.now().strftime("%d/%m/%Y %H:%M")
        conn.execute("""UPDATE flux_camions 
                     SET DH_FIN_CHARG=?, STATUT='Fin de chargement' 
                     WHERE CAMION=?""", (dh_now, camion_sel))
        conn.commit()
        st.success(f"Chargement terminé pour {camion_sel} à {dh_now}")
        st.rerun()
else:
    st.info("Aucun camion n'est actuellement en cours de chargement.")

conn.close()
