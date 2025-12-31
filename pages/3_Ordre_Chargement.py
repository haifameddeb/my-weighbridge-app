import streamlit as st
from database import get_trucks_by_status, update_to_loading

st.set_page_config(page_title="Étape 2 - Affectation", layout="centered")
st.title("🏗️ 2. Ordre de Chargement")

trucks = get_trucks_by_status('Tare prise')

if not trucks.empty:
    options = trucks.apply(lambda x: f"{x['matricule_camion']} | {x['produit']}", axis=1).tolist()
    selection = st.selectbox("Sélectionner le camion à diriger", options)
    
    idx = options.index(selection)
    row = trucks.iloc[idx]
    
    silo = st.radio("Point de chargement affecté :", ["Silo 01", "Silo 02", "Silo 03", "Hangar"])
    
    if st.button("ENVOYER AU SILO"):
        update_to_loading(row['id'], silo)
        st.success(f"Camion {row['matricule_camion']} envoyé vers {silo}")
else:
    st.info("Aucun camion en attente d'affectation.")
