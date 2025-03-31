import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
import pandas as pd
from urllib.parse import urlparse
import os

class SegmentationURL:
    def __init__(self, root):
        self.root = root
        self.root.title("Segmentation des URLs")
        self.root.geometry("800x600")
        self.root.configure(padx=20, pady=20)
        
        # Variables
        self.fichier_importe = None
        self.df = None
        self.colonne_selectionee = None
        
        # Création de l'interface
        self.creer_interface()
    
    def creer_interface(self):
        # Titre
        titre = tk.Label(self.root, text="Segmentation des URLs", font=("Arial", 16, "bold"))
        titre.pack(pady=10)
        
        # Notebook (onglets)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, pady=10)
        
        # Onglet 1: Import et segmentation
        self.tab_import = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_import, text="Import et segmentation")
        
        # Onglet 2: Prévisualisation du résultat
        self.tab_preview = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_preview, text="Prévisualisation")
        
        # Construction de l'onglet d'import
        self.construire_tab_import()
        
        # Construction de l'onglet de prévisualisation (initialement vide)
        self.construire_tab_preview()
    
    def construire_tab_import(self):
        # Section: Pourquoi utiliser ce script ?
        frame_pourquoi = ttk.LabelFrame(self.tab_import, text="Pourquoi utiliser ce script ?")
        frame_pourquoi.pack(fill="x", pady=10)
        
        pourquoi_texte = tk.Label(frame_pourquoi, 
                                 text="Ce script peut être utilisé pour segmenter les URLs en fonction des dossiers présents dans l'URL.",
                                 wraplength=750, justify="left", padx=10, pady=10)
        pourquoi_texte.pack(fill="x")
        
        # Section: Comment utiliser ce script ?
        frame_comment = ttk.LabelFrame(self.tab_import, text="Comment utiliser ce script ?")
        frame_comment.pack(fill="x", pady=10)
        
        comment_texte = tk.Label(frame_comment, justify="left", padx=10, pady=10,
                                wraplength=750,
                                text="1. Importer un fichier Excel / CSV dans la zone d'import de fichier ci-dessous, avec une colonne d'URLs à segmenter (dans le premier onglet).\n\n" +
                                     "2. Une fois le fichier importé, sélectionner la colonne du fichier contenant les URLs à segmenter.\n\n" +
                                     "3. Une fois le fichier mis en forme : cliquer sur \"Télécharger le fichier\".")
        comment_texte.pack(fill="x")
        
        # Section d'import de fichier
        frame_import = ttk.LabelFrame(self.tab_import, text="Importer un fichier Excel / CSV :")
        frame_import.pack(fill="x", pady=10)
        
        bouton_import = tk.Button(frame_import, text="Parcourir les fichiers", command=self.importer_fichier)
        bouton_import.pack(pady=10)
        
        self.label_fichier = tk.Label(frame_import, text="Aucun fichier sélectionné")
        self.label_fichier.pack(pady=5)
        
        # Section de sélection de colonne
        self.frame_selection = ttk.LabelFrame(self.tab_import, text="Sélectionner la colonne contenant les URLs à segmenter")
        self.frame_selection.pack(fill="x", pady=10)
        self.frame_selection.pack_forget()  # Caché jusqu'à ce qu'un fichier soit importé
        
        # Section de lancement de l'analyse
        self.frame_analyse = ttk.LabelFrame(self.tab_import, text="Lancer l'analyse")
        self.frame_analyse.pack(fill="x", pady=10)
        self.frame_analyse.pack_forget()  # Caché jusqu'à ce qu'une colonne soit sélectionnée
        
        self.bouton_analyse = tk.Button(self.frame_analyse, text="Segmenter les URLs", command=self.segmenter_urls)
        self.bouton_analyse.pack(pady=10)
        
        # Section de téléchargement
        self.frame_telechargement = ttk.LabelFrame(self.tab_import, text="Télécharger le fichier")
        self.frame_telechargement.pack(fill="x", pady=10)
        self.frame_telechargement.pack_forget()  # Caché jusqu'à ce que l'analyse soit faite
        
        self.bouton_telechargement = tk.Button(self.frame_telechargement, text="Télécharger le fichier", command=self.telecharger_fichier)
        self.bouton_telechargement.pack(pady=10)
    
    def construire_tab_preview(self):
        # Zone d'information
        info_label = tk.Label(self.tab_preview, text="Prévisualisation des données segmentées")
        info_label.pack(pady=10)
        
        # Frame pour la table
        frame_table = ttk.Frame(self.tab_preview)
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Création du treeview (tableau)
        columns = ["URL", "Protocole", "Domaine"]
        self.treeview = ttk.Treeview(frame_table, columns=columns, show='headings')
        
        # Configurer les en-têtes
        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=200)
        
        # Ajouter des barres de défilement
        scrollbar_y = ttk.Scrollbar(frame_table, orient="vertical", command=self.treeview.yview)
        scrollbar_x = ttk.Scrollbar(frame_table, orient="horizontal", command=self.treeview.xview)
        self.treeview.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Placer les widgets
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.treeview.pack(side="left", fill="both", expand=True)
        
        # Bouton pour télécharger les données depuis cet onglet
        bouton_telecharger = tk.Button(self.tab_preview, text="Télécharger le fichier", command=self.telecharger_fichier)
        bouton_telecharger.pack(pady=10)
    
    def importer_fichier(self):
        filetypes = [
            ("Fichiers Excel", "*.xlsx *.xls"),
            ("Fichiers CSV", "*.csv"),
            ("Tous les fichiers", "*.*")
        ]
        fichier = filedialog.askopenfilename(filetypes=filetypes)
        
        if fichier:
            self.fichier_importe = fichier
            nom_fichier = os.path.basename(fichier)
            self.label_fichier.config(text=f"Fichier sélectionné : {nom_fichier}")
            
            # Charger le fichier
            try:
                if fichier.endswith('.csv'):
                    self.df = pd.read_csv(fichier)
                else:
                    self.df = pd.read_excel(fichier)
                    
                # Afficher le sélecteur de colonne
                self.afficher_selecteur_colonne()
                
                # Informer l'utilisateur
                messagebox.showinfo("Importation réussie", 
                                   f"Le fichier a été importé avec succès.\nNombre de lignes : {len(self.df)}\nNombre de colonnes : {len(self.df.columns)}")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'importation du fichier : {str(e)}")
    
    def afficher_selecteur_colonne(self):
        # Vider le frame si des widgets existent déjà
        for widget in self.frame_selection.winfo_children():
            widget.destroy()
        
        # Afficher le frame
        self.frame_selection.pack(fill="x", pady=10)
        
        # Créer le combobox avec les noms de colonnes
        colonnes = self.df.columns.tolist()
        
        label_colonne = tk.Label(self.frame_selection, text="Sélectionner la colonne :")
        label_colonne.pack(pady=5)
        
        self.combobox_colonnes = ttk.Combobox(self.frame_selection, values=colonnes)
        self.combobox_colonnes.pack(pady=5)
        
        # Si 'Adresse' ou 'URL' existe dans les colonnes, le sélectionner par défaut
        for col_default in ['Adresse', 'URL', 'adresse', 'url']:
            if col_default in colonnes:
                self.combobox_colonnes.set(col_default)
                break
        
        bouton_valider = tk.Button(self.frame_selection, text="Valider", command=self.valider_colonne)
        bouton_valider.pack(pady=5)
    
    def valider_colonne(self):
        colonne = self.combobox_colonnes.get()
        
        if colonne and colonne in self.df.columns:
            self.colonne_selectionee = colonne
            messagebox.showinfo("Information", f"Colonne '{colonne}' sélectionnée. Vous pouvez maintenant lancer la segmentation.")
            
            # Afficher la section d'analyse
            self.frame_analyse.pack(fill="x", pady=10)
            
            # Information
            info_texte = tk.Label(self.frame_analyse, 
                                  text=f"Cliquer sur le bouton ci-dessous pour segmenter les URLs de la colonne '{colonne}'.",
                                  wraplength=750, justify="left", padx=10, pady=5)
            info_texte.pack(fill="x")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner une colonne valide.")
    
    def segmenter_url(self, url):
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
    
    def segmenter_urls(self):
        if not self.df is not None or not self.colonne_selectionee:
            messagebox.showerror("Erreur", "Veuillez d'abord importer un fichier et sélectionner une colonne.")
            return
        
        try:
            # Créer un nouveau DataFrame avec l'URL d'origine
            df_resultat = pd.DataFrame()
            df_resultat['URL'] = self.df[self.colonne_selectionee]
            
            # Segmenter chaque URL
            segments_list = []
            max_dossiers = 0
            
            for url in self.df[self.colonne_selectionee]:
                segments = self.segmenter_url(url)
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
            
            # Stocker le résultat
            self.df_resultat = df_resultat
            
            # Mettre à jour la prévisualisation
            self.mettre_a_jour_preview()
            
            # Afficher un aperçu
            messagebox.showinfo("Segmentation terminée", 
                               f"Segmentation terminée avec succès! {len(df_resultat)} URLs ont été segmentées.\n\n" +
                               "Vous pouvez maintenant prévisualiser les résultats dans l'onglet Prévisualisation et télécharger le fichier.")
            
            # Afficher la section de téléchargement
            self.frame_telechargement.pack(fill="x", pady=10)
            
            # Passer à l'onglet de prévisualisation
            self.notebook.select(self.tab_preview)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la segmentation des URLs : {str(e)}")
    
    def mettre_a_jour_preview(self):
        # Vider la table existante
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Récupérer les en-têtes des colonnes
        columns = self.df_resultat.columns.tolist()
        
        # Configurer les colonnes du treeview
        self.treeview["columns"] = columns
        
        # Configurer les en-têtes
        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=150)
        
        # Ajouter les données (limité à 100 lignes pour la performance)
        max_rows = min(100, len(self.df_resultat))
        for i in range(max_rows):
            values = self.df_resultat.iloc[i].tolist()
            self.treeview.insert("", "end", values=values)
        
        # Ajouter un message si plus de lignes existent
        if len(self.df_resultat) > max_rows:
            restant = len(self.df_resultat) - max_rows
            self.treeview.insert("", "end", values=[f"... et {restant} lignes supplémentaires"] + [""] * (len(columns) - 1))
    
    def telecharger_fichier(self):
        if not hasattr(self, 'df_resultat'):
            messagebox.showerror("Erreur", "Aucun résultat à télécharger. Veuillez d'abord effectuer la segmentation.")
            return
        
        # Demander à l'utilisateur où enregistrer le fichier
        filetypes = [
            ("Fichier Excel", "*.xlsx"),
            ("Fichier CSV", "*.csv")
        ]
        fichier_sortie = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=filetypes)
        
        if fichier_sortie:
            try:
                # Enregistrer selon l'extension
                if fichier_sortie.endswith('.csv'):
                    self.df_resultat.to_csv(fichier_sortie, index=False)
                else:
                    self.df_resultat.to_excel(fichier_sortie, index=False)
                
                messagebox.showinfo("Succès", f"Le fichier a été enregistré avec succès à l'emplacement :\n{fichier_sortie}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement du fichier : {str(e)}")

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = SegmentationURL(root)
    root.mainloop()
