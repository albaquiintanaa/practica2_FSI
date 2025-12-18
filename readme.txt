🔹Este repositorio contiene la implementación de estrategias de búsqueda informada para resolver el problema de rutas en el mapa de Rumanía adjunto. 

🔹El proyecto compara el rendimiento de algoritmos no informados y sin tener en cuenta el peso, frente a algoritmos informados en términos de coste, tiempo y nodos explorados.

➮Algoritmos Implementados
El código base se ha ampliado para incluir:
-Amplitud (BFS) y Profundidad (DFS), incluidas en el fichero original.
-Ramificación y Acotación (Branch & Bound): Búsqueda óptima basada en el coste acumulado g(n).
-Ramificación y Acotación con Subestimación (A*): Búsqueda óptima y eficiente utilizando la distancia euclídea como heurística f(n) = g(n) + h(n).
-Experimentación con Sobreestimación: Prueba con una heurística no admisible para analizar la pérdida de optimalidad.

➮Estructura del Repositorio
🔸Código principal
-search.py: Código que contiene la estructura general de los problemas y los algoritmos de búsqueda.
-table.py: Script que automatiza la tabla comparativa de la memoria.
-run.py: Script principal para ejecutar una búsqueda individual. Permite probar una ruta concreta entre un origen y un destino y ver el resultado detallado.

🔸Carpeta overestimation
Contiene los experimentos con una heurística que no garantiza el camino óptimo:
-search_overestimated_heuristic.py: Implementa una heurística agresiva donde se multiplica la distancia euclídea por 4 Al sobreestimar el coste real, el algoritmo es más rápido pero pierde la admisibilidad, encontrando a veces rutas que no es la ruta óptima.
-table_overestimation.py: Script para generar la tabla de resultados específica de esta heurística y compararla.

🔸Carpeta graphics
Contiene la parte visual de la práctica:
-graph.py: Visualización del grafo de Rumanía con sus costes, nodos y aristas reales (usando networkx y matplotlib).
-graphH.py: Extensión de la visualización anterior que muestra, además, el valor de la heurística (distancia euclídea) de cada ciudad respecto a un destino seleccionado.

➮Métricas
El sistema contabiliza automáticamente:
Nodos Generados: Total de estados añadidos a la frontera.
Nodos Visitados: Total de estados analizados (objetivo comprobado).
Tiempo de Ejecución: En microsegundos.
Ruta: Lista de nodos desde el origen hasta el objetivo.
Peso: Coste acumulado de la ruta encontrada.
