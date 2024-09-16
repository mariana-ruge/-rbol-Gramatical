#Importar las librerias
import networkx as nx #Realiza los grafos
import matplotlib.pyplot as plt #Funciones para crear los gráficos
import sys

#Imprimir el árbol
def mostrar_arbol(G):
    #Tamaño de impresión del árbol
    plt.figure(figsize=(12, 8))
    #Calcular la disposición de los nodos
    pos = nx.spring_layout(G, k=0.9, iterations=50)
    #Dibujar los grafos usando la posición calculada
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=3000, font_size=10, font_weight='bold')
    
    # Añadir etiquetas a los nodos
    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    plt.title("Árbol Sintáctico")
    plt.axis('off')
    
    # Ajuste manual si tight_layout da advertencias
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    
    plt.show()


#Identificar y leer la gramática
def leer_gramatica(archivo_gramatica):
    #Abrir y leer el archivo de texto
    with open(archivo_gramatica, 'r') as archivo:
        Vt = set()  # Terminales
        Vxt = set()  # No terminales
        P = []  # Producciones
        S = None  # Símbolo inicial
        
        #Leer las líneas de los archivos de texto
        for linea in archivo:
            #Separar las líneas de los archivos de texto
            linea = linea.strip()
            #Identificar el conjunto de terminales
            #Los retira de la cadena para poder procesarlos
            if linea.startswith('Vt:'):
                Vt = set(linea.replace('Vt:', '').strip().split())
            #Busca líneas que comiencen con el prefijo vtx
            elif linea.startswith('Vxt:'):
                Vxt = set(linea.replace('Vxt:', '').strip().split())
            #Indican el simbolo inicial
            elif linea.startswith('S:'):
                S = linea.replace('S:', '').strip()
            #Indica el inicio de las producciones
            elif linea.startswith('P:'):
                # Se asume que las producciones empiezan justo después de 'P:'
                break
        
        #Leer los archivos, línea por línea
        for linea in archivo:
            #Descomponer las líneas de texto
            linea = linea.strip()
            if '->' in linea:
                #Crear el recorrido del arbol
                #Preorder
                izquierda, derecha = linea.split('->')
                izquierda = izquierda.strip()
                derecha = derecha.strip().split()
                P.append((izquierda, derecha))
        
        #Sino se encuentran los caracteres
        if not (Vt and Vxt and S and P):
            raise ValueError("La gramática no está completa o el formato es incorrecto.")
        
        return Vt, Vxt, S, P

#Función para validar la gramática 
def validar_gramatica(Vt, Vxt, S, P):
    #Buscar el simbolo inicial
    if S not in Vxt:
        raise ValueError("El símbolo inicial no está en el conjunto de no terminales.")
    
    #Buscar en la producción los simbolos
    for izq, der in P:
        if izq not in Vxt:
            raise ValueError(f"El lado izquierdo de la producción '{izq} -> {' '.join(der)}' no es un no terminal.")
        for simbolo in der:
            if simbolo not in Vt and simbolo not in Vxt:
                raise ValueError(f"El símbolo '{simbolo}' en la producción '{izq} -> {' '.join(der)}' no es válido.")


def validar_cadena(cadena, Vt, Vxt, S, P):
    """
    Valida si una cadena puede ser generada por la gramática.
    cadena: Cadena a validar.
    Vt: Conjunto de terminales.
    Vxt: Conjunto de no terminales.
    S: Símbolo inicial.
    P: Producciones.
    :return: True si la cadena es válida, False en caso contrario.
    """
    # La cadena debe ser una lista de caracteres
    cadena = list(cadena)
    
    # La pila de símbolos iniciales, comenzando con el símbolo inicial
    pila = [S]
    
    # Mientras queden símbolos por procesar y caracteres en la cadena
    while pila and cadena:
        simbolo = pila.pop(0)  # Extrae el primer símbolo de la pila
        
        if simbolo in Vt:
            if simbolo == cadena[0]:
                cadena.pop(0)  # El símbolo coincide, avanzamos en la cadena
            else:
                return False  # El símbolo no coincide, cadena no válida
        elif simbolo in Vxt:
            # Buscamos una producción que empiece con el símbolo actual
            produccion_encontrada = False
            for izq, der in P:
                if izq == simbolo:
                    # Añadimos los símbolos de la producción en orden inverso a la pila
                    pila = list(der) + pila
                    produccion_encontrada = True
                    break
            if not produccion_encontrada:
                return False  # No se encontró una producción para el símbolo
        else:
            return False  # Símbolo no terminal no reconocido
    
    # La cadena debe estar vacía y la pila también
    return not cadena and not pila

#Construir el árbol binario
def construir_arbol(cadena, S, P, Vt):
    #Organizar la cadena
    def derivacion(simbolo, cadena_restante, G=None):
        if G is None:
            G = nx.DiGraph()
        
        #Sino no encuentra el simbolo -> Retorna none
        if not simbolo:
            return G
        
        if not cadena_restante:
            if simbolo[0] in Vt:
                G.add_node(simbolo[0])
                return G
            return None

        #Añadir los grafos al nodo
        if simbolo[0] in Vt:
            #Si el simbolo corresponde con la cadena restante, añadir
            if simbolo[0] == cadena_restante[0]:
                G.add_node(simbolo[0])
                return G
            return None
        
        #Recorrido del árbol en preorder
        for izq, der in P:
            if izq == simbolo[0]:
                #Asignar a una nueva cadena 
                nueva_cadena = der + simbolo[1:]
                #Crear un subgrafo con la cadena del recorrido
                subgrafo = derivacion(nueva_cadena, cadena_restante, G)
                #Pintar el subgrafo con sus nodos
                if subgrafo:
                    G.add_edges_from(subgrafo.edges())
                    G.add_node(simbolo[0])
                    for s in der:
                        G.add_edge(simbolo[0], s)
                    return G
        
        return None

    arbol = derivacion([S], list(cadena))
    if arbol:
        # Agregar nodos terminales y etiquetas
        for i, c in enumerate(cadena):
            if c not in arbol.nodes():
                arbol.add_node(c)
            arbol.add_edge(S, c)  # Añade una conexión desde el símbolo inicial a cada terminal
    return arbol

#Main (recibe el archivo de gramática)
def main(archivo_gramatica):
    try:
        # Leer la gramática
        Vt, Vxt, S, P = leer_gramatica(archivo_gramatica)
        
        # Imprimir los componentes de la gramática
        print("\nComponentes de la Gramática:")
        print(f"Terminales (Vt): {Vt}")
        print(f"No terminales (Vxt): {Vxt}")
        print(f"Símbolo inicial (S): {S}")
        print("Producciones (P):")
        
        #Imprimir el recorrido que está haciendo
        for izquierda, derecha in P:
            print(f"  {izquierda} -> {' '.join(derecha)}")
        
        # Validar la gramática
        validar_gramatica(Vt, Vxt, S, P)
        
        # Pedir la cadena de entrada
        cadena = input("\nIngrese la cadena a validar: ")
        
        # Validar la cadena
        if validar_cadena(cadena, Vt, Vxt, S, P):
            print(f"La cadena '{cadena}' es válida según la gramática.")
            # Construir y mostrar el árbol sintáctico
            arbol = construir_arbol(cadena, S, P, Vt)
            #Simepre que existan nodos, y el árbol haya sido construido
            if arbol and len(arbol.nodes()) > 0:
                print("\nConstruyendo y mostrando el árbol sintáctico...")
                mostrar_arbol(arbol)
            else:
                print("No se pudo construir el árbol sintáctico.")
        else:
            print(f"La cadena '{cadena}' no es válida según la gramática.")
    
    #Manejar los erores
    except Exception as e:
        print(f"Error: {str(e)}")

#Entry point (main)
if __name__ == "__main__":
    #Validar los argumentos del archivo de texto
    if len(sys.argv) != 2:
        print("Uso: python programa.py archivo_gramatica.txt")
        sys.exit(1)
    main(sys.argv[1])

