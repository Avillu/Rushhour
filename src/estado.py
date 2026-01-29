# estado.py
from movimientos import successors, apply_moves
from tablero import def_tablero

# QUE: Representa un estado del juego Rush Hour (cadena de 36 caracteres).
# POR QUE: Encapsula la configuración del tablero para los algoritmos de búsqueda.
class Estado:
    
    def __init__(self, cadena, tablero=None, posiciones=None):
        # Comprobación básica de validez del estado
        # El tablero siempre debe ser una cadena de 36 caracteres (6x6)
        if len(cadena) != 36:
            raise ValueError("El estado debe tener 36 caracteres")
        
        # Almacena la representación compacta del tablero
        self.cadena = cadena
        
        # Reutiliza tablero y posiciones si se pasan
        # Esto evita recalcularlos y mejora el rendimiento en la búsqueda
        if tablero is not None and posiciones is not None:
            self.tablero = tablero
            self.posiciones = posiciones
        else:
            # Convierte la cadena plana en una matriz 6x6
            self.tablero = def_tablero(cadena)
            
            # Diccionario: vehículo -> lista de posiciones (r, c)
            # Se ignoran las casillas vacías ('o')
            self.posiciones = {ch: [] for ch in set(cadena) if ch != 'o'}
            
            # Recorre el tablero para registrar las posiciones de cada vehículo
            for r in range(6):
                for c in range(6):
                    ch = self.tablero[r][c]
                    if ch != 'o':
                        self.posiciones[ch].append((r, c))

    # --- Métodos de comportamiento ---

    # QUE: Genera los sucesores del estado actual.
    # POR QUE: Es la operación fundamental para expandir nodos en la búsqueda.
    def successors(self):
        # Devuelve una lista de triples: (acción, nueva_cadena, coste)
        return successors(self.cadena)

    # QUE: Aplica un único movimiento a un vehículo.
    # POR QUE: Permite generar nuevos estados de forma controlada.
    def mover(self, vehiculo_id, direccion, pasos):
        # Codifica el movimiento en el formato estándar 
        move = f"{vehiculo_id}{direccion}{pasos}"
        
        # Aplica el movimiento sobre la cadena actual
        nueva_cadena = apply_moves(self.cadena, [move])
        
        # Devuelve un nuevo objeto Estado
        return Estado(nueva_cadena)

    # QUE: Comprueba si el estado es objetivo.
    # POR QUE: El problema termina cuando el vehículo A alcanza la salida.
    def es_meta(self):
        # El coche rojo 'A' debe ocupar la posición (fila 2, columna 5)
        return any(r == 2 and c == 5 for r, c in self.posiciones.get('A', []))

    # QUE: Calcula el valor heurístico del estado.
    # POR QUE: Guía la búsqueda informada (GBF y A*) hacia la solución.
    def heuristica(self, tipo: int) -> int:
        """
        Calcula la heurística de forma muy eficiente directamente sobre la cadena.
        
        Args:
            tipo: 0 → distancia del coche rojo a la salida
                  1 → número de vehículos bloqueando la fila de salida
                  2 → suma de ambas (más informada)
        
        Returns:
            Valor heurístico (cuanto menor, mejor)
        """
        # Buscamos todas las posiciones del coche rojo 'A' en la cadena plana
        a_positions = [i for i in range(36) if self.cadena[i] == 'A']
        
        # Si no existe el coche rojo heurística nula
        if not a_positions:
            return 0
        
        # Columna más a la derecha del coche rojo 
        max_col = max(i % 6 for i in a_positions)
        
        if tipo == 0:
            # Número de casillas que le faltan al coche rojo para salir
            return 5 - max_col
        
        elif tipo == 1:
            # Cuenta vehículos distintos bloqueando la salida en la fila 2
            blocking = set()
            for col in range(max_col + 1, 6):
                idx = 12 + col  # Fila 2 corresponde a índices 12..17
                ch = self.cadena[idx]
                if ch != 'o':
                    blocking.add(ch)
            return len(blocking)
        
        elif tipo == 2:
            # Heurística combinada: distancia + bloqueos
            h0 = 5 - max_col
            h1 = len({
                self.cadena[12 + col]
                for col in range(max_col + 1, 6)
                if self.cadena[12 + col] != 'o'
            })
            return h0 + h1
        
        else:
            raise ValueError("Heurística inválida: debe ser 0, 1 o 2")

    # --- Representación y Hashing ---

    # Representación textual del estado
    def __str__(self):
        return self.cadena

    # Dos estados son iguales si su cadena es idéntica
    def __eq__(self, other):
        return isinstance(other, Estado) and self.cadena == other.cadena

    # Permite usar Estado en conjuntos y diccionarios
    def __hash__(self):
        return hash(self.cadena)
