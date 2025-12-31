import streamlit as st
import sqlite3
from datetime import datetime
from database import init_db

# 1. CONTRÔLE D'ACCÈS : Vérifie si l'utilisateur est connecté
if 'auth' not in st.session_state or not st.session_state.auth:
    st.warning("⚠️ Accès refusé. Veuillez vous connecter sur la page d'accueil.")
    if st.button("Aller à la page de connexion"):
        st.switch_page("app.py")
    st.stop()

# Initialisation de la base
init_db()

st.title("🚛 Réception & Prise de Tare")

# 2. FORMULAIRE : Champs vides à l'ouverture (sans initialisation)
with st.form("form_tare", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        # Utilisation de chaînes vides "" pour ne pas pré-remplir
        num_quit = st.text_input("N° Quittance", value="")
        num_pesee = st.text_input("N° Pesée", value="")
        camion = st.text_input("Matricule Camion", value="")
        
    with col2:
        transporteur = st.text_input("Transporteur", value="")
        # Valeur 0.0 pour le poids (standard numérique)
        tare = st.number_input("Poids Tare (kg)", min_value=0.0, step=0.1, value=0.0)
    
    submit = st.form_submit_button("Enregistrer l'arrivée")

    if submit:
        # Validation stricte : Matricule et Transporteur obligatoires
        if not camion or not transporteur:
            st.error("Veuillez remplir au moins le matricule et le transporteur.")
        else:
            try:
                dh_now = datetime.now().strftime("%d/%m/%Y %H:%M")
                conn = sqlite3.connect('logistique.db')
                c = conn.cursor()
                
                # Insertion avec l'orthographe TRANPORTEUR validée précédemment
                # Note : Assurez-vous que votre database.py utilise bien TRANPORTEUR
                c.execute("""INSERT INTO flux_camions 
                             (NUM_QUIT, NUM_PESEE, CAMION, TRANPORTEUR, TARE, DH_TARE, STATUT) 
                             VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                          (num_quit, num_pesee, camion, transporteur, tare, dh_now, "Tare prise"))
                
                conn.commit()
                conn.close()
                st.success(f"✅ Camion {camion} enregistré au statut 'Tare prise'.")
                st.rerun() # Rafraîchit pour vider visuellement les champs après succès
            except sqlite3.OperationalError as e:
                # Alerte spécifique en cas d'erreur de nom de colonne (ex: TRANSPORTEUR vs TRANPORTEUR)
                st.error(f"Erreur de structure de base de données : {e}")
            except Exception as e:
                st.error(f"Erreur lors de l'enregistrement : {e}")

# 3. AFFICHAGE DE L'HISTORIQUE RÉCENT
st.subheader("Dernières arrivées")
try:
    conn_list = sqlite3.connect('logistique.db')
    # Utilisation de TRANPORTEUR pour correspondre à la requête de tableau de bord corrigée
    query = "SELECT CAMION, TRANPORTEUR, DH_TARE FROM flux_camions WHERE STATUT='Tare prise' ORDER BY DH_TARE DESC"
    df_recent = conn_list.execute(query).fetchall()
    if df_recent:
        st.table(df_recent)
    conn_list.close()
except:
    st.info("Aucun camion en attente pour le moment.")
