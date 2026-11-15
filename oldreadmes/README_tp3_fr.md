# TP3 : Expérience contrôlée et analyse des résultats

## Description

Ce TP couvre la collecte, le prétraitement et l'analyse statistique des données issues de l'expérience du TP2. Le rapport final est disponible directement en HTML et PDF, ou reproductible depuis RStudio.

## Consulter les résultats (sans installation)

Les rapports pré-générés sont disponibles directement :
- `logs.html` : ouvrir dans n'importe quel navigateur (code masqué, sections dépliables)
- `logs.pdf` : ouvrir dans un lecteur PDF (code source visible)

## Reproduire l'analyse dans RStudio

1. Installer [R](https://cran.r-project.org/) et [RStudio](https://posit.co/download/rstudio-desktop/)
2. Ouvrir `TP LOGS.Rproj` dans RStudio
3. Ouvrir `logs.Rmd` et cliquer sur **Knit** (ou exécuter cellule par cellule)

Le fichier `data.csv` est déjà présent — aucun prétraitement Python nécessaire pour rejouer l'analyse.

## Structure des fichiers

| Fichier / Dossier | Rôle |
|-------------------|------|
| `logs.Rmd` | Script d'analyse R Markdown — statistiques, visualisations, tests |
| `logs.html` | Rapport généré (HTML, code masqué) |
| `logs.pdf` | Rapport généré (PDF, code visible) |
| `data.csv` | Dataset consolidé de tous les participants, prêt pour R |
| `TP LOGS.Rproj` | Projet RStudio |
| `data final/` | Dossiers bruts par participant (1 à 7) |
| `data final/create_csv.py` | Fusion globale des participants → `data.csv` |

## Format du dataset (`data.csv`)

```
User, Technique, Density, Size, Repetition, Target_ID, Timestamp, Errors, Time_ms
```

## Reconstruire `data.csv` depuis les données brutes (optionnel)

Si besoin de recréer le dataset depuis zéro :

**Étape 1 : Fusionner les données de chaque participant** (dans chaque sous-dossier `data final/X/`) :
```bash
python merge.py
```
Produit `merged_user_X.csv` à partir des trois CSVs bruts (Bubble, Normal, Rope).

**Étape 2 : Fusionner tous les participants** (depuis `data final/`) :
```bash
python create_csv.py
```
Produit `data.csv` (7 participants × 720 lignes = 5 040 lignes attendues) avec vérifications automatiques.