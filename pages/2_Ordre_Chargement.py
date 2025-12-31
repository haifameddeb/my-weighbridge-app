import streamlit as st
from database import get_trucks_by_status, update_to_loading

st.title("🏗️ Étape 2 : Affectation Silo")
trucks = get_trucks_by_status('Tare prise')
if not trucks.empty:
    sel = st.selectbox("Camion", trucks['matricule_camion'])
    silo = st.selectbox("Silo", ["Silo 01", "Silo 02", "Silo 03"])
    id_p = trucks[trucks['matricule_camion'] == sel]['id'].values[0]
    if st.button("Affecter"):
        update_to_loading(id_p, silo)
        st.success("Camion envoyé au silo")
