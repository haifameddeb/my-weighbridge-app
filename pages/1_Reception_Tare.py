import streamlit as st
from database import add_tare
from datetime import datetime

st.set_page_config(page_title="Étape 1 - Réception", layout="centered")
st.title("📥 1. Réception & Pesée Tare")

with st.form("form_etape1"):
    col1, col2 = st.columns(2)
    with col1:
        num_q = st.text_input("N° Quittance Tare (STAM)")
        num_p = st.text_input("N° de Pesée")
        mat = st.text_input("Matricule Camion")
    with col2:
        transp = st.selectbox("Transporteur", ["SNC", "STAM", "Privé", "Autre"])
        prod = st.selectbox("Produit", ["BLÉ TENDRE", "MAÏS", "SOJA", "ORGE"])
        poids_t = st.number_input("Poids Tare (KG)", min_value=0.0, step=10.0)

    if st.form_submit_button("VALIDER L'ENTRÉE"):
        if mat and poids_t > 0:
            add_tare(num_q, num_p, mat, transp, prod, poids_t, datetime.now())
            st.success(f"Camion {mat} enregistré. Statut: Tare prise")
        else:
            st.error("Veuillez remplir le matricule et le poids tare.")
