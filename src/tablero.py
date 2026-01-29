# tablero.py

# QUE: Convierte una cadena de 36 caracteres en un tablero de 6x6.
# POR QUE: Para facilitar el acceso y la manipulación de las posiciones en la cuadricula del juego.
def def_tablero(s):
    tablero = []
    
    # Divide la cadena en filas consecutivas de 6 caracteres
    for i in range(6):
        fila = list(s[i * 6:(i + 1) * 6])
        tablero.append(fila)
    
    return tablero

# QUE: Imprime una representación del tablero.
# POR QUE: Funcionalidad adicional para visualizar la solución paso a paso 
def print_tablero(cadena):
    # Recorre las filas del tablero 
    for i in range(6):
        print(' '.join(cadena[i*6:(i+1)*6]))
    
    # Línea separadora para mejorar la claridad visual
    print('-' * 12)
