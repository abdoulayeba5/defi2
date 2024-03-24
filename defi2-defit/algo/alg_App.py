import pandas as pd
import networkx as nx
import geopy.distance

# Charger les données à partir du fichier Excel en utilisant Pandas
capitales_df = pd.read_excel('Cordonnees_GPS.xlsx', sheet_name='Capitales_Wilaya')
mougataas_df = pd.read_excel('Cordonnees_GPS.xlsx', sheet_name='Mougataa')

# Créer un graphe non orienté
G = nx.Graph()

# Ajouter les nœuds et les arêtes avec leurs poids basés sur les distances géodésiques
for _, row in capitales_df.iterrows():
    ville, latitude, longitude = row
    G.add_node(ville, pos=(latitude, longitude))

for _, row in mougataas_df.iterrows():
    ville, wilaya, latitude, longitude = row
    G.add_node(ville, pos=(latitude, longitude))

# Calculer les distances entre les nœuds et ajouter les arêtes au graphe
for u in G.nodes():
    for v in G.nodes():
        if u != v and not G.has_edge(u, v):
            coords_u = G.nodes[u]['pos']
            coords_v = G.nodes[v]['pos']
            distance = geopy.distance.geodesic(coords_u, coords_v).km      
            G.add_edge(u, v, weight=distance)

# Calculer l'arbre couvrant minimal
mst = nx.minimum_spanning_tree(G)

# Définir la ville de départ et d'arrivée à Nouakchott
ville_depart = 'Nouakchott'
ville_arrivee = 'Nouakchott'

# Effectuer le parcours DFS sur l'arbre couvrant minimal à partir de Nouakchott
dfs_edges = list(nx.dfs_edges(mst, source=ville_depart))

# Ajouter la dernière arête pour revenir à Nouakchott
dfs_edges.append((dfs_edges[-1][1], ville_arrivee))

# Afficher les arêtes dans l'ordre du parcours DFS
print("Arêtes dans l'ordre du parcours DFS, démarrant et terminant à Nouakchott :")
for edge in dfs_edges:
    print(edge)
