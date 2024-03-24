import folium


def visualize_ant_colony(G, best_tour):
    m = folium.Map(location=[20.0, -10.0], zoom_start=6)
    
    # Dessiner les arêtes du graphe
    for u, v, data in G.edges(data=True):
        folium.PolyLine(
            locations=[(G.nodes[u]['pos'][0], G.nodes[u]['pos'][1]), (G.nodes[v]['pos'][0], G.nodes[v]['pos'][1])],
            color='blue', weight=1, opacity=0.5, dash_array='5, 5').add_to(m)

    # Dessiner les villes
    for node in G.nodes():
        folium.Marker(location=(G.nodes[node]['pos'][0], G.nodes[node]['pos'][1]), popup=node,
                      icon=folium.Icon(color='green', icon='circle', prefix='fa')).add_to(m)

    # Dessiner le meilleur tour en rouge
    for i in range(len(best_tour) - 1):
        u = best_tour[i]
        v = best_tour[i + 1]
        folium.PolyLine(
            locations=[(G.nodes[u]['pos'][0], G.nodes[u]['pos'][1]), (G.nodes[v]['pos'][0], G.nodes[v]['pos'][1])],
            color='red', weight=2).add_to(m)

    # Ajuster le zoom et la position de la carte
    m.fit_bounds(m.get_bounds())

    return m


def visualize_approximation(G, path):
    m = folium.Map(location=[20.0, -10.0], zoom_start=6)
    
    # Dessiner les arêtes du graphe
    for u, v, data in G.edges(data=True):
        folium.PolyLine(
            locations=[(G.nodes[u]['pos'][0], G.nodes[u]['pos'][1]), (G.nodes[v]['pos'][0], G.nodes[v]['pos'][1])],
            color='blue', weight=1, opacity=0.5, dash_array='5, 5').add_to(m)

    # Dessiner les villes
    for node in G.nodes():
        folium.Marker(location=(G.nodes[node]['pos'][0], G.nodes[node]['pos'][1]), popup=node,
                      icon=folium.Icon(color='green', icon='circle', prefix='fa')).add_to(m)

    # Dessiner le chemin approximatif en rouge
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        folium.PolyLine(
            locations=[(G.nodes[u]['pos'][0], G.nodes[u]['pos'][1]), (G.nodes[v]['pos'][0], G.nodes[v]['pos'][1])],
            color='red', weight=2).add_to(m)

    # Ajuster le zoom et la position de la carte
    m.fit_bounds(m.get_bounds())

    return m



#fuction pour la visualisation du maps 
def visualize_graph(G):
    m = folium.Map(location=[20.0, -10.0], zoom_start=6)
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

    