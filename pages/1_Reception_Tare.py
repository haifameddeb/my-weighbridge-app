import streamlit as st
from database import add_tare
from datetime import datetime
import cv2
import numpy as np
from pyzbar.pyzbar import decode

st.set_page_config(page_title="Réception Tare", page_icon="⚖️", layout="wide")

def scan_qr(image_file):
    try:
        file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        det = decode(opencv_image)
        if det:
            return det[0].data.decode('utf-8')
    except Exception as e:
        st.error(f"Erreur technique lors du scan : {e}")
    return None

if not st.session_state.get('authenticated', False):
    st.warning("Veuillez vous connecter sur la page d'accueil.")
    st.stop()

st.title("📥 Arrivée Camion / Tare")

# Valeurs par défaut
data = {"q": "", "p": "", "m": ""}

# Section Photo
img_file = st.camera_input("Scanner le QR Code (Quittance-Pesée-Matricule)")

if img_file:
    raw_text = scan_qr(img_file)
    if raw_text:
        parts = raw_text.split('-')
        if len(parts) >= 3:
            data["q"], data["p"], data["m"] = parts[0], parts[1], parts[2]
            st.success(f"✅ Scan réussi : {raw_text}")
        else:
            st.error("❌ Format QR invalide. Attendu : Quittance-Pesée-Matricule")

with st.form("form_tare", clear_on_submit=True):
    st.subheader("Informations de Pesée")
    col1, col2 = st.columns(2)
    
    with col1:
        no_quittance = st.text_input("N° Quittance Tare", value=data["q"])
        no_pesee = st.text_input("N° de pesée", value=data["p"])
        matricule = st.text_input("Matricule Camion 🚛", value=data["m"])
    
    with col2:
        transporteur = st.selectbox("Transporteur", ["SNC", "STAM", "Privé", "Autre"])
        produit = st.selectbox("Produit", ["BLÉ TENDRE", "MAÏS", "SOJA", "ORGE"])
        poids_tare = st.number_input("Poids à vide (KG)", min_value=0, step=10)

    if st.form_submit_button("VALIDER L'ENTRÉE"):
        if matricule and poids_tare > 0:
            add_tare(no_quittance, no_pesee, matricule, transporteur, produit, poids_tare, datetime.now())
            st.balloons()
            st.success("Données enregistrées !")
