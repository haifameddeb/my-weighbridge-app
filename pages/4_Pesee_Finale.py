import streamlit as st
from database import get_trucks_by_status, finalize_weighing

st.title("⚖️ Étape 4 & 5 : Pesée Finale & Sortie")
trucks = get_trucks_by_status('Chargé')
if not trucks.empty:
    sel = st.selectbox("Camion sur bascule", trucks['matricule_camion'])
    row = trucks[trucks['matricule_camion'] == sel].iloc[0]
    pb = st.number_input("Poids Brut (KG)", min_value=float(row['poids_tare']))
    if st.button("Clôturer"):
        net = finalize_weighing(row['id'], pb)
        st.success(f"Poids Net : {net} KG. Camion Sorti.")
