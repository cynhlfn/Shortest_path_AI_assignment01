import os
import threading
from flask import Flask, render_template, request, jsonify
import folium
import osmnx as ox
import networkx as nx
import heapq
from geopy.distance import geodesic

app = Flask(__name__)

region = "Béjaïa, Algeria"
G = None  # Graphe chargé en arrière-plan

def charger_graphe():
    global G
    print("Téléchargement du graphe en arrière-plan...")
    try:
        # Centre de Béjaïa, rayon de 5km seulement
        G = ox.graph_from_point((36.7509, 5.0564), dist=5000, network_type="drive")
        print("Graphe prêt !")
    except Exception as e:
        print(f"Erreur : {e}")

# Lance le téléchargement dans un thread séparé dès le démarrage
thread = threading.Thread(target=charger_graphe)
thread.daemon = True
thread.start()


@app.route('/')
def home():
    print("Accès à la page d'accueil")
    m = folium.Map(location=[36.7509, 5.0564], zoom_start=12)
    map_html = m._repr_html_()
    return render_template("selection_map.html", map_html=map_html)


def heuristic(a, b):
    return geodesic(
        (G.nodes[a]['y'], G.nodes[a]['x']),
        (G.nodes[b]['y'], G.nodes[b]['x'])
    ).meters


def A_star_algo(G, start, goal):
    q = []
    heapq.heappush(q, (0, start))
    parents = {}
    g = {node: float('inf') for node in G.nodes}
    f = {node: float('inf') for node in G.nodes}
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
            if new_g < g[n]:
                parents[n] = curr
                g[n] = new_g
                f[n] = g[n] + heuristic(n, goal)
                heapq.heappush(q, (f[n], n))
    return None


@app.route('/shortest_path', methods=['POST'])
def shortest_path():
    # Graphe pas encore prêt → réponse claire
    if G is None:
        return jsonify({
            "error": "Le graphe est en cours de chargement, veuillez patienter quelques secondes et réessayer."
        }), 503

    data = request.get_json()
    start = tuple(data.get("start"))
    goal = tuple(data.get("goal"))

    if not start or not goal:
        return jsonify({
            "error": "Veuillez sélectionner un point de départ et un point d'arrivée"
        }), 400

    print(f"Départ : {start}, Arrivée : {goal}")

    try:
        orig_node = ox.distance.nearest_nodes(G, start[1], start[0])
        dest_node = ox.distance.nearest_nodes(G, goal[1], goal[0])
        print(f"Nœud départ : {orig_node}, Nœud arrivée : {dest_node}")

        shortest_path_nodes = A_star_algo(G, orig_node, dest_node)
        print(f"Chemin trouvé : {shortest_path_nodes}")

        if shortest_path_nodes is None:
            return jsonify({
                "error": "A* n'a pas pu trouver de chemin entre les points sélectionnés."
            }), 400

        path_coords = [
            (G.nodes[node]['y'], G.nodes[node]['x'])
            for node in shortest_path_nodes
        ]
        return jsonify({"path": path_coords})

    except Exception as e:
        print(f"Erreur lors du calcul du chemin : {e}")
        return jsonify({"error": "Problème lors du calcul du chemin."}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
