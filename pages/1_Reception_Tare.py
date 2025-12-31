import streamlit as st
import sqlite3
from datetime import datetime
from database import init_db

# Sécurité : Initialiser la base si elle n'existe pas
init_db()

st.title("🚛 Réception & Prise de Tare")

with st.form("form_tare", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        num_quit = st.text_input("N° Quittance")
        num_pesee = st.text_input("N° Pesée")
        camion = st.text_input("Matricule Camion")
        
    with col2:
        transporteur = st.text_input("Transporteur")
        tare = st.number_input("Poids Tare (kg)", min_value=0.0, step=0.1)
    
    submit = st.form_submit_button("Enregistrer l'arrivée")

    if submit:
        if not camion or not transporteur:
            st.error("Veuillez remplir au moins le matricule et le transporteur.")
        else:
            try:
                dh_now = datetime.now().strftime("%d/%m/%Y %H:%M")
                conn = sqlite3.connect('logistique.db')
                c = conn.cursor()
                
                # Utilisation de TRANPORTEUR pour correspondre à la DB
                c.execute("""INSERT INTO flux_camions 
                             (NUM_QUIT, NUM_PESEE, CAMION, TRANPORTEUR, TARE, DH_TARE, STATUT) 
                             VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                          (num_quit, num_pesee, camion, transporteur, tare, dh_now, "Tare prise"))
                
                conn.commit()
                conn.close()
                st.success(f"✅ Camion {camion} enregistré avec succès au statut 'Tare prise'.")
            except Exception as e:
                st.error(f"Erreur lors de l'enregistrement : {e}")

# Affichage des camions déjà arrivés pour vérification
st.subheader("Dernières arrivées")
conn = sqlite3.connect('logistique.db')
df = sqlite3.connect('logistique.db').execute("SELECT CAMION, TRANPORTEUR, DH_TARE FROM flux_camions WHERE STATUT='Tare prise' ORDER BY DH_TARE DESC").fetchall()
if df:
    st.table(df)
conn.close()
