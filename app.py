import streamlit as st
import pandas as pd
from database import init_db, get_all_pesees, get_dashboard_metrics

# Configuration de la page
st.set_page_config(page_title="Pont Bascule - Medigrain", page_icon="📊", layout="wide")

# Cacher le footer "Created by..." et le menu Streamlit
st.markdown("""
    <style>
    /* Cache le footer "Made with Streamlit" */
    footer {visibility: hidden;}
    
    /* Cache le bouton 'Manage App' et les infos de déploiement pour les non-admin */
    header {visibility: hidden;}
    
    /* Optionnel : Supprimer le padding en haut pour gagner de l'espace */
    .block-container {
        padding-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)
# Initialisation BDD
init_db()

# Style CSS pour le look professionnel
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #E63946; color: white; }
    </style>
""", unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- LOGIQUE DE CONNEXION ---
if not st.session_state.authenticated:
    _, col_card, _ = st.columns([1, 2, 1])
    with col_card:
        st.title("🔐 Authentification")
        username = st.text_input("Identifiant")
        password = st.text_input("Mot de passe", type="password")
        if st.button("SE CONNECTER"):
            if username == "admin" and password == "admin":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Identifiant ou mot de passe incorrect")
    st.stop()

# --- AFFICHAGE DU TABLEAU DE BORD (Dès le lancement) ---
st.title("📊 Tableau de Bord - Accueil")

st.sidebar.title("Navigation")
if st.sidebar.button("Déconnexion"):
    st.session_state.authenticated = False
    st.rerun()

# KPIs comme dans votre version précédente
metrics = get_dashboard_metrics()
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"<div style='background-color:#E63946; padding:20px; border-radius:10px; color:white; text-align:center;'><h3>Tare Prise</h3><h1>{metrics['tare_prise']}</h1></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div style='background-color:#457B9D; padding:20px; border-radius:10px; color:white; text-align:center;'><h3>En Cours</h3><h1>{metrics['en_cours']}</h1></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div style='background-color:#1D3557; padding:20px; border-radius:10px; color:white; text-align:center;'><h3>Terminé</h3><h1>{metrics['termine']}</h1></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div style='background-color:#A8DADC; padding:20px; border-radius:10px; color:white; text-align:center;'><h3>Total Jour</h3><h1>{metrics['total']}</h1></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tableau des camions récents
st.subheader("📋 Suivi des flux en temps réel")
df = get_all_pesees()
if not df.empty:
    st.dataframe(df[["matricule_camion", "produit", "poids_tare", "statut", "date_heure_entree"]], use_container_width=True, hide_index=True)
else:
    st.info("Aucun mouvement enregistré aujourd'hui.")

