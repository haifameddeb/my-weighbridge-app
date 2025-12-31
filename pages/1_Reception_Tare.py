import streamlit as st
from database import add_tare

st.title("📥 Étape 1 : Réception & Tare")

with st.form("form_reception"):
    col1, col2 = st.columns(2)
    with col1:
        q = st.text_input("N° Quittance Tare")
        p = st.text_input("N° de Pesée")
        m = st.text_input("Matricule Camion")
    with col2:
        trans = st.text_input("Transporteur")
        prod = st.selectbox("Produit", ["BLÉ", "MAÏS", "ORGE", "SOJA"])
        w = st.number_input("Poids Tare (KG)", min_value=0.0)
    
    submit = st.form_submit_button("VALIDER L'ENTRÉE")
    
    if submit:
        if m and w > 0:
            # On envoie 6 arguments ici (q, p, m, trans, prod, w)
            add_tare(q, p, m, trans, prod, w)
            st.success(f"Camion {m} enregistré !")
        else:
            st.error("Veuillez remplir le matricule et le poids.")
