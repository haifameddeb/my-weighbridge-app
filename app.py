import streamlit as st
import pandas as pd
from database import init_db, get_all_pesees, get_dashboard_metrics

# 1. Configuration de la page
st.set_page_config(page_title="Pont Bascule - Medigrain", page_icon="📊", layout="wide")

# 2. Initialisation BDD
init_db()

# 3. Hack CSS pour masquer les éléments Streamlit et nettoyer l'UI
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #E63946; color: white; height: 3em; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- LOGIQUE DE CONNEXION ---
if not st.session_state.authenticated:
    _, col_card, _ = st.columns([1, 2, 1])
    with col_card:
        st.markdown("<br><br>", unsafe_allow_html=True)
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

# --- AFFICHAGE DU TABLEAU DE BORD (Page de lancement) ---
st.title("📊 Tableau de Bord - Accueil")

st.sidebar.title("Navigation")
if st.sidebar.button("Déconnexion"):
    st.session_state.authenticated = False
    st.rerun()

# Récupération des données pour les KPIs
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
    # On affiche les colonnes essentielles pour le dashboard
    cols_to_show = ["matricule_camion", "produit", "poids_tare", "statut", "date_heure_entree"]
    st.dataframe(df[cols_to_show], use_container_width=True, hide_index=True)
else:
    st.info("Aucun mouvement enregistré aujourd'hui.")
