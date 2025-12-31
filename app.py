import streamlit as st
from database import init_db, get_dashboard_metrics, get_all_pesees

st.set_page_config(page_title="Medigrain - Dashboard", layout="wide")
init_db()

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

st.title("📊 Suivi des 5 Étapes - Pont Bascule")

m = get_dashboard_metrics()
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("1. Tare Prise", m['tare'])
c2.metric("2. Au Silo", m['chargement'])
c3.metric("3. Chargé", m['charge'])
c4.metric("4. Pesé (Sortie)", m['pese'])
c5.metric("Total Flux", m['total'])

st.divider()
df = get_all_pesees()
if not df.empty:
    st.subheader("Historique des mouvements")
    st.dataframe(df[["num_quittance_tare", "matricule_camion", "produit", "statut", "date_heure_entree"]], use_container_width=True)

if st.sidebar.button("Déconnexion"):
    st.session_state.authenticated = False
    st.rerun()
