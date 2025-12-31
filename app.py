import streamlit as st
from database import init_db, get_dashboard_metrics, get_all_pesees

st.set_page_config(page_title="Medigrain TB", layout="wide")
init_db()

# CSS pour masquer le footer et styliser les KPIs
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.stMetric {background-color: white; padding: 10px; border-radius: 10px; border-left: 5px solid #E63946; shadow: 2px 2px 5px rgba(0,0,0,0.1);}</style>""", unsafe_allow_html=True)

if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if not st.session_state.authenticated:
    st.title("🔐 Connexion")
    if st.button("Se connecter (Admin/Admin)"): # Simplifié pour le test
        st.session_state.authenticated = True
        st.rerun()
    st.stop()

st.title("📊 Tableau de Bord - Flux Logistique")

m = get_dashboard_metrics()
cols = st.columns(5)
cols[0].metric("1. Tare Prise", m['tare'])
cols[1].metric("2. Ordre Charg.", m['ordre'])
cols[2].metric("3. En Cours", m['cours'])
cols[3].metric("4. Chargé", m['charge'])
cols[4].metric("5. Pesé (Sortie)", m['pese'])

st.divider()
st.subheader("🚚 Suivi des véhicules sur site")
df = get_all_pesees()
if not df.empty:
    st.dataframe(df[["matricule_camion", "produit", "silo_affecte", "statut", "date_heure_entree"]], use_container_width=True, hide_index=True)

if st.sidebar.button("Déconnexion"):
    st.session_state.authenticated = False
    st.rerun()
