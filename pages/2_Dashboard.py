import streamlit as st
import pandas as pd
from database import get_all_pesees, get_dashboard_metrics

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

if not st.session_state.get('authenticated', False):
    st.warning("Veuillez vous connecter.")
    st.stop()

st.title("📊 Tableau de Bord - Accueil")

# KPIs en haut
metrics = get_dashboard_metrics()
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"<div style='background-color:#E63946; padding:20px; border-radius:10px; color:white; text-align:center;'>"
                f"<h3>Tare Prise</h3><h1>{metrics['tare_prise']}</h1></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div style='background-color:#457B9D; padding:20px; border-radius:10px; color:white; text-align:center;'>"
                f"<h3>En Cours</h3><h1>{metrics['en_cours']}</h1></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div style='background-color:#1D3557; padding:20px; border-radius:10px; color:white; text-align:center;'>"
                f"<h3>Terminé</h3><h1>{metrics['termine']}</h1></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div style='background-color:#A8DADC; padding:20px; border-radius:10px; color:white; text-align:center;'>"
                f"<h3>Total Jour</h3><h1>{metrics['total']}</h1></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tableau des camions
st.subheader("📋 Suivi des flux en temps réel")
df = get_all_pesees()

if not df.empty:
    # Fonction pour colorer le statut
    def highlight_status(val):
        color = '#ffcc00' if val == 'Tare prise' else '#28a745'
        return f'color: {color}; font-weight: bold'

    # Nettoyage de l'affichage
    display_df = df[["matricule_camion", "produit", "poids_tare", "statut", "date_heure_entree"]]
    st.dataframe(display_df.style.applymap(highlight_status, subset=['statut']), use_container_width=True)
else:
    st.info("Aucun camion enregistré aujourd'hui.")
