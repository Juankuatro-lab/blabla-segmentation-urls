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
        
        # Domaine et sous-domaine
        domaine_complet = parsed.netloc
        resultat['Domaine'] = domaine_complet
        
        # Tenter d'extraire le sous-domaine
        parties_domaine = domaine_complet.split('.')
        if len(parties_domaine) > 2:
            resultat['Sous-domaine'] = '.'.join(parties_domaine[:-2])
        else:
            resultat['Sous-domaine'] = ''
        
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
    df_resultat['Sous-domaine'] = [s.get('Sous-domaine', '') for s in segments_list]
    
    # Ajouter les colonnes de dossiers
    for i in range(1, max_dossiers + 1):
        dossier_key = f'Dossier_{i}'
        df_resultat[dossier_key] = [s.get(dossier_key, '') for s in segments_list]
    
    return df_resultat

def creer_feuille_analyse_par_sous_domaine(df_segmente):
    """Crée un DataFrame pour l'analyse par sous-domaine."""
    
    # Grouper par sous-domaine et domaine, et compter le nombre de pages
    df_sous_domaines = df_segmente.groupby(['Sous-domaine', 'Domaine']).size().reset_index(name='Nombre de pages')
    
    # Si le sous-domaine est vide, le remplacer par "(domaine principal)"
    df_sous_domaines['Sous-domaine'] = df_sous_domaines['Sous-domaine'].replace('', '(domaine principal)')
    
    # Trier par nombre de pages décroissant
    df_sous_domaines = df_sous_domaines.sort_values('Nombre de pages', ascending=False)
    
    return df_sous_domaines

def creer_analyse_par_sous_repertoire(df_segmente, niveau_max=10):
    """Crée des DataFrames pour l'analyse par sous-répertoire pour chaque sous-domaine.
    Format optimisé avec une structure plus claire."""
    
    # Dictionnaire pour stocker les analyses par sous-domaine
    analyses_par_sous_domaine = {}
    
    # Obtenir la liste des sous-domaines (y compris le domaine principal)
    sous_domaines = df_segmente['Sous-domaine'].unique()
    
    # Pour chaque sous-domaine
    for sous_domaine in sous_domaines:
        # Créer une étiquette pour le sous-domaine (s'il est vide, utiliser "domaine principal")
        label_sous_domaine = sous_domaine if sous_domaine else '(domaine principal)'
        
        # Filtrer les données pour ce sous-domaine
        df_filtre = df_segmente[df_segmente['Sous-domaine'] == sous_domaine]
        
        # Créer une liste pour stocker les analyses de chaque niveau
        analyses_niveaux = []
        
        # Pour chaque niveau de répertoire
        for niveau in range(1, niveau_max + 1):
            colonne_dossier = f'Dossier_{niveau}'
            
            # Vérifier si ce niveau existe dans les données
            if colonne_dossier in df_filtre.columns:
                # Compter les occurrences de chaque valeur à ce niveau
                if not df_filtre[colonne_dossier].empty and df_filtre[colonne_dossier].notna().any():
                    counts = df_filtre[colonne_dossier].value_counts().reset_index()
                    counts.columns = ['Répertoire', 'Nombre de pages']
                    
                    # Ajouter une colonne pour le niveau
                    counts['Niveau'] = niveau
                    
                    # Ajouter à la liste des analyses
                    analyses_niveaux.append(counts)
        
        # Si nous avons des analyses, les combiner en un seul DataFrame
        if analyses_niveaux:
            df_analyse = pd.concat(analyses_niveaux, ignore_index=True)
            
            # Trier par niveau puis par nombre de pages décroissant
            df_analyse = df_analyse.sort_values(['Niveau', 'Nombre de pages'], ascending=[True, False])
            
            # Réorganiser les colonnes pour plus de clarté
            df_analyse = df_analyse[['Niveau', 'Répertoire', 'Nombre de pages']]
            
            # Stocker l'analyse dans le dictionnaire
            analyses_par_sous_domaine[label_sous_domaine] = df_analyse
        else:
            # Créer un DataFrame vide si pas d'analyse
            analyses_par_sous_domaine[label_sous_domaine] = pd.DataFrame(columns=['Niveau', 'Répertoire', 'Nombre de pages'])
    
    return analyses_par_sous_domaine

def get_table_download_link_with_sheets(df_principal, df_sous_domaines, analyses_repertoires, filename="segmentation_urls.xlsx", link_text="Télécharger le fichier Excel"):
    """Génère un lien de téléchargement pour le fichier Excel avec plusieurs feuilles."""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Feuille principale avec les URLs segmentées
        df_principal.to_excel(writer, sheet_name='URLs segmentées', index=False)
        
        # Feuille d'analyse par sous-domaine
        df_sous_domaines.to_excel(writer, sheet_name='URLs par sous-domaine', index=False)
        
        # Feuilles d'analyse par sous-répertoire pour chaque sous-domaine
        for sous_domaine, df_analyse in analyses_repertoires.items():
            # Limiter la longueur du nom de la feuille à 31 caractères (limite Excel)
            sheet_name = f"Rép. {sous_domaine}"
            if len(sheet_name) > 31:
                sheet_name = sheet_name[:28] + "..."
            
            # Vérifier si le DataFrame n'est pas vide
            if not df_analyse.empty:
                df_analyse.to_excel(writer, sheet_name=sheet_name, index=False)
    
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
                
                # Créer les analyses supplémentaires
                df_sous_domaines = creer_feuille_analyse_par_sous_domaine(df_resultat)
                analyses_repertoires = creer_analyse_par_sous_repertoire(df_resultat)
                
                # Afficher un aperçu du résultat principal
                st.subheader("Aperçu des URLs segmentées")
                st.dataframe(df_resultat.head(10))
                
                # Afficher un aperçu de l'analyse par sous-domaine
                st.subheader("Analyse par sous-domaine")
                st.dataframe(df_sous_domaines)
                
                # Onglets pour les aperçus d'analyse par sous-répertoire
                if analyses_repertoires:
                    st.subheader("Analyse par sous-répertoire")
                    
                    # Créer des onglets pour chaque sous-domaine
                    sous_domaine_tabs = st.tabs(list(analyses_repertoires.keys()))
                    
                    # Afficher l'analyse dans chaque onglet
                    for i, tab in enumerate(sous_domaine_tabs):
                        sous_domaine = list(analyses_repertoires.keys())[i]
                        df_analyse = analyses_repertoires[sous_domaine]
                        
                        with tab:
                            if not df_analyse.empty:
                                st.dataframe(df_analyse)
                            else:
                                st.write("Pas de données de sous-répertoires pour ce sous-domaine.")
                
                # Afficher les statistiques
                nb_urls = len(df_resultat)
                nb_protocoles = df_resultat['Protocole'].nunique()
                nb_domaines = df_resultat['Domaine'].nunique()
                nb_sous_domaines = len([sd for sd in df_resultat['Sous-domaine'].unique() if sd])
                
                st.subheader("Statistiques")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Nombre d'URLs", nb_urls)
                col2.metric("Protocoles uniques", nb_protocoles)
                col3.metric("Domaines uniques", nb_domaines)
                col4.metric("Sous-domaines uniques", nb_sous_domaines)
                
                # Proposer le téléchargement
                st.subheader("Télécharger le résultat")
                st.markdown(
                    get_table_download_link_with_sheets(
                        df_resultat, 
                        df_sous_domaines, 
                        analyses_repertoires
                    ), 
                    unsafe_allow_html=True
                )
                
                # Sauvegarder dans la session
                st.session_state.df_resultat = df_resultat
                st.session_state.df_sous_domaines = df_sous_domaines
                st.session_state.analyses_repertoires = analyses_repertoires
    
    except Exception as e:
        st.error(f"Erreur lors de l'importation ou du traitement du fichier: {str(e)}")
