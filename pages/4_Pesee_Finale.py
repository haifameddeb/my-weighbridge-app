import streamlit as st
import sqlite3
import pandas as pd

if 'auth' not in st.session_state or not st.session_state.auth:
    st.warning("⚠️ Accès refusé.")
    st.stop()

st.title("⚖️ Pesée Finale")

conn = sqlite3.connect('logistique.db')
camions_fin = pd.read_sql("SELECT CAMION, TARE FROM flux_camions WHERE STATUT='Fin de chargement'", conn)

if not camions_fin.empty:
    camion_sel = st.selectbox("Sélectionner camion", camions_fin['CAMION'])
    tare = camions_fin[camions_fin['CAMION'] == camion_sel]['TARE'].values[0]
    
    # Pas de valeur par défaut (0.0)
    poids_brut = st.number_input("Poids Brut (kg)", min_value=0.0, value=0.0)
    
    if st.button("Enregistrer Pesée Finale"):
        poids_net = poids_brut - tare
        conn.execute("UPDATE flux_camions SET POIDS_BRUT=?, POIDS_NET=?, STATUT='Pesée effectuée' WHERE CAMION=?", 
                     (poids_brut, poids_net, camion_sel))
        conn.commit()
        st.success(f"Pesée enregistrée. Net : {poids_net} kg")
        st.rerun()
else:
    st.warning("Aucun camion prêt.")
conn.close()
