
import networkx as nx
import geopy.distance
import pandas as pd
 
 
 
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
