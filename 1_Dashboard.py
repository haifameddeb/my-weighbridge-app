import streamlit as st
from database import get_dashboard_metrics, get_all_pesees
import plotly.express as px

st.set_page_config(page_title="Tableau de Bord", page_icon="📊", layout="wide")

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("Veuillez vous connecter.")
    st.stop()

st.title("Tableau de bord - Accueil")

# Récupération des données fraîches
metrics = get_dashboard_metrics()

# Affichage des KPIs comme sur l'image 
c1, c2, c3, c4 = st.columns(4)
c1.metric("⚖️ Tare prise", metrics["tare_prise"])
c2.metric("📋 Ordre chargement", "N/A") # Sera dev au sprint 2
c3.metric("🚚 En chargement", metrics["en_cours"])
c4.metric("✅ Pesée effectuée", metrics["termine"])

st.markdown("---")

st.subheader("Flux des camions récents")
df = get_all_pesees()

if not df.empty:
    st.dataframe(
        df[["matricule_camion", "transporteur", "produit", "poids_tare", "statut", "date_heure_entree"]],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Aucun camion enregistré pour le moment.")