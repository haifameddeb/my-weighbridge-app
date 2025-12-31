import streamlit as st
from database import init_db, get_dashboard_metrics, get_all_pesees

st.set_page_config(page_title="Medigrain - Pont Bascule", layout="wide")
init_db()

# Hack CSS pour cacher les éléments Streamlit et styliser les cartes
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Connexion")
    user = st.text_input("Identifiant")
    pw = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if user == "admin" and pw == "admin":
            st.session_state.authenticated = True
            st.rerun()
    st.stop()

st.title("📊 Tableau de Bord Temps Réel")

# 5 Compteurs basés sur les étapes du document
m = get_dashboard_metrics()
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("1. Tare Prise", m['tare'])
c2.metric("2. En Chargement", m['chargement'])
c3.metric("3. Chargé", m['charge'])
c4.metric("4. Pesé", m['pese'])
c5.metric("Total Mouvements", m['total'])

st.divider()
st.subheader("📋 Liste des mouvements")
df = get_all_pesees()
if not df.empty:
    st.dataframe(df[["num_quittance_tare", "matricule_camion", "produit", "statut", "date_heure_entree"]], use_container_width=True, hide_index=True)

if st.sidebar.button("Déconnexion"):
    st.session_state.authenticated = False
    st.rerun()
