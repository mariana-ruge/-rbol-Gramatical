# Importar las librerías necesarias
# networkx -> Para construir y manipular grafos
import networkx as nx
# Matplotlib -> Para generar gráficos
import matplotlib.pyplot as plt
# sys -> Para manejar argumentos de la línea de comandos
import sys
# Para ajustar el grafo a una estructura de árbol usando Graphviz
from networkx.drawing.nx_agraph import graphviz_layout

# Función para mostrar un árbol usando Matplotlib
def mostrar_arbol(G):
    plt.figure(figsize=(12, 8))  # Configura el tamaño de la figura
    pos = graphviz_layout(G, prog='dot')  # Genera una disposición para el grafo usando Graphviz
    # Dibuja el grafo con etiquetas, colores, tamaños y fuentes específicas
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=3000, font_size=10, font_weight='bold', edge_color='gray')
    # Crea un diccionario de etiquetas para los nodos
    labels = {node: node for node in G.nodes()}
    # Dibuja las etiquetas de los nodos con una fuente más pequeña
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    plt.title("Árbol Sintáctico")  # Título del gráfico
    plt.axis('off')  # Oculta los ejes
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # Ajusta el espacio de los bordes
    plt.show()  # Muestra el gráfico

# Función para leer una gramática desde un archivo
def leer_gramatica(archivo_gramatica):
    with open(archivo_gramatica, 'r') as archivo:  # Abre el archivo en modo lectura
        Vt = set()  # Conjunto de terminales
        Vxt = set()  # Conjunto de no terminales
        P = []  # Lista de producciones
        S = None  # Símbolo inicial
        
        # Lee el archivo línea por línea
        for linea in archivo:
            linea = linea.strip()  # Elimina espacios en blanco al inicio y final de la línea
            # Procesa la línea dependiendo del prefijo
            if linea.startswith('Vt:'):
                Vt = set(linea.replace('Vt:', '').strip().split())  # Extrae terminales
            elif linea.startswith('Vxt:'):
                Vxt = set(linea.replace('Vxt:', '').strip().split())  # Extrae no terminales
            elif linea.startswith('S:'):
                S = linea.replace('S:', '').strip()  # Extrae el símbolo inicial
            elif linea.startswith('P:'):
                break  # Termina la lectura de la gramática cuando encuentra 'P:'
        
        # Lee las producciones desde el archivo
        for linea in archivo:
            linea = linea.strip()  # Elimina espacios en blanco
            if '->' in linea:  # Verifica si la línea contiene una producción
                izquierda, derecha = linea.split('->')  # Divide la producción en izquierda y derecha
                izquierda = izquierda.strip()  # Elimina espacios en blanco
                derecha = derecha.strip().split()  # Divide la parte derecha en símbolos
                P.append((izquierda, derecha))  # Agrega la producción a la lista
        
        # Verifica que la gramática esté completa
        if not (Vt and Vxt and S and P):
            raise ValueError("La gramática no está completa o el formato es incorrecto.")
        
        return Vt, Vxt, S, P  # Retorna los componentes de la gramática

# Función para validar los componentes de la gramática
def validar_gramatica(Vt, Vxt, S, P):
    # Verifica que el símbolo inicial esté en el conjunto de no terminales
    if S not in Vxt:
        raise ValueError("El símbolo inicial no está en el conjunto de no terminales.")
    
    # Verifica que todas las producciones sean válidas
    for izq, der in P:
        if izq not in Vxt:
            raise ValueError(f"El lado izquierdo de la producción '{izq} -> {' '.join(der)}' no es un no terminal.")
        for simbolo in der:
            if simbolo not in Vt and simbolo not in Vxt:
                raise ValueError(f"El símbolo '{simbolo}' en la producción '{izq} -> {' '.join(der)}' no es válido.")

# Función para validar si una cadena puede ser generada por la gramática
def validar_cadena(cadena, Vt, Vxt, S, P):
    def derivar(actual, resto):
        if not actual and not resto:
            return True  # La cadena está completamente derivada y vacía
        if not actual or not resto:
            return False  # La cadena está vacía pero el resto no, o viceversa
        
        if actual[0] in Vt:
            if actual[0] == resto[0]:
                return derivar(actual[1:], resto[1:])  # Continúa con la siguiente parte de la cadena
            return False  # El símbolo terminal no coincide
        
        for izq, der in P:
            if izq == actual[0]:
                if derivar(der + actual[1:], resto):
                    return True  # Si la derivación es exitosa, retorna True
        return False  # No se pudo derivar la cadena
        
    return derivar([S], list(cadena))  # Inicia la derivación con el símbolo inicial

# Función para construir el árbol sintáctico a partir de una cadena
def construir_arbol(cadena, S, P, Vt):
    def derivacion(simbolo, cadena_restante, G=None, padre=None):
        if G is None:
            G = nx.DiGraph()  # Crea un grafo dirigido si no se ha proporcionado uno
            G.add_node(simbolo)  # Agrega el símbolo inicial como nodo
        
        if not cadena_restante and simbolo in Vt:
            return G, ''  # La derivación es completa si la cadena restante está vacía
        
        if simbolo in Vt:
            if cadena_restante and simbolo == cadena_restante[0]:
                if padre:
                    G.add_edge(padre, simbolo)  # Agrega un borde entre el nodo padre y el nodo actual
                return G, cadena_restante[1:]  # Continúa con la cadena restante
            return None, cadena_restante  # No se puede derivar el símbolo terminal
        
        for izq, der in P:
            if izq == simbolo:
                subgrafo = G.copy()  # Copia el grafo actual para la derivación
                resto_temp = cadena_restante
                todos_derivan = True
                for s in der:
                    resultado, resto_temp = derivacion(s, resto_temp, subgrafo, simbolo)
                    if resultado is None:
                        todos_derivan = False
                        break
                    subgrafo = resultado  # Actualiza el subgrafo con el resultado de la derivación
                if todos_derivan:
                    if padre:
                        subgrafo.add_edge(padre, simbolo)  # Agrega un borde entre el nodo padre y el símbolo derivado
                    return subgrafo, resto_temp  # Retorna el subgrafo y la cadena restante
        
        return None, cadena_restante  # No se pudo derivar la cadena

    arbol, _ = derivacion(S, cadena)  # Inicia la derivación con el símbolo inicial
    return arbol  # Retorna el árbol sintáctico construido

# Función principal para ejecutar el programa
def main(archivo_gramatica):
    try:
        # Lee y valida la gramática desde el archivo
        Vt, Vxt, S, P = leer_gramatica(archivo_gramatica)
        
        print("\nComponentes de la Gramática:")
        print(f"Terminales (Vt): {Vt}")
        print(f"No terminales (Vxt): {Vxt}")
        print(f"Símbolo inicial (S): {S}")
        print("Producciones (P):")
        for izquierda, derecha in P:
            print(f"  {izquierda} -> {' '.join(derecha)}")
        
        validar_gramatica(Vt, Vxt, S, P)  # Valida los componentes de la gramática
        
        while True:
            cadena = input("\nIngrese la cadena a validar (o 'salir' para terminar): ")
            if cadena.lower() == 'salir':
                break  # Sale del bucle si el usuario ingresa 'salir'
            
            if validar_cadena(cadena, Vt, Vxt, S, P):
                print(f"La cadena '{cadena}' es válida según la gramática.")
                arbol = construir_arbol(cadena, S, P, Vt)
                if arbol and len(arbol.nodes()) > 0:
                    print("\nConstruyendo y mostrando el árbol sintáctico...")
                    mostrar_arbol(arbol)  # Muestra el árbol sintáctico
                else:
                    print("No se pudo construir el árbol sintáctico.")
            else:
                print(f"La cadena '{cadena}' no es válida según la gramática.")
    
    except Exception as e:
        print(f"Error: {str(e)}")  # Muestra el mensaje de error si ocurre una excepción

# Punto de entrada del programa
if __name__ == "__main__":
    # Verifica que se haya proporcionado el nombre del archivo como argumento
    if len(sys.argv) != 2:
        print("Uso: python analizador_gramatica.py archivo_gramatica.txt")
        sys.exit(1)
    main(sys.argv[1])  # Llama a la función principal con el archivo de gramática
