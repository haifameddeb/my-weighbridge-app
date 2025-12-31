import streamlit as st
from database import init_db

# Configuration de la page
st.set_page_config(page_title="Pont Bascule - Medigrain", page_icon="🚛", layout="wide")

# Initialisation BDD
init_db()

# Gestion de la session
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def login():
    st.title("Connexion - Pont Bascule")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        # Simulation logo Rose Blanche [cite: 29]
        st.markdown("### 🌾 ROSE BLANCHE GROUP")
        
        username = st.text_input("Identifiant")
        password = st.text_input("Mot de passe", type="password")
        
        if st.button("Se connecter", use_container_width=True):
            # Login simulé pour le prototype
            if username == "admin" and password == "admin":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Identifiant ou mot de passe incorrect")

def main_app():
    st.sidebar.title("Navigation")
    st.sidebar.success("Connecté en tant que Admin")
    
    st.title("Bienvenue sur l'application Pont Bascule")
    st.info("Utilisez le menu latéral pour accéder aux fonctionnalités.")
    
    if st.sidebar.button("Déconnexion"):
        st.session_state.authenticated = False
        st.rerun()

# Logique d'affichage
if not st.session_state.authenticated:
    login()
else:
    main_app()