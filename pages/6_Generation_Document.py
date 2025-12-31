import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from database import init_db

# Sécurité : Vérification authentification
if 'auth' not in st.session_state or not st.session_state.auth:
    st.warning("⚠️ Accès refusé. Veuillez vous connecter sur la page d'accueil.")
    st.stop()

init_db()

st.title("📄 Créer document")

conn = sqlite3.connect('logistique.db')

# On récupère les camions ayant terminé la pesée finale
query = "SELECT CAMION, TRANSPORTEUR, ARTICLE, POIDS_NET FROM flux_camions WHERE STATUT='Pesée effectuée'"
df_pret = pd.read_sql(query, conn)

if not df_pret.empty:
    # 1. Sélection du camion
    camion_sel = st.selectbox("Sélectionnez le camion pour le document", df_pret['CAMION'])
    
    # Récupération des données liées au camion sélectionné
    infos_camion = df_pret[df_pret['CAMION'] == camion_sel].iloc[0]
    st.info(f"Détails : {infos_camion['TRANSPORTEUR']} | {infos_camion['ARTICLE']} | {infos_camion['POIDS_NET']} kg")

    st.markdown("---")

    # 2. Formulaire conforme à la maquette
    fournisseur = st.text_input("Fournisseur", value="Fournisseur X")
    num_cmd_fourn = st.text_input("N° commande fournisseur", value="PO-2025-441")
    
    bl_client = st.toggle("BL client ?", value=True)
    
    # Champs optionnels ou grisés si BL client est décoché (optionnel)
    code_client = st.text_input("Code client", value="C12345", disabled=not bl_client)
    raison_sociale = st.text_input("Raison sociale", value="Société Client SA", disabled=not bl_client)
    num_cmd_client = st.text_input("Commande client", value="CL-2025-0098", disabled=not bl_client)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Retour", use_container_width=True):
            st.switch_page("app.py")
            
    with col2:
        if st.button("Générer document", type="primary", use_container_width=True):
            try:
                dh_gen = datetime.now().strftime("%d/%m/%Y %H:%M")
                
                # Enregistrement dans la table documents_generes
                conn.execute("""INSERT INTO documents_generes 
                             (CAMION, FOURNISSEUR, NUM_CMD_FOURN, IS_BL_CLIENT, CODE_CLIENT, RAISON_SOCIALE, NUM_CMD_CLIENT, DH_GENERATION) 
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                             (camion_sel, fournisseur, num_cmd_fourn, 1 if bl_client else 0, code_client, raison_sociale, num_cmd_client, dh_gen))
                
                # Mise à jour du statut du camion
                conn.execute("UPDATE flux_camions SET STATUT='Terminé' WHERE CAMION=?", (camion_sel,))
                
                conn.commit()
                st.success(f"✅ Document généré avec succès pour le camion {camion_sel} !")
                st.balloons()
                st.rerun()
                
            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")

else:
    st.info("Aucun camion n'est en attente de génération de document (Statut 'Pesée effectuée' requis).")

conn.close()
# --- Affichage des documents déjà générés (à ajouter à la fin du fichier) ---
st.markdown("---")
st.subheader("📋 Historique des documents générés")

try:
    # On rouvre une connexion pour la lecture
    conn_hist = sqlite3.connect('logistique.db')
    
    # Requête pour récupérer les documents avec les infos clés
    query_hist = """
        SELECT ID_DOC, CAMION, FOURNISSEUR, NUM_CMD_FOURN, RAISON_SOCIALE, DH_GENERATION 
        FROM documents_generes 
        ORDER BY ID_DOC DESC
    """
    df_hist = pd.read_sql(query_hist, conn_hist)
    conn_hist.close()

    if not df_hist.empty:
        # Renommage des colonnes pour un affichage propre
        df_hist.columns = ["ID", "Matricule", "Fournisseur", "N° Commande F.", "Client", "Date Génération"]
        
        # Affichage sous forme de tableau interactif
        st.dataframe(df_hist, use_container_width=True, hide_index=True)
    else:
        st.info("Aucun document n'a encore été généré.")

except Exception as e:
    st.error(f"Erreur lors de la lecture de l'historique : {e}")
