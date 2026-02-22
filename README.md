# 🗺️ Shortest Path Finder — A* Algorithm

> Application web interactive pour calculer le plus court chemin entre deux points sur une carte réelle (notre code prend pour exemple la wilaya de Bejaia en Algerie, donc assurer vous bien de selectionner deux region de cette wilaya ;), en utilisant une implémentation manuelle de l'algorithme A*.

---

## 📌 Présentation

**Shortest Path Finder** est une application web développée dans le cadre d'un devoir d'Intelligence Artificielle (Assignment 01). Elle permet de visualiser le calcul du plus court chemin sur le réseau routier réel de la **wilaya de Béjaïa** (Algérie), en s'appuyant sur les données OpenStreetMap.

L'algorithme **A\*** est implémenté manuellement (sans librairie externe de pathfinding), avec une heuristique basée sur la distance géodésique entre les nœuds du graphe routier.

---

## ✨ Fonctionnalités clés

- 🖱️ **Sélection interactive** des points de départ et d'arrivée directement sur la carte
- 🧠 **Algorithme A\* implémenté from scratch** avec heuristique géodésique (distance réelle en mètres)
- 🗺️ **Réseau routier réel** chargé depuis OpenStreetMap via OSMnx
- 📍 **Visualisation du chemin** tracé sur la carte avec Folium
- ⚡ Calcul du nœud le plus proche automatiquement pour chaque point cliqué

---

## 🧰 Stack technique

| Composant | Technologie |
|---|---|
| Framework web | Python · Flask |
| Rendu cartographique | Folium |
| Réseau routier OSM | OSMnx |
| Graphes & structure | NetworkX |
| Heuristique distance | Geopy |
| Frontend | HTML · JavaScript |

---

## 🚀 Installation & lancement local

### Prérequis

- Python 3.10+
- pip

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/cynhlfn/Shortest_path_AI_assignment01.git
cd Shortest_path_AI_assignment01

# 2. Créer et activer un environnement virtuel
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
python app.py
```

L'application est accessible sur **http://127.0.0.1:5000**

> ⚠️ Au premier lancement, OSMnx télécharge le graphe routier de la wilaya de Béjaïa depuis OpenStreetMap. Cette opération peut prendre quelques secondes selon la connexion.

---

## 🧩 Structure du projet

```
Shortest_path_AI_assignment01/
├── templates/
│   └── selection_map.html   # Interface carte interactive
├── app.py                   # Serveur Flask + implémentation A*
├── requirements.txt         # Dépendances Python
├── .gitignore
└── README.md
```

---

## 🔬 Comment fonctionne A* ici ?

1. L'utilisateur clique deux points sur la carte (départ & arrivée)
2. OSMnx trouve les **nœuds du graphe routier** les plus proches de chaque clic
3. L'algorithme **A\*** explore les nœuds voisins en priorisant ceux dont `f(n) = g(n) + h(n)` est minimal :
   - `g(n)` : distance réelle parcourue depuis le départ
   - `h(n)` : distance géodésique estimée jusqu'à l'arrivée
4. Le chemin optimal est reconstitué via le tableau des parents et renvoyé au frontend
5. Folium trace le chemin sur la carte en temps réel

---

## 📄 Contexte académique

Projet réalisé dans le cadre du cours d'Intelligence Artificielle — Université de Béjaïa.
