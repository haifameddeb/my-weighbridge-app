import streamlit as st
from database import get_waiting_trucks, update_to_loading

st.set_page_config(page_title="Ordre de Chargement", page_icon="🏗️", layout="wide")

if not st.session_state.get('authenticated', False):
    st.warning("Veuillez vous connecter.")
    st.stop()

st.title("🏗️ Ordre de Chargement (Flux UNAGRO)")

# 1. Récupérer les camions en attente
waiting_df = get_waiting_trucks()

if waiting_df.empty:
    st.info("Aucun camion en attente de chargement (Pesée Tare requise d'abord).")
else:
    # 2. Sélection du camion par matricule
    st.subheader("Sélection du véhicule")
    options = waiting_df.apply(lambda x: f"{x['matricule_camion']} ({x['produit']})", axis=1).tolist()
    selection = st.selectbox("Choisir un camion à envoyer au chargement", options)
    
    # Récupérer l'ID correspondant à la sélection
    selected_idx = options.index(selection)
    id_to_update = int(waiting_df.iloc[selected_idx]['id'])
    matricule_selected = waiting_df.iloc[selected_idx]['matricule_camion']

    # 3. Choix du Silo
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        silo = st.radio("Affecter à un point de chargement :", ["Silo 01", "Silo 02", "Silo 03", "Quai Export"])
    
    with col2:
        st.info(f"Camion : {matricule_selected}\n\nProduit : {waiting_df.iloc[selected_idx]['produit']}")

    if st.button("CONFIRMER L'ORDRE DE CHARGEMENT", use_container_width=True, type="primary"):
        update_to_loading(id_to_update, silo)
        st.success(f"Ordre envoyé ! Le camion {matricule_selected} est dirigé vers le {silo}.")
        st.balloons()
        # Optionnel : redirection vers le dashboard pour voir le changement
        # st.switch_page("app.py")
