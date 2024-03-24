import base64
import io
from flask import Flask, Response, jsonify, render_template, request
import networkx as nx
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from ant_colony import *
from graphe import upload
from maps import *
 
app = Flask(__name__)







@app.route('/')
def main():
    return render_template('index.html')

@app.route('/upload')
def uploadfile():
    return render_template('upload.html')


@app.route('/uploadfile', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Aucun fichier trouvé !"
    
    file = request.files['file']

    if file.filename == '':
        return "Nom de fichier vide !"

    if file:
        filename = file.filename
        file.save(filename)
        return "Fichier téléchargé avec succès !"


@app.route('/ant_colony')
def run_ant_colony_optimization():
    G=upload()
    num_ants = 10
    alpha = 1
    beta = 2
    evaporation_rate = 0.5
    num_iterations = 100
    Q = 100

    best_tour, best_tour_length = ant_colony_optimization(G, num_ants, alpha, beta, evaporation_rate, num_iterations, Q)

    results = {
        "best_tour": best_tour,
        "best_tour_length": best_tour_length
    }
    plt.figure(figsize=(10, 6))
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=200, node_color='skyblue')
    plt.title('Graphe des villes en Mauritanie')

    best_tour_edges = [(best_tour[i], best_tour[i + 1]) for i in range(len(best_tour) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=best_tour_edges, edge_color='red', width=2)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    plot_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    plt.close()
    
    m = visualize_ant_colony(G,best_tour)
    m.save('templates/maps/ACO.html')
    # Chemin absolu complet vers le fichier HTML de la carte
    # map_path = os.path.abspath('maps/ant_colony.html')
    # webbrowser.open('file://' + map_path)

    return render_template('ant_colony.html',results=results, plot=plot_base64)

    

@app.get('/Alg_approx')
def Alg_approx():
    G = upload()
    mst = nx.minimum_spanning_tree(G)

    ville_depart = 'Nouakchott'
    ville_arrivee = 'Nouakchott'

    visited = set()
    path = [ville_depart]

    def dfs(city):
        visited.add(city)
        for neighbor in mst.neighbors(city):
            if neighbor not in visited:
                path.append(neighbor)
                dfs(neighbor)

    dfs(ville_depart)

    path.append(ville_arrivee)

    results = [{"from": path[i], "to": path[i + 1]} for i in range(len(path) - 1)]

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G) 
    nx.draw(G, pos, with_labels=True, node_size=200, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, edgelist=[(path[i], path[i + 1]) for i in range(len(path) - 1)], edge_color='red', width=2)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    m = visualize_approximation(G,path)
    m.save('templates/maps/approximation.html')
    # map_path = os.path.abspath('maps/approximation.html')
    # webbrowser.open('file://' + map_path)

    return render_template('graphe_Approx.html', results=results, plot=plot_base64)



@app.get('/maps')
def maps():
    G=upload()

    m = visualize_graph(G)

    m.save('templates/maps/map1.html')
    
    
    return render_template('map.html')
    





