import numpy as np
import random
import networkx as nx
import geopy.distance
import pandas as pd
import matplotlib.pyplot as plt


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


# Charger les données à partir du fichier Excel
data = pd.read_excel('Cordonnees_GPS.xlsx', sheet_name='Capitales_Wilaya')
data2 = pd.read_excel('Cordonnees_GPS.xlsx', sheet_name='Mougataa')

# Créer un graphe non orienté pondéré
G = nx.Graph()

# Ajouter les nœuds avec les coordonnées GPS
for index, row in data.iterrows():
    G.add_node(row['Ville'], pos=(row['Latitude'], row['Longitude']))

# Ajouter les nœuds avec les coordonnées GPS
# for index, row in data2.iterrows():
#     G.add_node(row['nom'], pos=(row['Latitude'], row['Longitude']))
    

# Calculer et ajouter les poids des arêtes (distances)
for u in G.nodes():
    for v in G.nodes():
        if u != v:
            coords_u = G.nodes[u]['pos']
            coords_v = G.nodes[v]['pos']
            distance = geopy.distance.geodesic(coords_u, coords_v).km
            G.add_edge(u, v, weight=distance)

# Définir les paramètres de l'algorithme
num_ants = 10
alpha = 1
beta = 2
evaporation_rate = 0.5
num_iterations = 100
Q = 100

# Appliquer l'algorithme de colonie de fourmis
best_tour, best_tour_length = ant_colony_optimization(G, num_ants, alpha, beta, evaporation_rate, num_iterations, Q)

# Afficher le résultat
print("Meilleure tournée trouvée:", best_tour)
print("Longueur de la meilleure tournée:", best_tour_length)

# Affichage graphique du graphe et de la solution trouvée
plt.figure(figsize=(10, 6))

# Affichage du graphe
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos, with_labels=True, node_size=200, node_color='skyblue')
plt.title('Graphe des villes en Mauritanie')

# Affichage de la solution trouvée
best_tour_edges = [(best_tour[i], best_tour[i + 1]) for i in range(len(best_tour) - 1)]
nx.draw_networkx_edges(G, pos, edgelist=best_tour_edges, edge_color='red', width=2)
plt.show()
