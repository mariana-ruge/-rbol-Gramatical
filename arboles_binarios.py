# Importar las librerías necesarias
import networkx as nx  # Para construir y manipular grafos
import matplotlib.pyplot as plt  # Para generar gráficos
from networkx.drawing.nx_agraph import graphviz_layout  # Para ajustar el grafo a una estructura de árbol

#Declarar la clase nodo 
class Nodo:
    #Atributos
    _id_counter = 0  # Contador para asignar IDs únicos a los nodos
    def __init__(self, valor):
        self.valor = valor  # Asigna el valor del nodo
        self.izquierda = None  # Inicializa el hijo izquierdo como None
        self.derecha = None  # Inicializa el hijo derecho como None
        self.id = Nodo._id_counter  # Asigna un ID único al nodo
        Nodo._id_counter += 1  # Incrementa el contador de IDs para el próximo nodo

# Función para leer la gramática desde un archivo
def leer_gramatica(archivo_gramatica):
    # Abre el archivo en modo lectura
    with open(archivo_gramatica, 'r') as archivo:
        Vt = set()  # Inicializa un conjunto vacío para los terminales
        Vxt = set()  # Inicializa un conjunto vacío para los no terminales
        P = []  # Inicializa una lista vacía para las producciones
        S = None  # Inicializa el símbolo inicial como None

        # Leer las diferentes partes de la gramática
        for linea in archivo:
            linea = linea.strip()  # Elimina espacios en blanco al inicio y final de la línea
            if linea.startswith('Vt:'):
                Vt = set(linea.replace('Vt:', '').strip().split())  # Lee los terminales
            elif linea.startswith('Vxt:'):
                Vxt = set(linea.replace('Vxt:', '').strip().split())  # Lee los no terminales
            elif linea.startswith('S:'):
                S = linea.replace('S:', '').strip()  # Lee el símbolo inicial
            elif linea.startswith('P:'):
                break  # Termina la lectura de la parte inicial

        # Leer las producciones, del archivo txt
        for linea in archivo:
            linea = linea.strip()  # Elimina espacios en blanco al inicio y final de la línea
            if '->' in linea:
                izquierda, derecha = linea.split('->')  # Separa la parte izquierda y derecha de la producción
                izquierda = izquierda.strip()  # Elimina espacios en blanco de la parte izquierda
                derecha = derecha.strip().split()  # Convierte la parte derecha en una lista de símbolos
                P.append((izquierda, derecha))  # Agrega la producción a la lista de producciones

        # Verificar que todos los componentes de la gramática estén presentes
        if not (Vt and Vxt and S and P):
            #Si uno de los elementos no esta presente, se alza una excepcion para eviatr que el programa se rompa
            raise ValueError("La gramática no está completa o el formato es incorrecto.")
        return Vt, Vxt, S, P  # Devuelve los componentes de la gramática

# Función para validar la gramática
def validar_gramatica(Vt, Vxt, S, P):
    #Buscar el simbolo inicial dentro de los terminales
    if S not in Vxt:
        raise ValueError("El símbolo inicial no está en el conjunto de no terminales.")
    #Recorrer la izquierda y la derecha de los productos en el arbol que se genera
    for izq, der in P:
        #Buscar los terminales por la izquierda
        if izq not in Vxt:
            #Levantar la excepción si no encuentran los terminales
            raise ValueError(f"El lado izquierdo de la producción '{izq} -> {' '.join(der)}' no es un no terminal.")
        #Buscar los simbolos en la producción
        #Buscar por la derecha del recirrido
        for simbolo in der:
            #Si no se encuentra el simbolo en la producción
            if simbolo != 'ε' and simbolo not in Vt and simbolo not in Vxt:
                raise ValueError(f"El símbolo '{simbolo}' en la producción '{izq} -> {' '.join(der)}' no es válido.")

# Función para validar una cadena según la gramática
def validar_cadena(cadena, Vt, Vxt, S, P):
    #Recorrer los simbolos y buscar los terminales 
    def derivar(actual, resto, arbol_nodo):
        if not actual:
            return not resto, arbol_nodo  # Si no hay más símbolos por procesar, la cadena es válida si no queda resto

        simbolo_actual = actual[0]  # Toma el primer símbolo de la lista actual

        if simbolo_actual in Vt:  # Si el símbolo actual es un terminal
            if resto and simbolo_actual == resto[0]:  # Si coincide con el primer símbolo del resto
                hoja = Nodo(simbolo_actual)  # Crea un nodo hoja con el símbolo
                arbol_nodo.izquierda = hoja  # Lo agrega como hijo izquierdo
                return derivar(actual[1:], resto[1:], arbol_nodo), arbol_nodo  # Continúa la derivación
            return False, None  # Si no coincide, la cadena no es válida

        if simbolo_actual in Vxt:  # Si el símbolo actual es un no terminal
            for izq, der in P:  # Recorre las producciones
                if izq == simbolo_actual:  # Si encuentra una producción aplicable
                    subarbol = Nodo(izq)  # Crea un nodo para el no terminal
                    if arbol_nodo.izquierda is None:
                        arbol_nodo.izquierda = subarbol  # Lo agrega como hijo izquierdo si no tiene
                    else:
                        arbol_nodo.derecha = subarbol  # O como hijo derecho si ya tiene izquierdo

                    if der == ['ε']:  # Si es una producción epsilon
                        valido, _ = derivar(actual[1:], resto, subarbol)  # Deriva sin consumir símbolo del resto
                        if valido:
                            return True, arbol_nodo
                    else:
                        nuevo_actual = der + actual[1:]  # Reemplaza el no terminal por su producción
                        valido, nuevo_arbol = derivar(nuevo_actual, resto, subarbol)  # Continúa la derivación
                        if valido:
                            return True, arbol_nodo
            return False, None  # Si no se encuentra una derivación válida

        return False, None  # Si el símbolo no es ni terminal ni no terminal

    tokens = list(cadena.replace(" ", ""))  # Convierte la cadena en una lista de tokens sin espacios
    valido, arbol = derivar([S], tokens, Nodo(S))  # Inicia la derivación desde el símbolo inicial
    return valido, arbol  # Devuelve si la cadena es válida y el árbol de derivación

# Función recursiva para agregar nodos al grafo
def agregar_nodos(grafo, nodo):
    if nodo:
        grafo.add_node(nodo.id, label=nodo.valor)  # Agrega el nodo al grafo
        if nodo.izquierda:
            grafo.add_edge(nodo.id, nodo.izquierda.id)  # Agrega una arista al hijo izquierdo
            agregar_nodos(grafo, nodo.izquierda)  # Procesa recursivamente el hijo izquierdo
        if nodo.derecha:
            grafo.add_edge(nodo.id, nodo.derecha.id)  # Agrega una arista al hijo derecho
            agregar_nodos(grafo, nodo.derecha)  # Procesa recursivamente el hijo derecho

# Función para dibujar el árbol de derivación
def dibujar_arbol(raiz, expresion):
    grafo = nx.DiGraph()  # Crea un nuevo grafo dirigido
    agregar_nodos(grafo, raiz)  # Agrega los nodos al grafo

    try:
        pos = graphviz_layout(grafo, prog='dot')  # Calcula las posiciones de los nodos
    except:
        print("Error: graphviz_layout requiere que pygraphviz o pydot estén instalados.")
        return

    etiquetas = nx.get_node_attributes(grafo, 'label')  # Obtiene las etiquetas de los nodos

    #Posiciones de las ventanas de los grafos
    nx.draw(grafo, pos, labels=etiquetas, with_labels=True, arrows=True, node_size=2000, node_color='lightblue')
    plt.title(f"Árbol de Derivación para la Expresión: {expresion}")  # Agrega un título al gráfico
    plt.show()  # Muestra el gráfico

# Función principal para analizar una gramática
def analizar_gramatica(archivo_gramatica):
    try:
        Vt, Vxt, S, P = leer_gramatica(archivo_gramatica)  # Lee la gramática del archivo

        # Imprime los componentes de la gramática
        print("\nComponentes de la Gramática:")
        print(f"Terminales (Vt): {Vt}")
        print(f"No terminales (Vxt): {Vxt}")
        print(f"Símbolo inicial (S): {S}")
        print("Producciones (P):")
        for izquierda, derecha in P:
            print(f"  {izquierda} -> {' '.join(derecha)}")

        validar_gramatica(Vt, Vxt, S, P)  # Valida la gramática

        # Bucle principal para validar cadenas
        while True:
            cadena = input("\nIngrese la cadena a validar (o 'salir' para terminar): ")
            if cadena.lower() == 'salir':
                break

            valido, arbol = validar_cadena(cadena, Vt, Vxt, S, P)  # Valida la cadena
            if valido:
                print(f"La cadena '{cadena}' es válida según la gramática.")
                dibujar_arbol(arbol, cadena)  # Dibuja el árbol de derivación
            else:
                print(f"La cadena '{cadena}' no es válida según la gramática.")

    except Exception as e:
        print(f"Error: {str(e)}")  # Imprime cualquier error que ocurra

# Función para analizar expresiones aritméticas
def analizar_aritmetica(archivo_gramatica):
    try:
        Vt, Vxt, S, P = leer_gramatica(archivo_gramatica)  # Lee la gramática del archivo

        # Imprime los componentes de la gramática aritmética
        print("\nComponentes de la Gramática Aritmética:")
        print(f"Terminales (Vt): {Vt}")
        print(f"No terminales (Vxt): {Vxt}")
        print(f"Símbolo inicial (S): {S}")
        print("Producciones (P):")
        for izquierda, derecha in P:
            print(f"  {izquierda} -> {' '.join(derecha)}")

        validar_gramatica(Vt, Vxt, S, P)  # Valida la gramática

        # Bucle principal para validar expresiones aritméticas
        while True:
            expresion = input("\nIngrese la expresión aritmética a validar (o 'salir' para terminar): ")
            #Validar si se selecciono salir en el menú
            if expresion.lower() == 'salir':
                break

            valido, arbol = validar_cadena(expresion, Vt, Vxt, S, P)  # Valida la expresión
            if valido:
                print(f"La expresión aritmética '{expresion}' es válida según la gramática.")
                dibujar_arbol(arbol, expresion)  # Dibuja el árbol de derivación
            else:
                print(f"La expresión aritmética '{expresion}' no es válida según la gramática.")

    except Exception as e:
        print(f"Error: {str(e)}")  # Imprime cualquier error que ocurra

# Función del menú principal
def menu():
    #Mientras se esté corriendo el programa
    while True:
        print("\nSeleccione una opción:")
        print("1. Analizador de gramática") #Analizara la gramática y la cadena que se ingrese por consola
        print("2. Analizador de expresiones aritméticas") #Analizara las expresiones escritas inorder (1 + 1)
        print("3. Salir") #Rompe el while
        opcion = input("Ingrese su opción (1/2/3): ") #Solicitar la opción al usuario

        #Iterar sobre la opción
        if opcion == '1':
            #Analizador de gramaticas, cargar el archivo
            archivo_gramatica = input("Ingrese el nombre del archivo de gramática (con extensión .txt): ")
            analizar_gramatica(archivo_gramatica)  # Llama a la función de análisis de gramática
        elif opcion == '2':
            #Busca la gramatica de las expresiones matemáticas
            archivo_gramatica = input("Ingrese el nombre del archivo de gramática aritmética (con extensión .txt): ")
            analizar_aritmetica(archivo_gramatica)  # Llama a la función de análisis de expresiones aritméticas
        elif opcion == '3':
            #Salir del programa y romper el while
            print("Saliendo...")
            break  # Sale del bucle y termina el programa
        else:
            print("Opción no válida. Intente de nuevo.")

# Punto de entrada del programa
if __name__ == "__main__":
    menu()  # Llama a la función del menú principal