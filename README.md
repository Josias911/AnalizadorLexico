Documentación del Analizador Léxico

1. Descripción General
Este programa implementa un analizador léxico en Python que permite identificar, clasificar y contar los distintos tokens presentes en un archivo de entrada que contiene código fuente en pseudocódigo. El sistema reconoce palabras reservadas, operadores, variables, números, cadenas de texto, comentarios, entre otros. Además, genera un reporte detallado con estadísticas, errores encontrados y una tabla de clasificación.

2. Estructura del Código
Definición de Tokens
Se usa una lista TOKENS que define los tipos de elementos a reconocer mediante expresiones regulares (regex):

- PALABRA_RESERVADA → Algoritmo, Definir, Leer, Si, Entonces, Si no, etc.
- OPERADOR_ARITMÉTICO → +, -, *, /, =, ^
- OPERADOR_RELACIONAL → >, <, ==, !=, <=, >=, <>, Y, O
- SIGNO_AGRUPACION → (), {}, []
- COMENTARIO_LINEA → // ...
- COMENTARIO_BLOQUE → /* ... */
- CADENA_TEXTO → "texto"
- NUMERO → Enteros y reales
- VARIABLE → Identificadores
- FIN_LINEA → ;
- COMA → ,
- ESPACIO → espacios en blanco
- ERROR → cualquier otro carácter no reconocido


Clase AnalizadorLexico
Encapsula toda la lógica del analizador.

Principales atributos:
- tokens_regex: regex principal para los tokens
- pattern_bloque: regex especial para comentarios de bloque
- conteo: diccionario con la frecuencia de cada token
- errores: lista de errores léxicos encontrados
- todos_tokens: lista con todos los tokens detectados



Métodos principales:
1. analizar_archivo(archivo_entrada): Lee el archivo, elimina comentarios de bloque y ejecuta el análisis.


2. analizar(codigo): Recorre línea por línea el código, identificando tokens y errores.
   Guarda información de cada token: tipo, valor, línea y columna.


3. generar_reporte_completo(archivo_entrada, archivo_salida): Genera un archivo de texto con:

   - Resumen general (tokens, errores, porcentaje de éxito).
   - Clasificación detallada por tipo.
   - Tabla de conteos.
   - Lista completa de tokens.
   - Errores encontrados.
   - Estadísticas finales.

Función main()
Verifica si se pasó un archivo como argumento, o lo pide por consola. Crea un objeto AnalizadorLexico y ejecuta el análisis. Guarda el reporte en la carpeta Documents del usuario con un nombre como: Analisis_YYYYMMDD_HHMMSS.txt. Muestra en consola un resumen rápido del análisis.
3. Flujo de Ejecución
1. Entrada → archivo de código fuente en pseudocódigo.
2. Proceso → se eliminan comentarios de bloque y se analizan las líneas.
3. Salida → reporte detallado en .txt y resumen en consola.



4. Ejemplo de Uso
Ejecución por terminal:
python AUTOMATAS_CODIGO_TOKENS.py ejemplo_algoritmo.txt
Salida esperada en consola:
<img width="972" height="457" alt="image" src="https://github.com/user-attachments/assets/9f83b036-c564-43b4-b8f3-eadd2323f281" />

