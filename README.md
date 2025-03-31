# Guide d'installation et d'utilisation de l'outil de segmentation d'URLs

## À propos de l'outil

Cet outil permet de segmenter les URLs en fonction des dossiers présents dans l'URL. Il prend en entrée un fichier Excel ou CSV contenant une colonne d'URLs, et génère un nouveau fichier avec les URLs segmentées (protocole, domaine, dossiers).

## Prérequis

Pour utiliser cet outil, vous aurez besoin d'installer :

1. **Python 3.7 ou plus récent**
   - Téléchargez Python depuis [python.org](https://www.python.org/downloads/)
   - Assurez-vous de cocher l'option "Add Python to PATH" lors de l'installation

2. **Les bibliothèques nécessaires**
   - Pandas : pour la manipulation de données tabulaires
   - Openpyxl : pour la gestion des fichiers Excel

## Installation

1. **Téléchargez les fichiers sources**

2. **Installez les dépendances**
   
   Ouvrez un terminal (Invite de commandes sur Windows) et exécutez :
   ```
   pip install pandas openpyxl
   ```

## Utilisation

### Version avec interface graphique (GUI)

1. **Lancez l'application**
   
   Double-cliquez sur le fichier `segmentation_url_gui.py` ou exécutez-le depuis un terminal :
   ```
   python segmentation_url_gui.py
   ```

2. **Importez votre fichier**
   
   - Cliquez sur "Parcourir les fichiers" et sélectionnez votre fichier Excel ou CSV contenant les URLs à segmenter
   - Le fichier doit contenir une colonne avec les URLs (comme "Adresse" ou "URL")

3. **Sélectionnez la colonne contenant les URLs**
   
   - Dans la liste déroulante, choisissez la colonne qui contient vos URLs
   - Cliquez sur "Valider"

4. **Lancez la segmentation**
   
   - Cliquez sur "Segmenter les URLs"
   - Attendez que le traitement soit terminé

5. **Prévisualisez les résultats**
   
   - L'onglet "Prévisualisation" s'affiche automatiquement pour montrer un aperçu des résultats
   - Vous pouvez consulter les premières lignes du fichier segmenté

6. **Téléchargez le résultat**
   
   - Cliquez sur "Télécharger le fichier"
   - Choisissez l'emplacement et le format (Excel ou CSV) où enregistrer le fichier
   - Cliquez sur "Enregistrer"

### Version en ligne de commande

Pour une utilisation rapide ou dans des scripts automatisés, vous pouvez utiliser la version en ligne de commande :

```
python segmentation_url_cli.py chemin/vers/fichier.xlsx nom_colonne -o chemin/vers/sortie.xlsx
```

Options :
- `chemin/vers/fichier.xlsx` : le chemin vers votre fichier d'entrée (Excel ou CSV)
- `nom_colonne` : le nom de la colonne contenant les URLs
- `-o chemin/vers/sortie.xlsx` : (optionnel) le chemin du fichier de sortie. Si non spécifié, un nom par défaut sera généré.

## Format de sortie

Le fichier de sortie contiendra :
- Une colonne "URL" contenant les URLs d'origine
- Une colonne "Protocole" avec le protocole (http, https)
- Une colonne "Domaine" avec le nom de domaine
- Une série de colonnes "Dossier_1", "Dossier_2", etc. contenant les différents segments du chemin

## Résolution des problèmes courants

### "Module not found"
Si vous obtenez une erreur "No module named...", assurez-vous d'avoir bien installé les dépendances :
```
pip install pandas openpyxl
```

### Problèmes de lecture de fichier
- Vérifiez que votre fichier n'est pas ouvert dans Excel ou un autre programme
- Assurez-vous que le fichier est bien au format Excel (.xlsx, .xls) ou CSV (.csv)
- Pour les fichiers CSV, vérifiez l'encodage (UTF-8 recommandé)

### URLs mal segmentées
- Les URLs doivent être complètes et commencer par http:// ou https://
- L'outil gère automatiquement les caractères spéciaux et les espaces dans les URLs

## Personnalisation

Vous pouvez modifier le code source pour adapter l'outil à vos besoins spécifiques :
- Ajouter des colonnes supplémentaires (paramètres d'URL, fragment, etc.)
- Modifier le format de sortie
- Ajouter des fonctionnalités comme l'extraction de statistiques sur les URLs
