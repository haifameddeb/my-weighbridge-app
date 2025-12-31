import streamlit as st
from database import get_trucks_by_status, update_to_loaded

st.title("🚛 Étape 3 : Confirmation Chargement")
trucks = get_trucks_by_status('En cours de chargement')
if not trucks.empty:
    sel = st.selectbox("Camion chargé", trucks['matricule_camion'])
    id_p = trucks[trucks['matricule_camion'] == sel]['id'].values[0]
    if st.button("Confirmer"):
        update_to_loaded(id_p)
        st.success("Chargement terminé")
