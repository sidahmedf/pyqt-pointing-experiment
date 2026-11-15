# TP1 : Programmation de techniques de pointage

Simulation de trois techniques de pointage interactives développée avec **PyQt5**.

---

## Synopsis

Ce TP implémente et compare trois techniques de pointage classiques en IHM :

- **Curseur normal** :pointage standard, la cible est sélectionnée uniquement si le curseur physique la survole directement.
- **Bubble cursor** : le curseur s'étend dynamiquement pour toujours englober la cible la plus proche, facilitant la sélection.
- **Rope cursor** : variante du bubble cursor qui affiche un trait visuel (la « corde ») reliant le curseur à la cible la plus proche.

Les cibles sont chargées depuis un fichier CSV et affichées dans une fenêtre PyQt5. Un clic sur la cible attendue (en rouge) enregistre le temps de réaction dans la console.

---

## Lancer le projet

### Prérequis

Python 3.x doit être installé. Installer ensuite PyQt5 :

```bash
pip install PyQt5
```

### Exécution

```bash
python main.py
```

Assurez-vous que le fichier `src_tp_bubble.csv` est présent dans le même répertoire que `main.py`. Ce fichier définit les positions et tailles des cibles (format : `id,x,y`).

---

## Changer de technique de pointage

### Changer le widget principal (dans `main.py`)

Par défaut, le widget affiché utilise le **Bubble cursor**. Pour tester une autre technique, modifier les lignes suivantes dans `main.py` :

```python
# Bubble cursor (défaut)
self.display = BubbleWidget()

# Pour le curseur normal — décommenter la ligne ci-dessous et commenter celle du dessus :
# self.display = NormalWidget()
```

### Changer le curseur dans `BubbleWidget` (dans `BubbleWidget.py`)

`BubbleWidget` peut utiliser soit le **Bubble cursor**, soit le **Rope cursor**. Modifier les lignes suivantes dans `BubbleWidget.py` :

```python
# Bubble cursor (défaut)
self.cursor = BubbleCursor(self.targets)

# Pour le Rope cursor — décommenter la ligne ci-dessous et commenter celle du dessus :
# self.cursor = RopeCursor(self.targets)
```

**Récapitulatif des combinaisons possibles :**

| Widget dans `main.py` | Curseur dans `BubbleWidget.py` | Technique affichée |
|---|---|---|
| `BubbleWidget()` | `BubbleCursor` | Bubble cursor |
| `BubbleWidget()` | `RopeCursor` | Rope cursor |
| `NormalWidget()` | *(sans objet)* | Curseur normal |

---

## Architecture

### Vue d'ensemble

```
main.py
├── BubbleWidget  ←→  BubbleCursor
│                 ←→  RopeCursor (étend BubbleCursor)
│                 ←→  Target
└── NormalWidget  ←→  NormalCursor
                  ←→  Target
```

### Description des classes

#### `Target` — `Target.py`
Représente une cible circulaire affichée à l'écran.

- Stocke la position (`x`, `y`) et la taille (`size`) de la cible.
- Gère trois états visuels : **normal** (bleu foncé), **survolé** (vert), **à sélectionner** (rouge).
- Méthode `paint(painter)` : dessine la cible avec la couleur correspondant à son état.

---

#### `BubbleCursor` — `BubbleCursor.py`
Implémente la logique du **bubble cursor**.

- À chaque mouvement de souris, calcule la distance entre le curseur et toutes les cibles.
- Identifie la cible la plus proche (`self.closest`) et ajuste le rayon du curseur pour l'englober exactement.
- Méthode `move(x, y)` : met à jour la position et recalcule la cible englobée.
- Méthode `paint(painter)` : dessine le curseur sous forme de cercle dont le rayon s'adapte dynamiquement.

---

#### `RopeCursor` — `RopeCursor.py`
Variante visuelle du **bubble cursor**, hérite de `BubbleCursor`.

- Surcharge uniquement la méthode `paint(painter)`.
- Au lieu d'un cercle englobant, affiche un **trait** (la corde) entre le curseur et la cible la plus proche, ainsi qu'un petit point à la position du curseur.
- La logique de détection (`move`) est entièrement héritée de `BubbleCursor`.

---

#### `NormalCursor` — `NormalCursor.py`
Implémente le **curseur standard**.

- Détecte la cible survolée uniquement par intersection directe (distance ≤ rayon de la cible).
- Méthode `move(x, y)` : met à jour la position et met en évidence la cible survolée si applicable.
- Méthode `paint(painter)` : dessine un simple point noir.

---

#### `BubbleWidget` — `BubbleWidget.py`
Widget PyQt5 principal pour les techniques **bubble** et **rope**.

- Charge les cibles depuis un CSV via `load_csv()`.
- Gère les événements souris : déplacement (`mouseMoveEvent`) et clic (`mousePressEvent`).
- Sélectionne aléatoirement la prochaine cible à atteindre via `select_new_target()`.
- En mode standalone, affiche le temps de réaction dans la console. En mode géré (`manager`), délègue les résultats au gestionnaire externe (utilisé par le TP2).
- Méthodes `load_scenario()` et `set_active_target()` : extensions pour l'intégration avec le TP2.

---

#### `NormalWidget` — `NormalWidget.py`
Widget PyQt5 équivalent pour le **curseur normal**.

- Même logique que `BubbleWidget`, mais utilise `NormalCursor` à la place.
- La détection de clic vérifie `cursor.hovered_target` au lieu de `cursor.closest`.
- Possède également les méthodes `load_scenario()` et `set_active_target()` pour le TP2.

---

#### `main.py`
Point d'entrée de l'application.

- Crée la fenêtre principale (`MyWindow`, sous-classe de `QMainWindow`).
- Instancie le widget choisi (`BubbleWidget` ou `NormalWidget`) et le définit comme widget central.
- Lance la boucle d'événements PyQt5.