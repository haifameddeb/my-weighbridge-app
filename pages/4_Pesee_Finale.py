import streamlit as st
import sqlite3
import pandas as pd

st.title("⚖️ Pesée Finale")

conn = sqlite3.connect('logistique.db')
camions_fin = pd.read_sql("SELECT CAMION, TARE FROM flux_camions WHERE STATUT='Fin de chargement'", conn)

if not camions_fin.empty:
    camion_sel = st.selectbox("Sélectionner camion pour pesée", camions_fin['CAMION'])
    tare = camions_fin[camions_fin['CAMION'] == camion_sel]['TARE'].values[0]
    
    poids_brut = st.number_input("Poids Brut (kg)", min_value=0.0)
    poids_net = poids_brut - tare
    
    st.write(f"**Tare initiale :** {tare} kg")
    st.write(f"**Poids Net calculé :** {poids_net} kg")
    
    if st.button("Enregistrer Pesée Finale"):
        conn.execute("UPDATE flux_camions SET POIDS_BRUT=?, POIDS_NET=?, STATUT='Pesée effectuée' WHERE CAMION=?", 
                     (poids_brut, poids_net, camion_sel))
        conn.commit()
        st.success("Processus terminé pour ce camion.")
else:
    st.warning("Aucun camion prêt pour la pesée finale.")
conn.close()
