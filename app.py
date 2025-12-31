import streamlit as st
from database import init_db

# Configuration de la page
st.set_page_config(page_title="Pont Bascule - Medigrain", page_icon="🚛", layout="centered")

# Initialisation BDD
init_db()

# Style CSS pour l'ergonomie mobile et look Rose Blanche
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #E63946;
        color: white;
        font-weight: bold;
        border: none;
    }
    .login-box {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def login():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Apple_Computer_Logo_1977.svg/424px-Apple_Computer_Logo_1977.svg.png", width=100) # À remplacer par logo Medigrain
    st.title("Authentification")
    
    username = st.text_input("Identifiant", placeholder="Entrez votre ID")
    password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
    
    if st.button("SE CONNECTER"):
        if username == "admin" and password == "admin":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Identifiant ou mot de passe incorrect")
    st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.authenticated:
    login()
else:
    st.sidebar.title("Navigation")
    if st.sidebar.button("Déconnexion"):
        st.session_state.authenticated = False
        st.rerun()
    
    st.title("🚛 Gestion Pont Bascule")
    st.success("Bienvenue dans l'interface de gestion Medigrain.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("👈 Utilisez le menu pour saisir une **Tare**.")
    with col2:
        st.info("📊 Consultez le **Dashboard** pour le suivi.")
