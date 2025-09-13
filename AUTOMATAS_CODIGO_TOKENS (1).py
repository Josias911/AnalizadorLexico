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

