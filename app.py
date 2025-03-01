print("Début du script...")

from flask import Flask, render_template, request, jsonify
import folium
import osmnx as ox
import networkx as nx
import heapq
from geopy.distance import geodesic
import math

app = Flask(__name__)

# le graphe de alger (comme exemple)
region = "Alger, Algeria"  # a modifier selon la région souhaitée

print("Téléchargement du graphe en cours...")
try:
    G = ox.graph_from_place(region, network_type="drive")
    print("Graphe téléchargé avec succès !")
except Exception as e:
    print(f"Erreur lors du téléchargement du graphe : {e}")
    exit(1)



@app.route('/')
def home():
    print("Accès à la page d'accueil")
    # Créer une carte centrée sur Alger
    m = folium.Map(location=[36.7410995, 3.1208536], zoom_start=12)
    # Convertir la carte en HTML
    map_html = m._repr_html_()
    return render_template("selection_map.html", map_html=map_html)


def heuristic(a, b):
    return geodesic((G.nodes[a]['y'], G.nodes[a]['x']), (G.nodes[b]['y'], G.nodes[b]['x'])).meters

def A_star_algo(G, start, goal):
    q = []
    heapq.heappush(q, (0, start))
    #utiliser 'parents' pour memoriser le parent de chaque element ajouté
    parents = {}
    #initialiser la fonciton 'g' et 'f' a plus l'infini pour chaque noeud 
    g = {node: float('inf') for node in  G.nodes}
    f = {node: float('inf') for node in  G.nodes}
    g[start] = 0
    f[start] = heuristic(start, goal)


    while q:
        a, curr = heapq.heappop(q)
        if curr == goal:
            resultpath = []
            while curr in parents:
                resultpath.append(curr)
                curr = parents[curr]
            resultpath.append(start)
            resultpath.reverse()
            return resultpath
        
        for n in G.neighbors(curr):
            new_g = g[curr] + min(edge['length'] for edge in G[curr][n].values())
            if new_g < g[n] :
                parents[n] = curr
                g[n] = new_g
                f[n] = g[n] + heuristic(n, goal)
                heapq.heappush(q, (f[n], n))
    return None





@app.route('/shortest_path', methods=['POST'])
def shortest_path():
    data = request.get_json()
    start = tuple(data.get("start")) 
    goal = tuple(data.get("goal")) 

    if not start or not goal:
        return jsonify({"error": "Veuillez sélectionner un point de départ et un point d'arrivée"}), 400

    print(f"Départ : {start}, Arrivée : {goal}")

    try:
        # Trouver les nœuds les plus proches
        orig_node = ox.distance.nearest_nodes(G, start[1], start[0])
        dest_node = ox.distance.nearest_nodes(G, goal[1], goal[0])
        print(f"Nœud départ : {orig_node}, Nœud arrivée : {dest_node}")

        # Calculer le plus court chemin
        shortest_path_nodes = A_star_algo(G, orig_node, dest_node)   
        print(f"Chemin trouvé : {shortest_path_nodes}")
        if shortest_path_nodes is None:
            return jsonify({"error": "A* could not find a path between the selected points."}), 400


        # Convertion en lat, long
        path_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path_nodes]
        return jsonify({"path": path_coords})

    except Exception as e:
        print(f"Erreur lors du calcul du chemin : {e}")
        return jsonify({"error": "Problème lors du calcul du chemin."}), 500


if __name__ == "__main__":
    print("Lancement de Flask sur http://127.0.0.1:5000/")
    app.run(host="0.0.0.0", port=5000, debug=True) 
