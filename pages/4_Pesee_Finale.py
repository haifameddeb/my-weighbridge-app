import streamlit as st
from database import get_trucks_by_status, finalize_weighing

st.set_page_config(page_title="Étape 4/5 - Pesée Finale", layout="centered")
st.title("⚖️ 4 & 5. Pesée Brute & Sortie")

trucks = get_trucks_by_status('Chargé')

if not trucks.empty:
    options = trucks.apply(lambda x: f"{x['matricule_camion']} (Tare: {x['poids_tare']} KG)", axis=1).tolist()
    selection = st.selectbox("Camion sur la bascule (Sortie)", options)
    
    idx = options.index(selection)
    row = trucks.iloc[idx]
    
    pb = st.number_input("Saisir POIDS BRUT (KG)", min_value=float(row['poids_tare']), step=10.0)
    
    if st.button("VALIDER PESÉE & SORTIE"):
        net = finalize_weighing(row['id'], pb)
        st.write(f"### Poids Net : {net} KG")
        st.success("Mouvement clôturé avec succès.")
        st.balloons()
else:
    st.info("Aucun camion chargé en attente de pesée finale.")
