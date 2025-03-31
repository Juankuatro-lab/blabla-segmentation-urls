# Outil de Segmentation d'URLs

Ce projet propose un outil pour segmenter les URLs en fonction des dossiers présents dans le chemin. Il transforme un fichier contenant des URLs en un tableau structuré avec les différentes parties de chaque URL (protocole, domaine, dossiers).

## Fonctionnalités

- Import de fichiers Excel (.xlsx, .xls) et CSV
- Sélection de la colonne contenant les URLs
- Segmentation automatique des URLs en :
  - Protocole (http, https)
  - Domaine
  - Dossiers (niveau 1, 2, 3, etc.)
- Prévisualisation des résultats
- Téléchargement des résultats au format Excel ou CSV
- Statistiques sur les URLs traitées

## Prérequis

- Python 3.7 ou supérieur
- Les bibliothèques listées dans `requirements.txt`

## Installation

1. Clonez ce dépôt ou téléchargez les fichiers source
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Version Streamlit (recommandée)

1. Lancez l'application :
   ```bash
   streamlit run segmentation_urls_app.py
   ```

2. Ouvrez votre navigateur à l'adresse indiquée (généralement http://localhost:8501)

3. Suivez les instructions à l'écran :
   - Importez votre fichier Excel ou CSV
   - Sélectionnez la colonne contenant les URLs
   - Cliquez sur "Segmenter les URLs"
   - Visualisez les résultats et téléchargez le fichier

### Version en ligne de commande (alternative)

Pour une utilisation rapide ou automatisée :

```bash
python segmentation_url_cli.py chemin/vers/fichier.xlsx nom_colonne -o chemin/vers/sortie.xlsx
```

## Déploiement

Pour rendre l'application accessible à d'autres utilisateurs, vous pouvez la déployer sur Streamlit Cloud :

1. Créez un compte sur [streamlit.io](https://streamlit.io/)
2. Connectez votre repository GitHub à Streamlit Cloud
3. Configurez le déploiement et partagez l'URL avec vos utilisateurs

## Structure des fichiers

- `segmentation_urls_app.py` : Application principale (Streamlit)
- `segmentation_url_cli.py` : Version en ligne de commande
- `requirements.txt` : Liste des dépendances
- `README.md` : Documentation

## Notes techniques

L'outil utilise la bibliothèque `urlparse` de Python pour décomposer les URLs de manière fiable. Il peut gérer différents formats d'URL, y compris ceux contenant des caractères spéciaux ou des paramètres de requête.

## Résolution des problèmes

### "Module not found"

Si vous rencontrez une erreur de module manquant :
```
pip install -r requirements.txt
```

### "Could not find a version that satisfies the requirement"

Si vous avez des problèmes avec les versions des packages :
```
pip install --upgrade pip
pip install -r requirements.txt
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à proposer une pull request pour améliorer cet outil.
