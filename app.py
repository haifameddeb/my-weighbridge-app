import streamlit as st
from database import init_db, get_dashboard_metrics, get_all_pesees

st.set_page_config(page_title="Dashboard Medigrain", layout="wide")
init_db()

st.title("📊 Tableau de Bord Logistique")

m = get_dashboard_metrics()
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("1. Tare Prise", m['tare'])
c2.metric("2. Ordre Chargement", m['ordre'])
c3.metric("3. En Cours", m['cours'])
c4.metric("4. Chargé", m['charge'])
c5.metric("5. Pesé (Sortie)", m['pese'])

st.divider()
df = get_all_pesees()
if not df.empty:
    st.dataframe(df[["matricule_camion", "produit", "statut", "date_heure_entree"]], use_container_width=True)
