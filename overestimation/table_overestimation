import search_bad_heuristic as search


destinos_romania = [['A', 'B'], ['O', 'E'], ['G', 'Z'], ['N', 'D'], ['M', 'F']]

for i, (origen, destino) in enumerate(destinos_romania, start=1):
    print("=========================================================")
    print(f"Ruta {i}: Origen = {origen}, Destino = {destino}")
    print("=========================================================")

    ab = search.GPSProblem(origen, destino, search.romania)


    # Ramificación y Acotación con Sobreestimación
    print("Ramificación y Acotación con Sobreestimación")
    solution, gen, vis, weight, tiempo = search.branch_and_bound_with_overestimation_graph_search(ab)
    print("Ruta:", solution.path())
    print("Nodos generados: ", gen)
    print("Nodos visitados:", vis)
    print("Peso:", weight)
    print(f"Tiempo de ejecución: {tiempo*1_000_000:.1f} μs")
    print("---------------------------------------------------------")

    print("")
