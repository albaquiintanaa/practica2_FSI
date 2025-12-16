import search
#import search_bad_heuristic as search

ab = search.GPSProblem('F', 'D'
                       , search.romania)

print("========================================")

print("BFS")
solution, gen, vis, weight, time = search.breadth_first_graph_search(ab)
print("Ruta:", solution.path())
print("Nodos generados: ", gen)
print("Nodos visitados:", vis)
print("Peso:", weight)
print(f"Tiempo de ejecución: {time*1_000_000:.1f} μs")



print("========================================")

print("DFS")
solution, gen, vis, weight, time = search.depth_first_graph_search(ab)
print("Ruta:", solution.path())
print("Nodos generados: ", gen)
print("Nodos visitados:", vis)
print("Peso:", weight)
print(f"Tiempo de ejecución: {time*1_000_000:.1f} μs")

print("========================================")

print("Ramificación y Acotación")
solution, gen, vis, weight , time = search.branch_and_bound_graph_search(ab)
print("Ruta:", solution.path())
print("Nodos generados: ", gen)
print("Nodos visitados:", vis)
print("Peso:", weight)
print(f"Tiempo de ejecución: {time*1_000_000:.1f} μs")

print("========================================")

print("Ramificación y Acotación con Subestimación")
solution, gen, vis, weight, time = search.branch_and_bound_with_underestimation_graph_search(ab)
print("Ruta:", solution.path())
print("Nodos generados: ", gen)
print("Nodos visitados:", vis)
print("Peso:", weight)
print(f"Tiempo de ejecución: {time*1_000_000:.1f} μs")

print("========================================")
