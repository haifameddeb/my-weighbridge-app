import streamlit as st
from database import add_tare
from datetime import datetime

st.set_page_config(page_title="Réception Tare", page_icon="⚖️", layout="wide")

if not st.session_state.get('authenticated', False):
    st.warning("Veuillez vous connecter sur la page d'accueil.")
    st.stop()

st.title("📥 Arrivée Camion / Tare")

# Section Scan (Simulation Mobile)
with st.expander("📷 Option de Scan Quittance", expanded=False):
    st.camera_input("Scanner le QR Code STAM")

with st.form("form_tare", clear_on_submit=True):
    st.subheader("Informations de Pesée")
    
    # Utilisation de colonnes qui s'empilent sur mobile
    col1, col2 = st.columns([1, 1])
    
    with col1:
        no_quittance = st.text_input("N° Quittance Tare (STAM)", placeholder="Ex: Q-2023-001")
        no_pesee = st.text_input("N° de pesée", placeholder="Ex: P-998")
        matricule = st.text_input("Matricule Camion 🚛", placeholder="Ex: 123 TUN 456")
    
    with col2:
        transporteur = st.selectbox("Transporteur", ["SNC", "STAM", "Privé", "Autre"])
        produit = st.selectbox("Produit", ["BLÉ TENDRE", "MAÏS", "SOJA", "ORGE"])
        poids_tare = st.number_input("Poids à vide (KG)", min_value=0, step=10)

    st.markdown("---")
    submitted = st.form_submit_button("VALIDER L'ENTRÉE DU CAMION")

    if submitted:
        if not matricule or poids_tare <= 0:
            st.error("Veuillez remplir le matricule et le poids.")
        else:
            add_tare(no_quittance, no_pesee, matricule, transporteur, produit, poids_tare, datetime.now())
            st.balloons()
            st.success(f"Camion {matricule} enregistré avec succès !")
