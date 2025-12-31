import streamlit as st
import pandas as pd
import sqlite3

# Configuration
st.set_page_config(page_title="Logistique Camions", layout="wide")

def get_stats():
    # Liste fixe des statuts selon votre workflow
    statuts_reference = [
        "Tare prise", 
        "Ordre de chargement", 
        "En cours de chargement", 
        "Fin de chargement", 
        "Pesée effectuée"
    ]
    
    try:
        conn = sqlite3.connect('logistique.db')
        df_real = pd.read_sql("SELECT STATUT, COUNT(*) as NB FROM flux_camions GROUP BY STATUT", conn)
        conn.close()
    except:
        # Si la table n'existe pas encore
        df_real = pd.DataFrame(columns=['STATUT', 'NB'])

    # Fusion avec la liste de référence pour garantir l'affichage des zéros
    df_ref = pd.DataFrame({'STATUT': statuts_reference})
    df_final = pd.merge(df_ref, df_real, on='STATUT', how='left').fillna(0)
    df_final['NB'] = df_final['NB'].astype(int)
    
    return df_final

# --- AUTHENTIFICATION ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Connexion")
    with st.container():
        user = st.text_input("Identifiant")
        pw = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter", use_container_width=True):
            if user == "admin" and pw == "admin":
                st.session_state.auth = True
                st.rerun()
else:
    # --- TABLEAU DE BORD ---
    st.title("📊 Tableau de Bord - Suivi en Temps Réel")
    st.markdown("---")
    
    stats = get_stats()
    
    # Création de 5 colonnes pour l'ergonomie
    cols = st.columns(5)
    
    # Couleurs et icônes pour chaque étape
    icons = ["🚛", "📝", "⏳", "✅", "⚖️"]
    
    for i, row in stats.iterrows():
        with cols[i]:
            # Utilisation d'un container pour styliser l'affichage
            st.metric(
                label=f"{icons[i]} {row['STATUT']}", 
                value=row['NB']
            )
    
    st.markdown("---")
    
    # Optionnel : Vue détaillée
    if st.checkbox("Afficher le détail des camions par statut"):
        conn = sqlite3.connect('logistique.db')
        df_all = pd.read_sql("SELECT CAMION, TRANSPORTEUR, STATUT, DH_TARE FROM flux_camions", conn)
        conn.close()
        st.dataframe(df_all, use_container_width=True)

    st.sidebar.success("Connecté : Admin")



