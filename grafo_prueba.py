# Importar las librerías necesarias
import networkx as nx
import matplotlib.pyplot as plt #Se importa matplotlib

# Crear la instancia de un grafo no dirigido
G = nx.Graph()

# Imprimir información inicial del grafo vacío
print(f"Grafo  con {G.number_of_nodes()} nodos y {G.number_of_edges()} aristas")

# Añadir nodos y aristas al grafo
G.add_edges_from([("A", "C"), ("B", "C")])

# Imprimir la información actualizada del grafo
print(f"Grafo con {G.number_of_nodes()} nodos y {G.number_of_edges()} aristas")

# Verificar si es un grafo dirigido
print(f"Este grafo es dirigido o no {G.is_directed()}") #Devuelve true o false

# Configurar la visualización del grafo
fig, ax = plt.subplots(figsize=(5, 5))

# Dibujar el grafo con etiquetas
nx.draw(G, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_color='black', ax=ax)

# Ajustar los límites de los ejes para mejorar la visualización
ax.set_xlim([1.2*x for x in ax.get_xlim()])
ax.set_ylim([1.2*y for y in ax.get_ylim()])

# Mostrar el grafo
plt.show()
