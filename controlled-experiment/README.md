# TP2 : Programmation d'une expérience contrôlée

## Description

Ce TP met en place une expérience contrôlée pour comparer les trois techniques de pointage implémentées en TP1 (Bubble, Rope, Normal). Le logiciel séquence automatiquement les conditions expérimentales pour chaque participant et enregistre les résultats dans des fichiers CSV.

## Prérequis

- Python 3.x avec PyQt5
- Le dossier `TP1/` doit être présent (version locale isolée — ne pas modifier le TP1 original)
- Les fichiers de cibles et de séquences doivent être générés avant le lancement (voir ci-dessous)

## Étape 1 : Générer les fichiers de cibles

Avant de lancer l'expérience, il faut générer les fichiers CSV de cibles et de séquences pour chaque combinaison de conditions. La configuration utilisée est :

| Paramètre | Valeurs |
|-----------|---------|
| Tailles de cibles | 8 px, 18 px |
| Densités | 30, 90 |
| Techniques | Bubble, Rope, Normal |
| Répétitions | 3 |
| Cibles par répétition | 20 |

Lancer la commande suivante pour chaque combinaison densité/taille :

```bash
python generate_files.py -n <densité> -s <taille> -m 10
```

Exemple pour les 4 combinaisons :

```bash
python generate_files.py -n 30 -s 8 -m 10
python generate_files.py -n 30 -s 18 -m 10
python generate_files.py -n 90 -s 8 -m 10
python generate_files.py -n 90 -s 18 -m 10
```

Cela génère les fichiers `targets_<n>_<s>.csv` et `sequence_<n>_<s>.csv` dans le répertoire courant.

## Étape 2 : Lancer l'expérience

```bash
python MainExp.py
```


Une fenêtre de configuration s'ouvre. Renseigner :
- L'identifiant du participant (User ID)
- La technique à tester (Bubble / Rope / Normal)
- Le nombre de répétitions

### Note sur les fichiers de lancement

Deux fichiers `main.py` et `MainExp.py` sont présents dans le répertoire.

- `main.py` — version intermédiaire conservée pour traçabilité, le dialog s'ouvre mais l'expérience ne se lance pas réellement.
- `MainExp.py` — **point d'entrée à utiliser**, branche le widget de pointage et le gestionnaire d'essais.

> Toujours lancer l'expérience via `python MainExp.py`.

## Structure des fichiers

| Fichier | Rôle |
|---------|------|
| `MainExp.py` | Point d'entrée principal de l'expérience |
| `ExpSetup.py` | Dialogue de configuration (User ID, technique, répétitions…) |
| `XPManager.py` | Gestion du déroulement des essais, séquencement, logging CSV |
| `generate_files.py` | Générateur de fichiers de cibles et de séquences |
| `TP1/` | Copie locale des widgets de pointage (BubbleWidget, RopeWidget, NormalWidget) |
| `results/` | Dossier créé automatiquement, contient les CSV de résultats par participant |

## Format des résultats

Les résultats sont sauvegardés dans `results/user_<id>_<technique>_<timestamp>.csv` avec les colonnes :

```
User, Technique, Density, Size, Repetition, Target_ID, Timestamp, Errors, Time_ms
```