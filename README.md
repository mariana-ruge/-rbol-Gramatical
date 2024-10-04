# Árbol Gramatical

 **Realizado por:**
 - Mariana Ruge Vargas
 - Andrés Sebastian Urrego Amaya
 - Julian Esteban Rincón Rodríguez
 - Sebastián Cortés Briceño
 

## Descripción
Este repositorio contiene la implementación para la construcción de un árbol gramatical a partir de una cadena libre de texto que es validada anteriormente, y muestra la representación de la cadena recibida según la gramática solicitada.


###  Funciones
En analizador realiza las siguientes funciones.
1. **Lee una gramática** Desde un archivo.txt
2. **Valida las cadenas** Se valida la entrada según la entrada.
3. **Construye un árbol sintáctico** representa la derivación de una cadena u operación aritmética.
4. **Mostrar el árbol** Se grafica por medio de matplotlib.

### Archivo de gramática (cadenas)
Esta se compone de los siguientes elementos para poder ser procesado correctamente. 

- **Terminales (Vt):** Lista de símbolos terminales.
- **No terminales (Vxt):** Lista de símbolos no terminales.
- **Símbolo inicial (S):** El símbolo inicial de la gramática.
- **Producciones (P):** Conjunto de producciones en la forma `X -> Y Z`, donde `X` es un no terminal y `Y Z` son secuencias de terminales y/o no terminales.

## Uso
- Para correr este programa debes hacer lo siguiente:
	### Requisitos
	1.**Tener Python instalado, puedes verificarlo de la siguiente forma**

    		python --version

	En caso de no tenerlo instalado ejecuta:

	  	sudo apt install python

	2.**Tener Network X (version 3.1) instalado, puedes verificarlo con:**

		pip show networkx
    
    En caso de no tenerlo instalado ejecuta:

			pip install networkx

	3. . **Tener pygraphviz  (version 1.13) instalado, puedes verificarlo con:**

			pip show pygraphviz

	En caso de no tenerlo instalado ejecuta:

			pip install pygraphviz


### Clonar el repositorio
- Una vez has verificado que todos los requerimientos, puedes proceder a clonar este repositorio de forma local. Para ello sigue estos pasos:

	1. Ubicate en la carpeta donde vas a clonar el repositorio.
	
			cd Expresiones
	
	2.  Ejecuta el comando de git para clonar el proyecto
	
			git clone https://github.com/mariana-ruge/Arbol-Gramatical.git
	
	3. Accede a la carpeta que ha clonado llamada, Arbol-Gramatical
	
			cd Arbol-Gramatical

	4. Verifica el contenido de la carpeta
			ls

		Debes ver 3 archivos:
		1. **gramatica.py:** 
		Este archivo es el núcleo del programa. Se encarga de: Leer y validar una gramática desde un archivo de texto. Validar las cadenas de entrada según la gramática proporcionada. Construir un árbol sintáctico que representa la derivación de la cadena válida.

		2.  **gramatica.txt** Es el archivo que contiene la gramática a evaluar en cada 		una de las entradas o inputs. 
		Incluye los símbolos terminales, no terminales, el símbolo inicial y las producciones necesarias para la validación.
		3.  **gramatica2.txt** Es el archivo que contiene la gramática a evaluar en cada 		una de las entradas o inputs. 
		Incluye los símbolos terminales, no terminales, el símbolo inicial y las producciones necesarias para la validación.

### Ejecutar el programa
- Con los archivos en tu entorno local deberás, en tu terminal unix, ejecutar el programa.
- Usa el siguiente comando para correr el programa en tu entorno local.

			python arboles_binarios.py
		
- El programa solicitará el archivo .txt con la cadena a validar, mostrará la gramática que este contiene, una vez ingresas la cadena, si esta es válida se mostrará el árbol.
`