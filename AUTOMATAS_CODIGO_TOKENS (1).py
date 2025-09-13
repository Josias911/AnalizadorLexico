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



