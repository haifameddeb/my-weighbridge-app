import streamlit as st
from database import add_tare
from datetime import datetime

st.title("📥 Étape 1 : Réception & Tare")
with st.form("f1"):
    col1, col2 = st.columns(2)
    with col1:
        q = st.text_input("N° Quittance Tare")
        p = st.text_input("N° de Pesée")
    with col2:
        m = st.text_input("Matricule Camion")
        w = st.number_input("Poids Tare (KG)", min_value=0.0)
    
    prod = st.selectbox("Produit", ["BLÉ", "MAÏS", "ORGE"])
    trans = st.text_input("Transporteur")
    
    if st.form_submit_button("Valider"):
        add_tare(q, p, m, trans, prod, w, datetime.now())
        st.success("Enregistré !")
