import matplotlib.pyplot as plt
import networkx as nx
from search import romania

def dibujar_grafo(graph):
    G = nx.Graph()

    for ciudad in graph.nodes():
        G.add_node(ciudad)

    for a in graph.nodes():
        for b, dist in graph.get(a).items():
            G.add_edge(a, b, weight=dist)

    # Coordenadas reales del archivo
    if hasattr(graph, "locations"):
        pos = dict(graph.locations)
    else:
        pos = nx.spring_layout(G)

    plt.figure(figsize=(10, 8))
    plt.title("Mapa de Rumanía")


    # Nodos y aristas
    nx.draw(
        G, pos,
        with_labels=True,
        node_size=900,
        font_size=9,
        font_weight="bold"
    )

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=labels,
        font_size=7
    )

    plt.show()


if __name__ == "__main__":
    dibujar_grafo(romania)
