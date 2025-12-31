import streamlit as st
from database import add_tare

st.set_page_config(page_title="Arrivée camion / Tare", layout="centered")

st.title("Arrivée camion / Tare")

# Formulaire respectant strictement la liste des champs
with st.container():
    num_quittance = st.text_input("N° Quittance tare", placeholder="Saisir le numéro...")
    num_pesee = st.text_input("N° de pesée", placeholder="Saisir le numéro...")
    poids_entree = st.number_input("Poids d'entrée (KG)", min_value=0.0, step=10.0)
    
    # Information : La date/heure sera stockée automatiquement lors du clic
    st.info("Date / Heure d'entrée : Sera enregistrée automatiquement")
    
    matricule = st.text_input("Matricule camion")
    transporteur = st.text_input("Transporteur")

    # Bouton Scan Quittance (Simulé ici par un bouton décoratif selon CDC) 
    if st.button("🔍 Scanner quittance STAM", use_container_width=True):
        st.write("Fonction de scan activée...")

    st.markdown("---")
    
    # Bouton Enregistrer pour valider l'entrée au statut 'Tare prise'
    if st.button("Enregistrer", type="primary", use_container_width=True):
        if num_quittance and num_pesee and matricule and poids_entree > 0:
            add_tare(num_quittance, num_pesee, matricule, transporteur, poids_entree)
            st.success(f"Camion {matricule} enregistré au statut 'Tare prise'")
        else:
            st.error("Veuillez remplir tous les champs obligatoires.")
