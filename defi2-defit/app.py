import webbrowser
from flask import Flask, jsonify, render_template, request
import folium
import numpy as np
import random
import networkx as nx
import geopy.distance
import pandas as pd
import matplotlib.pyplot as plt
 
app = Flask(__name__)


# Fonction pour calculer la visibilité entre deux villes (distance inverse)
def visibility(G, u, v):
    return 1 / G[u][v]['weight']

# Fonction pour initialiser les niveaux de phéromone sur toutes les arêtes
def initialize_pheromone(G, initial_pheromone=0.1):
    for u, v in G.edges():
        G[u][v]['pheromone'] = initial_pheromone

# Fonction pour choisir la prochaine ville à visiter pour une fourmi donnée
def choose_next_vertex(G, visited, current_vertex, alpha, beta):
    unvisited = [v for v in G.nodes() if v not in visited]
    probabilities = []
    total = 0
    for v in unvisited:
        if G.has_edge(current_vertex, v):
            pheromone = G[current_vertex][v]['pheromone']
            visibility_val = visibility(G, current_vertex, v)
            probabilities.append((v, pheromone ** alpha * visibility_val ** beta))
            total += pheromone ** alpha * visibility_val ** beta
    probabilities = [(v, p / total) for v, p in probabilities]
    next_vertex = random.choices([v for v, _ in probabilities], [p for _, p in probabilities])[0]
    return next_vertex

# Fonction pour déposer la quantité de phéromone sur chaque arête visitée
def deposit_pheromone(G, tour, Q):
    for i in range(len(tour) - 1):
        u = tour[i]
        v = tour[i + 1]
        G[u][v]['pheromone'] += Q / len(tour)

# Algorithme de colonie de fourmis
def ant_colony_optimization(G, num_ants, alpha, beta, evaporation_rate, num_iterations, Q):
    best_tour = None
    best_tour_length = np.inf
    initialize_pheromone(G)

    for _ in range(num_iterations):
        for ant in range(num_ants):
            current_vertex = "Nouakchott"  # Définir la ville de départ comme "Nouakchott"
            tour = [current_vertex]
            visited = set([current_vertex])
            while len(visited) < len(G.nodes()):
                next_vertex = choose_next_vertex(G, visited, current_vertex, alpha, beta)
                tour.append(next_vertex)
                visited.add(next_vertex)
                current_vertex = next_vertex
            
            # Assurez-vous que le parcours se termine à "Nouakchott"
            tour.append("Nouakchott")
            
            # Calculer la longueur totale du parcours
            tour_length = nx.path_weight(G, tour, weight='weight')
            if tour_length < best_tour_length:
                best_tour = tour
                best_tour_length = tour_length
            deposit_pheromone(G, tour, Q)
        for u, v in G.edges():
            G[u][v]['pheromone'] *= (1 - evaporation_rate)

    return best_tour, best_tour_length

@app.route('/')
def run_ant_colony_optimization():
    G=upload()
    num_ants = 10
    alpha = 1
    beta = 2
    evaporation_rate = 0.5
    num_iterations = 100
    Q = 100

    # Appliquer l'algorithme de colonie de fourmis
    best_tour, best_tour_length = ant_colony_optimization(G, num_ants, alpha, beta, evaporation_rate, num_iterations, Q)

    results = {
        "best_tour": best_tour,
        "best_tour_length": best_tour_length
    }

    return jsonify(results)

@app.route('/upload')
def upload():
    capitales_df = pd.read_excel('Cordonnees_GPS.xlsx', sheet_name='Capitales_Wilaya')
    # mougataas_df = pd.read_excel('Cordonnees_GPS.xlsx', sheet_name='Mougataa')

    G = nx.Graph()
    
    for _, row in capitales_df.iterrows():
        ville, latitude, longitude = row
        G.add_node(ville, pos=(latitude, longitude))

    # for _, row in mougataas_df.iterrows():
    #     ville, wilaya, latitude, longitude = row
    #     G.add_node(ville, pos=(latitude, longitude))

    for u in G.nodes():
        for v in G.nodes():
            if u != v and not G.has_edge(u, v):
                coords_u = G.nodes[u]['pos']
                coords_v = G.nodes[v]['pos']
                distance = geopy.distance.geodesic(coords_u, coords_v).km      
                G.add_edge(u, v, weight=distance)
    return G

@app.get('/Alg_approx')
def Alg_approx():
    
    # recuperer le graph 
    G=upload()
    # Calculer l'arbre couvrant minimal
    mst = nx.minimum_spanning_tree(G)

    ville_depart = 'Nouakchott'
    ville_arrivee = 'Nouakchott'

    # Effectuer le parcours DFS sur l'arbre couvrant minimal à partir de Nouakchott
    dfs_edges = list(nx.dfs_edges(mst, source=ville_depart))

    # Ajouter la dernière arête pour revenir à Nouakchott
    dfs_edges.append((dfs_edges[-1][1], ville_arrivee))

    # Formatter les résultats dans un format JSON
    results = [{"from": edge[0], "to": edge[1]} for edge in dfs_edges]

    # Retourner les résultats
    return jsonify(results)



@app.get('/map')
def visualize_graph(G, m):
    for u, v, data in G.edges(data=True):
        # Ajouter la ligne entre les villes avec une flèche
        folium.PolyLine(
            locations=[(G.nodes[u]['pos'][0], G.nodes[u]['pos'][1]), (G.nodes[v]['pos'][0], G.nodes[v]['pos'][1])],
            color='blue', weight=1, opacity=0.5, dash_array='5, 5').add_to(m)

        # Ajouter les marqueurs pour chaque ville
        folium.Marker(location=(G.nodes[u]['pos'][0], G.nodes[u]['pos'][1]), popup=u,
                      icon=folium.Icon(color='green', icon='circle', prefix='fa')).add_to(m)
        folium.Marker(location=(G.nodes[v]['pos'][0], G.nodes[v]['pos'][1]), popup=v,
                      icon=folium.Icon(color='green', icon='circle', prefix='fa')).add_to(m)

        # Calculer la position du label de distance
        label_lat = (G.nodes[u]['pos'][0] + G.nodes[v]['pos'][0]) / 2
        label_lon = (G.nodes[u]['pos'][1] + G.nodes[v]['pos'][1]) / 2

        # Ajouter le label de distance
        folium.Marker(location=(label_lat, label_lon), icon=folium.DivIcon(
            html=f'<div style="font-size: 8pt;">{round(data["weight"], 2)} km</div>')).add_to(m)

    # Ajuster le zoom et la position de la carte
    m.fit_bounds(m.get_bounds())

    return m

    

    
@app.get('/maps')
def maps():
    G=upload()
        # Utilisation de la fonction
    m = folium.Map(location=[20.0, -10.0], zoom_start=6)
    m = visualize_graph(G, m)

    # Enregistrer la carte dans un fichier HTML
    m.save('mauritania_map_with_graph8.html')

    # Ouvrir le fichier HTML dans le navigateur par défaut
    webbrowser.open('mauritania_map_with_graph8.html')


    # return render_template('map.html')
