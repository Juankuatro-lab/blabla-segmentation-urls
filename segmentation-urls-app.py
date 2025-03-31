import streamlit as st
import pandas as pd
from urllib.parse import urlparse
import io
import base64

# Configuration de la page
st.set_page_config(
    page_title="Segmentation des URLs",
    page_icon="🔗",
    layout="wide"
)

# Fonctions
def segmenter_url(url):
    """Segmente une URL en ses différentes parties."""
    if not url or not isinstance(url, str):
        return {}
    
    try:
        parsed = urlparse(url)
        resultat = {}
        
        # Protocole (http, https)
        resultat['Protocole'] = parsed.scheme
        
        # Domaine
        resultat['Domaine'] = parsed.netloc
        
        # Chemin segmenté
        chemin = parsed.path.strip('/')
        parties_chemin = chemin.split('/')
        
        for i, partie in enumerate(parties_chemin):
            if partie:  # S'assurer que la partie n'est pas vide
                resultat[f'Dossier_{i+1}'] = partie
        
        return resultat
    except:
        return {}

def segmenter_urls_dataframe(df, colonne):
    """Segmente toutes les URLs d'un DataFrame."""
    # Créer un nouveau DataFrame avec l'URL d'origine
    df_resultat = pd.DataFrame()
    df_resultat['URL'] = df[colonne]
    
    # Segmenter chaque URL
    segments_list = []
    max_dossiers = 0
    
    for url in df[colonne]:
        segments = segmenter_url(url)
        segments_list.append(segments)
        
        # Garder trace du nombre maximum de dossiers
        dossiers_count = sum(1 for k in segments.keys() if k.startswith('Dossier_'))
        max_dossiers = max(max_dossiers, dossiers_count)
    
    # Ajouter les colonnes obligatoires
    df_resultat['Protocole'] = [s.get('Protocole', '') for s in segments_list]
    df_resultat['Domaine'] = [s.get('Domaine', '') for s in segments_list]
    
    # Ajouter les colonnes de dossiers
    for i in range(1, max_dossiers + 1):
        dossier_key = f'Dossier_{i}'
        df_resultat[dossier_key] = [s.get(dossier_key, '') for s in segments_list]
    
    return df_resultat

def get_table_download_link(df, filename="segmentation_urls.xlsx", link_text="Télécharger le fichier Excel"):
    """Génère un lien de téléchargement pour le DataFrame."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    b64 = base64.b64encode(output.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

# Interface utilisateur
st.title("Segmentation des URLs")

# Informations
with st.expander("Pourquoi utiliser ce script ?", expanded=True):
    st.write("Ce script peut être utilisé pour segmenter les URLs en fonction des dossiers présents dans l'URL.")

with st.expander("Comment utiliser ce script ?", expanded=True):
    st.write("""
    1. Importer un fichier Excel / CSV dans la zone d'import de fichier ci-dessous, avec une colonne d'URLs à segmenter (dans le premier onglet).
    2. Une fois le fichier importé, sélectionner la colonne du fichier contenant les URLs à segmenter.
    3. Une fois le fichier mis en forme : cliquer sur "Télécharger le fichier".
    """)

# Import de fichier
st.subheader("Importer un fichier Excel / CSV :")
uploaded_file = st.file_uploader("", type=["xlsx", "csv"])

if uploaded_file is not None:
    # Lecture du fichier
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"Fichier importé avec succès : {uploaded_file.name}")
        st.write(f"Nombre de lignes : {len(df)}, Nombre de colonnes : {len(df.columns)}")
        
        # Sélection de la colonne
        st.subheader("Sélectionner la colonne contenant les URLs à segmenter")
        colonnes = df.columns.tolist()
        
        # Essayer de détecter automatiquement la colonne URL
        default_col_index = 0
        for i, col in enumerate(colonnes):
            if col.lower() in ['adresse', 'url', 'lien', 'link']:
                default_col_index = i
                break
        
        colonne_selectionnee = st.selectbox("", colonnes, index=default_col_index)
        
        # Bouton pour lancer la segmentation
        if st.button("Segmenter les URLs"):
            with st.spinner("Segmentation en cours..."):
                # Segmenter les URLs
                df_resultat = segmenter_urls_dataframe(df, colonne_selectionnee)
                
                # Afficher un aperçu du résultat
                st.subheader("Aperçu des URLs segmentées")
                st.dataframe(df_resultat.head(10))
                
                # Afficher les statistiques
                nb_urls = len(df_resultat)
                nb_protocoles = df_resultat['Protocole'].nunique()
                nb_domaines = df_resultat['Domaine'].nunique()
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Nombre d'URLs", nb_urls)
                col2.metric("Protocoles uniques", nb_protocoles)
                col3.metric("Domaines uniques", nb_domaines)
                
                # Proposer le téléchargement
                st.subheader("Télécharger le résultat")
                st.markdown(get_table_download_link(df_resultat), unsafe_allow_html=True)
                
                # Sauvegarder dans la session
                st.session_state.df_resultat = df_resultat
    
    except Exception as e:
        st.error(f"Erreur lors de l'importation ou du traitement du fichier: {str(e)}")
