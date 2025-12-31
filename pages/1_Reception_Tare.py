import streamlit as st
import sqlite3
from datetime import datetime

st.title("🚛 Réception & Prise de Tare")

with st.form("form_tare"):
    num_quit = st.text_input("N° Quittance")
    num_pesee = st.text_input("N° Pesée")
    camion = st.text_input("Matricule Camion")
    transporteur = st.text_input("Transporteur")
    tare = st.number_input("Poids Tare (kg)", min_value=0.0)
    
    if st.form_submit_button("Valider l'arrivée"):
        dh_now = datetime.now().strftime("%d/%m/%Y %H:%M")
        conn = sqlite3.connect('logistique.db')
        c = conn.cursor()
        c.execute("""INSERT INTO flux_camions (NUM_QUIT, NUM_PESEE, CAMION, TRANSPORTUR, TARE, DH_TARE, STATUT) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                  (num_quit, num_pesee, camion, transporteur, tare, dh_now, "Tare prise"))
        conn.commit()
        conn.close()
        st.success(f"Camion {camion} enregistré avec succès.")
