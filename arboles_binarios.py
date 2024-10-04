#Importar librerias
import networkx as nx #Para crear el grafo
import matplotlib.pyplot as plt #Para hacer representaciones visuales
from networkx.drawing.nx_agraph import graphviz_layout #Para organizarlo en estructura de árbol

# Función para leer una gramática desde un archivo y validarla
def leer_gramatica(archivo):
    """
    Lee una gramática desde un archivo .txt y la devuelve junto con sus terminales, no terminales y símbolo inicial.
    """
    #Crear el diccionario de la gramática y los conjuntos de terminales y no terminales.
    #Inicializar el simbolo
    gramatica = {} 
    terminales = set()
    no_terminales = set()
    simbolo_inicial = None
    
    # Abre el archivo y procesa cada línea
    with open(archivo, 'r') as f:
        for linea in f:
            if '->' in linea:  # Verifica si la línea contiene una producción
                lado_izq, lado_der = linea.strip().split('->')  # Separar el lado izquierdo y derecho de la producción
                lado_izq = lado_izq.strip()
                producciones = [prod.strip() for prod in lado_der.split('|')]  # Separar las producciones alternativas
                
                if not simbolo_inicial:  # El primer no terminal se considera el símbolo inicial
                    simbolo_inicial = lado_izq
                #Añadir a los no terminales
                no_terminales.add(lado_izq)
                
                #Recorrer las producciones
                for prod in producciones:
                    #Buscar los simbolos en las producciones
                    for simbolo in prod:
                        #Verificar si es mayúscula o minúscula
                        if simbolo.islower():
                            terminales.add(simbolo)  # Si es minúscula, es un terminal
                        elif simbolo.isupper():
                            no_terminales.add(simbolo)  # Si es mayúscula, es un no terminal
                
                gramatica[lado_izq] = producciones  # Almacena la producción en la gramática
    
    return gramatica, simbolo_inicial, terminales, no_terminales

# Función para imprimir la gramática
def imprimir_gramatica(gramatica, simbolo_inicial, terminales, no_terminales):
    """
    Imprime los componentes de la gramática: símbolo inicial, terminales, no terminales y producciones.
    """
    print("Gramática:")
    print(f"Símbolo inicial: {simbolo_inicial}")
    print(f"Terminales: {', '.join(sorted(terminales))}")
    print(f"No terminales: {', '.join(sorted(no_terminales))}")
    print("Producciones:")
    for no_terminal, producciones in gramatica.items():
        print(f"{no_terminal} -> {' | '.join(producciones)}")

# Función para verificar si una cadena es aceptada por la gramática
def es_valida_cadena(gramatica, cadena, simbolo='S'):
    """
    Verifica si una cadena es válida según las reglas de la gramática. 
    Por defecto, comienza con el símbolo 'S'.
    """
    # Caso base: cadena vacía con una producción de ε
    if cadena == "" and 'ε' in gramatica.get(simbolo, []):
        return True
    if cadena == "":
        return False

    # Recorre todas las producciones del símbolo actual
    for produccion in gramatica.get(simbolo, []):
        if es_valida_produccion(gramatica, cadena, produccion):
            return True

    return False

# Función auxiliar para validar una producción específica
def es_valida_produccion(gramatica, cadena, produccion):
    """
    Verifica si una producción específica puede generar la cadena proporcionada.
    """
    i = 0  # Índice para recorrer la cadena
    produccion = produccion.split()  # Divide la producción en símbolos
    
    # Recorre los símbolos en la producción
    for simbolo in produccion:
        if simbolo in gramatica:  # Si es un no terminal
            # Intenta consumir la cadena parcialmente
            for j in range(i, len(cadena) + 1):
                if es_valida_cadena(gramatica, cadena[i:j], simbolo):
                    i = j  # Avanza el índice en la cadena
                    break
            else:
                return False  # Si no se puede consumir la cadena, es inválido
        else:  # Es un terminal
            if i < len(cadena) and cadena[i] == simbolo:
                i += 1  # Avanza si coincide el terminal
            else:
                return False
    
    return i == len(cadena)  # Devuelve True si toda la cadena ha sido consumida

# Función recursiva para construir el árbol de derivación
def construir_arbol_recursivo(gramatica, cadena, simbolo, G, parent):
    """
    Construye recursivamente un árbol de derivación para una cadena dada y lo almacena en el grafo G.
    """
    #Añade los nodos y las aristas
    if simbolo not in gramatica:  # Es un terminal
        G.add_node(cadena)
        G.add_edge(parent, cadena)
        return cadena

    #Producciones para los espacios y cadenas vacías
    for produccion in gramatica[simbolo]:
        if produccion == 'ε' and cadena == "":
            G.add_node("ε")
            G.add_edge(parent, "ε")
            return "ε"

        i = 0
        #Crear una lista para los hijos del árbol
        hijos = []
        produccion = produccion.split()
        
        #Buscar los caracteres de la gramática en la producción
        for char in produccion:
            if char in gramatica:
                subcadena = cadena[i:i+1]  # Procesa un carácter a la vez
                #Añadir a los hijos de árbol los caracteres válidos
                if es_valida_cadena(gramatica, subcadena, char):
                    hijos.append((char, subcadena))
                    i += len(subcadena)
            elif i < len(cadena) and cadena[i] == char:
                hijos.append((char, char))
                i += 1

        #Recorrer la cadena, en el tamaño de la mismo
        #Se construye un árbol recursivo
        if i == len(cadena):
            #recorrer cada hijo de la gramática en la subcadena a validar
            for hijo, subcadena in hijos:
                #Añadir los nodos y las aristas de los árboles
                G.add_node(hijo)
                G.add_edge(parent, hijo)
                #Construir el árbol
                construir_arbol_recursivo(gramatica, subcadena, hijo, G, hijo)
            return

# Función para construir el árbol de derivación
def construir_arbol(gramatica, cadena):
    """
    Construye y dibuja el árbol de derivación para una cadena dada usando la gramática proporcionada.
    """
    G = nx.DiGraph()  # Grafo dirigido para el árbol

    # Nodo raíz
    G.add_node("S")

    if cadena == "ε":  # Caso especial para cadena vacía
        G.add_edge("S", "ε")
    else:
        construir_arbol_recursivo(gramatica, cadena, "S", G, "S")  # Construcción recursiva

    # Dibujar el árbol
    pos = graphviz_layout(G, prog='dot')
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=16, font_weight="bold")
    plt.show()

# Función principal del programa
def main():
    """
    Función principal que coordina la lectura de la gramática, la validación de cadenas y la construcción del árbol.
    """
    # Paso 1: Pedir el archivo de gramática al usuario
    archivo_gramatica = input("Ingresa el nombre del archivo de gramática (.txt): ")

    # Paso 2: Leer la gramática desde el archivo
    gramatica, simbolo_inicial, terminales, no_terminales = leer_gramatica(archivo_gramatica)

    # Paso 3: Imprimir los detalles de la gramática
    imprimir_gramatica(gramatica, simbolo_inicial, terminales, no_terminales)

    # Paso 4: Pedir la cadena de texto al usuario
    cadena = input("Ingresa la cadena para verificar (usa espacios para simbolizar 'ε'): ")

    # Reemplazar espacios en la cadena por el símbolo de vacío (ε)
    cadena = cadena.replace(" ", "ε")

    # Paso 5: Validar la cadena ingresada
    if cadena == "":
        cadena = "ε"  # Si está vacía, la representamos como ε (cadena vacía)

    if es_valida_cadena(gramatica, cadena.replace("ε", "")):  # Validar la cadena sin ε
        print(f"La cadena '{cadena}' es válida.")
        construir_arbol(gramatica, cadena.replace("ε", ""))  # Construir árbol de derivación
    else:
        print(f"La cadena '{cadena}' no es válida.")

# Ejecutar el programa principal si es el script principal
if __name__ == "__main__":
    main()
