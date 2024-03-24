import numpy as np
import random
import networkx as nx
import pandas as pd
import matplotlib
matplotlib.use('Agg')  
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
