import re
import sys
import os
from collections import defaultdict
from datetime import datetime

# Definición de tokens con sus patrones regex
TOKENS = [
    ('PALABRA_RESERVADA', r'\b(Algoritmo|Definir|Como|Entero|Real|Caracter|Leer|Repetir|Hasta Que|Escribir|FinAlgoritmo|Si|Entonces|Sino|FinSi|Segun|Hacer|Caso|De Otro Modo|FinSegun)\b'),
    ('OPERADOR_ARITMETICO', r'(\+|\-|\*|\/|\=|\^)'),
    ('OPERADOR_RELACIONAL', r'(>|<|==|!=|<=|>=|<>|Y|O)'),
    ('SIGNO_AGRUPACION', r'(\(|\)|\{|\}|\[|\])'),
    ('COMENTARIO_LINEA', r'//.*'),
    ('COMENTARIO_BLOQUE', r'/\*.*?\*/'),  # CORREGIDO: sin re.DOTALL aquí
    ('CADENA_TEXTO', r'\"[^\"]*\"'),
    ('NUMERO', r'\b\d+(\.\d+)?\b'),
    ('VARIABLE', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),
    ('FIN_LINEA', r';'),
    ('COMA', r','),
    ('ESPACIO', r'\s+'),
    ('ERROR', r'.')  # Cualquier caracter no reconocido
]

class AnalizadorLexico:
    def __init__(self):
        # Filtrar COMENTARIO_BLOQUE para la regex principal
        tokens_filtrados = [(nombre, patron) for nombre, patron in TOKENS if nombre != 'COMENTARIO_BLOQUE']
        self.tokens_regex = '|'.join(f'(?P<{nombre}>{patron})' for nombre, patron in tokens_filtrados)
        self.pattern = re.compile(self.tokens_regex)
        self.pattern_bloque = re.compile(r'/\*.*?\*/', re.DOTALL)  # Compilado por separado
        self.conteo = defaultdict(lambda: defaultdict(int))
        self.errores = []
        self.todos_tokens = []

def analizar_archivo(self, archivo_entrada):
        try:
            with open(archivo_entrada, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Primero eliminar comentarios de bloque
            contenido = self.pattern_bloque.sub('', contenido)
            
            return self.analizar(contenido)
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo '{archivo_entrada}'")
            return False
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return False
 
    def analizar(self, codigo):
        linea_num = 1
        pos_linea = 0
        tokens = []
        
        lineas = codigo.split('\n')
        
        for num_linea, linea in enumerate(lineas, 1):
            pos = 0
            while pos < len(linea):
                match = self.pattern.match(linea, pos)
                if match:
                    tipo = match.lastgroup
                    valor = match.group()
                    inicio = match.start()
                    
                    if tipo == 'ESPACIO':
                        pos = match.end()
                        continue
                    elif tipo == 'COMENTARIO_LINEA':
                        break  # Terminar esta línea
                    elif tipo == 'ERROR':
                        self.errores.append({
                            'linea': num_linea,
                            'columna': inicio + 1,
                            'valor': valor
                        })
                    else:
                        token_info = {
                            'tipo': tipo,
                            'valor': valor,
                            'linea': num_linea,
                            'columna': inicio + 1
                        }

                        tokens.append(token_info)
                        self.todos_tokens.append(token_info)
                        
                        # Actualizar conteo
                        if tipo in ['PALABRA_RESERVADA', 'SIGNO_AGRUPACION', 
                                   'OPERADOR_ARITMETICO', 'OPERADOR_RELACIONAL',
                                   'VARIABLE', 'NUMERO', 'CADENA_TEXTO', 'COMA']:
                            self.conteo[tipo][valor] += 1
                    
                    pos = match.end()
                else:
                    # Carácter no reconocido
                    self.errores.append({
                        'linea': num_linea,
                        'columna': pos + 1,
                        'valor': linea[pos]
                    })
                    pos += 1
        
        return tokens
            def generar_reporte_completo(self, archivo_entrada, archivo_salida):
        try:
            # Crear directorio si no existe
            directorio = os.path.dirname(archivo_salida)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)
                
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                # Encabezado del reporte
                f.write("=" * 60 + "\n")
                f.write("ANÁLISIS LÉXICO - REPORTE DE CLASIFICACIÓN\n")
                f.write("=" * 60 + "\n")
                f.write(f"Archivo analizado: {archivo_entrada}\n")
                f.write(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                
                # 1. RESUMEN GENERAL
                f.write("1. RESUMEN GENERAL\n")
                f.write("-" * 40 + "\n")
                total_tokens = len(self.todos_tokens)
                total_errores = len(self.errores)
                
                f.write(f"Total de tokens encontrados: {total_tokens}\n")
                f.write(f"Total de errores léxicos: {total_errores}\n")
                f.write(f"Porcentaje de éxito: {((total_tokens/(total_tokens + total_errores)) * 100 if total_tokens + total_errores > 0 else 100):.2f}%\n\n")
                
                # 2. CLASIFICACIÓN DETALLADA POR TIPO
                f.write("2. CLASIFICACIÓN DETALLADA POR TIPO\n")
                f.write("-" * 40 + "\n")
                
                categorias = {
                    'PALABRA_RESERVADA': 'PALABRAS RESERVADAS',
                    'VARIABLE': 'VARIABLES',
                    'NUMERO': 'NÚMEROS',
                    'CADENA_TEXTO': 'CADENAS DE TEXTO',
                    'OPERADOR_ARITMETICO': 'OPERADORES ARITMÉTICOS',
                    'OPERADOR_RELACIONAL': 'OPERADORES RELACIONALES',
                    'SIGNO_AGRUPACION': 'SIGNOS DE AGRUPACIÓN',
                    'COMA': 'COMAS',
                    'FIN_LINEA': 'FIN DE LÍNEA'
                }

                
                for token_type, categoria in categorias.items():
                    if token_type in self.conteo:
                        f.write(f"\n{categoria}:\n")
                        for valor, conteo in sorted(self.conteo[token_type].items()):
                            f.write(f"  {valor}: {conteo}\n")

   # 3. TABLA DE CONTEOS (como en el ejemplo del proyecto)
                f.write("\n3. TABLA DE CONTEOS\n")
                f.write("-" * 40 + "\n")
                f.write("| Elemento            | Palabra       | Conteo |\n")
                f.write("|---------------------|---------------|--------|\n")
                
                # Palabras reservadas
                if 'PALABRA_RESERVADA' in self.conteo:
                    primera = True
                    for palabra, conteo in sorted(self.conteo['PALABRA_RESERVADA'].items()):
                        if primera:
                            f.write(f"| Palabras Reservadas | {palabra:<13} | {conteo:<6} |\n")
                            primera = False
                        else:
                            f.write(f"|                     | {palabra:<13} | {conteo:<6} |\n")
                
                # Signos de agrupación
                if 'SIGNO_AGRUPACION' in self.conteo:
                    primera = True
                    for signo, conteo in sorted(self.conteo['SIGNO_AGRUPACION'].items()):
                        if primera:
                            f.write(f"| Signos Agrupación   | {signo:<13} | {conteo:<6} |\n")
                            primera = False
                        else:
                            f.write(f"|                     | {signo:<13} | {conteo:<6} |\n")
                
                # Operadores
                if 'OPERADOR_ARITMETICO' in self.conteo:
                    primera = True
                    for op, conteo in sorted(self.conteo['OPERADOR_ARITMETICO'].items()):
                        if primera:
                            f.write(f"| Operadores Aritm.   | {op:<13} | {conteo:<6} |\n")
                            primera = False
                        else:
                            f.write(f"|                     | {op:<13} | {conteo:<6} |\n")
                
                # Variables
                if 'VARIABLE' in self.conteo:
                    primera = True
                    for var, conteo in sorted(self.conteo['VARIABLE'].items()):
                        if primera:
                            f.write(f"| Variables           | {var:<13} | {conteo:<6} |\n")
                            primera = False
                        else:
                            f.write(f"|                     | {var:<13} | {conteo:<6} |\n")
                
                # 4. LISTA COMPLETA DE TOKENS
                f.write("\n4. LISTA COMPLETA DE TOKENS\n")
                f.write("-" * 40 + "\n")
                f.write("| Línea | Columna | Tipo                 | Valor\n")
                f.write("|-------|---------|----------------------|---------\n")
                
                for token in self.todos_tokens:
                    f.write(f"| {token['linea']:<5} | {token['columna']:<7} | {token['tipo']:<20} | {token['valor']}\n")
 # 5. ERRORES ENCONTRADOS
                if self.errores:
                    f.write("\n5. ERRORES LÉXICOS\n")
                    f.write("-" * 40 + "\n")
                    f.write("| Línea | Columna | Carácter | Descripción\n")
                    f.write("|-------|---------|----------|------------\n")
                    
                    for error in self.errores:
                        f.write(f"| {error['linea']:<5} | {error['columna']:<7} | {error['valor']:<8} | Carácter no reconocido\n")
                
                # 6. ESTADÍSTICAS FINALES
                f.write("\n6. ESTADÍSTICAS FINALES\n")
                f.write("-" * 40 + "\n")
                for token_type in categorias.keys():
                    if token_type in self.conteo:
                        total = sum(self.conteo[token_type].values())
                        f.write(f"{categorias[token_type]}: {total}\n")
                
                f.write(f"TOTAL TOKENS: {total_tokens}\n")
                f.write(f"TOTAL ERRORES: {total_errores}\n")
                
                f.write("\n" + "=" * 60 + "\n")
                f.write("FIN DEL REPORTE\n")
                f.write("=" * 60 + "\n")
            
            print(f"✓ Reporte completo generado en: '{archivo_salida}'")
            return True
        except Exception as e:
            print(f"✗ Error al generar el reporte: {e}")
            return False

def main():
    if len(sys.argv) > 1:
        archivo_entrada = sys.argv[1]
    else:
        archivo_entrada = input("Por favor, ingrese la ruta del archivo a analizar: ")
    
    analizador = AnalizadorLexico()
    
    if analizador.analizar_archivo(archivo_entrada):
        # Carpeta del archivo de entrada
        carpeta_actual = os.path.dirname(archivo_entrada)
        nombre_salida = f"Analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        ruta_completa = os.path.join(carpeta_actual, nombre_salida)

        
        # Generar reporte completo en directorio especifico
        analizador.generar_reporte_completo(archivo_entrada, ruta_completa)
        
        # Mostrar resumen en consola
        print("\n" + "=" * 50)
        print("RESUMEN DEL ANÁLISIS")
        print("=" * 50)
        
        total_tokens = len(analizador.todos_tokens)
        total_errores = len(analizador.errores)
        
        print(f"Tokens reconocidos: {total_tokens}")
        print(f"Errores encontrados: {total_errores}")
        
        if total_errores > 0:
            print("\nErrores encontrados:")
            for error in analizador.errores:
                print(f"  Línea {error['linea']}, Columna {error['columna']}: '{error['valor']}'")
        else:
            print("✓ No se encontraron errores léxicos")
            
        print(f"\nEl reporte detallado se guardó en: {ruta_completa}")
        
    else:
        print("El análisis no pudo completarse")

if __name__ == "__main__":
    main()
