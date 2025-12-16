import matplotlib.pyplot as plt
import networkx as nx
from search import romania, GPSProblem
#import search_bad_heuristic as search

def dibujar_grafo_con_heuristica(graph, start, goal):
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

    problema = GPSProblem(start, goal, graph)

    plt.figure(figsize=(10, 8))
    plt.title(f"Mapa de Romania con Heurísticas (Origen: {start} - Destino: {goal})")


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

    # ============ HEURÍSTICA EN NODO ==============
    h_labels = {}
    pos_h = {}

    for ciudad, (x, y) in pos.items():
        h_value = problema.h(ciudad)

        h_labels[ciudad] = f"h={h_value}"

        # Desplazar
        pos_h[ciudad] = (x -30, y - 5) 

    nx.draw_networkx_labels(
        G,
        pos_h,
        labels=h_labels,
        font_size=9,
        font_color="red",
        font_family="monospace"
    )
    # ==============================================

    plt.show()


if __name__ == "__main__":
    dibujar_grafo_con_heuristica(romania, "S", "B")

