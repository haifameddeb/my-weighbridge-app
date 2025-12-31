import streamlit as st
from database import add_tare
from datetime import datetime

st.set_page_config(page_title="Arrivée Camion", page_icon="📥")

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("Veuillez vous connecter sur la page principale.")
    st.stop()

st.title("🚛 Arrivée Camion / Tare")
st.markdown("---")

with st.form("form_tare"):
    col1, col2 = st.columns(2)
    
    with col1:
        no_quittance = st.text_input("N° Quittance Tare (STAM)")
        no_pesee = st.text_input("N° de pesée")
        matricule = st.text_input("Matricule Camion")
    
    with col2:
        transporteur = st.selectbox("Transporteur", ["TransLog Services", "MEDIGRAINS SA", "Autre"]) # [cite: 80]
        produit = st.selectbox("Produit à charger", ["BLÉ TENDRE", "MAÏS", "SOJA", "LUZERNE"])
        poids_entree = st.number_input("Poids d'entrée (KG)", min_value=0.0, step=10.0)
    
    date_entree = st.date_input("Date d'entrée", datetime.now())
    heure_entree = st.time_input("Heure d'entrée", datetime.now())
    
    # Bouton Scanner (Simulation option 2 [cite: 100])
    st.caption("ℹ️ Option Scan Quittance non active dans cette version web.")
    
    submitted = st.form_submit_button("Enregistrer Tare", use_container_width=True)

    if submitted:
        if matricule and poids_entree > 0:
            dt_full = datetime.combine(date_entree, heure_entree)
            add_tare(no_quittance, no_pesee, matricule, transporteur, produit, poids_entree, dt_full)
            st.success(f"Camion {matricule} enregistré avec succès (Poids Tare: {poids_entree} kg)")
        else:
            st.error("Veuillez remplir le matricule et le poids.")
