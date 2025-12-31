import streamlit as st
from database import get_trucks_by_status, update_to_loaded

st.set_page_config(page_title="Étape 3 - Chargé", layout="centered")
st.title("🚛 3. Confirmation Chargement")

trucks = get_trucks_by_status('En cours de chargement')

if not trucks.empty:
    options = trucks.apply(lambda x: f"{x['matricule_camion']} | {x['silo_affecte']}", axis=1).tolist()
    selection = st.selectbox("Sélectionner le camion qui a fini de charger", options)
    
    idx = options.index(selection)
    if st.button("CONFIRMER FIN CHARGEMENT"):
        update_to_loaded(trucks.iloc[idx]['id'])
        st.success("Statut mis à jour : Chargé. Le camion peut retourner à la bascule.")
else:
    st.info("Aucun camion n'est actuellement au chargement.")
