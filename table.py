import search
#import search_bad_heuristic as search

destinos_romania = [['A', 'B'], ['O', 'E'], ['G', 'Z'], ['N', 'D'], ['M', 'F']]

for i, (origen, destino) in enumerate(destinos_romania, start=1):
    print("=========================================================")
    print(f"Ruta {i}: Origen = {origen}, Destino = {destino}")
    print("=========================================================")

    ab = search.GPSProblem(origen, destino, search.romania)


    # BFS
    print("BFS")
    solution, gen, vis, weight, tiempo = search.breadth_first_graph_search(ab)
    print("Ruta:", solution.path())
    print("Nodos generados: ", gen)
    print("Nodos visitados:", vis)
    print("Peso:", weight)
    print(f"Tiempo de ejecución: {tiempo*1_000_000:.1f} μs")
    print("---------------------------------------------------------")

    # DFS
    print("DFS")
    solution, gen, vis, weight, tiempo = search.depth_first_graph_search(ab)
    print("Ruta:", solution.path())
    print("Nodos generados: ", gen)
    print("Nodos visitados:", vis)
    print("Peso:", weight)
    print(f"Tiempo de ejecución: {tiempo*1_000_000:.1f} μs")
    print("---------------------------------------------------------")

    # Ramificación y Acotación
    print("Ramificación y Acotación")
    solution, gen, vis, weight, tiempo = search.branch_and_bound_graph_search(ab)
    print("Ruta:", solution.path())
    print("Nodos generados: ", gen)
    print("Nodos visitados:", vis)
    print("Peso:", weight)
    print(f"Tiempo de ejecución: {tiempo*1_000_000:.1f} μs")
    print("---------------------------------------------------------")

    # Ramificación y Acotación con Subestimación
    print("Ramificación y Acotación con Subestimación")
    solution, gen, vis, weight, tiempo = search.branch_and_bound_with_underestimation_graph_search(ab)
    print("Ruta:", solution.path())
    print("Nodos generados: ", gen)
    print("Nodos visitados:", vis)
    print("Peso:", weight)
    print(f"Tiempo de ejecución: {tiempo*1_000_000:.1f} μs")
    print("---------------------------------------------------------")

    print("")

