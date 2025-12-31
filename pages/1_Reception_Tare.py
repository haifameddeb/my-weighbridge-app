import streamlit as st
from database import add_tare
from datetime import datetime
import cv2
import numpy as np
from pyzbar.pyzbar import decode

st.set_page_config(page_title="Réception Tare", page_icon="⚖️", layout="wide")

# --- FONCTION DE DECODAGE QR ---
def scan_qr(image_file):
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    # Détection du QR Code
    det = decode(opencv_image)
    if det:
        return det[0].data.decode('utf-8') # Retourne la chaîne lue
    return None

if not st.session_state.get('authenticated', False):
    st.warning("Veuillez vous connecter.")
    st.stop()

st.title("📥 Arrivée Camion / Tare")

# --- SECTION SCANNER ---
st.subheader("📷 Scan du QR Code")
img_file = st.camera_input("Placez le QR Code face à la caméra")

# Initialisation des variables de champs
scanned_data = {"quittance": "", "pesee": "", "matricule": ""}

if img_file:
    result = scan_qr(img_file)
    if result:
        st.success(f"Code détecté : {result}")
        # Analyse de la chaîne (Parsing par '-')
        try:
            parts = result.split('-')
            if len(parts) >= 3:
                scanned_data["quittance"] = parts[0]
                scanned_data["pesee"] = parts[1]
                scanned_data["matricule"] = parts[2]
            else:
                st.error("Format QR Code invalide (doit être : Quittance-Pesée-Matricule)")
        except Exception as e:
            st.error(f"Erreur de lecture : {e}")
    else:
        st.warning("Aucun QR Code lisible sur la photo.")

# --- FORMULAIRE ---
with st.form("form_tare", clear_on_submit=True):
    st.subheader("Vérification des informations")
    col1, col2 = st.columns(2)
    
    with col1:
        # Les champs se remplissent automatiquement si le scan réussit
        no_quittance = st.text_input("N° Quittance Tare", value=scanned_data["quittance"])
        no_pesee = st.text_input("N° de pesée", value=scanned_data["pesee"])
        matricule = st.text_input("Matricule Camion 🚛", value=scanned_data["matricule"])
    
    with col2:
        transporteur = st.selectbox("Transporteur", ["SNC", "STAM", "Privé", "Autre"])
        produit = st.selectbox("Produit", ["BLÉ TENDRE", "MAÏS", "SOJA", "ORGE"])
        poids_tare = st.number_input("Poids à vide (KG)", min_value=0, step=10)

    if st.form_submit_button("VALIDER L'ENTRÉE"):
        if matricule and poids_tare > 0:
            add_tare(no_quittance, no_pesee, matricule, transporteur, produit, poids_tare, datetime.now())
            st.success("Enregistrement réussi !")
        else:
            st.error("Données manquantes.")
