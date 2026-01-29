# movimientos.py
from collections import defaultdict
from tablero import def_tablero

# QUE: Obtiene un diccionario con las posiciones de cada vehiculo en el tablero.
# POR QUE: Para analizar la orientación y posición, necesario para calcular movimientos.
def vehiculo(tablero):
    pos = defaultdict(list)
    
    # Recorre todas las casillas del tablero 6x6
    for r in range(6):
        for c in range(6):
            # Si la casilla no está vacía ('o'), pertenece a un vehículo
            if (ch := tablero[r][c]) != 'o':
                pos[ch].append((r, c))
    
    # Devuelve un diccionario: vehículo -> lista de posiciones
    return pos

# QUE: Aplica una secuencia de movimientos a un estado y devuelve el nuevo estado.
# POR QUE: Para generar los nuevos estados sucesores y responder a la consulta '--move', incluyendo validaciones de colisión.
def apply_moves(s, moves):
    # Convierte la cadena en una matriz 6x6
    tablero = def_tablero(s)
    
    # Procesa cada movimiento de la lista
    for move in moves:
        # Movimiento inválido si es demasiado corto
        if len(move) < 2:
            continue
        
        # Identificador del vehículo (letra)
        vehicle_id = move[0]
        
        # Dirección del movimiento ('+' o '-')
        direction = move[1]
        
        # Número de pasos a mover
        try:
            steps = int(move[2:]) 
        except:
            continue

        # Obtiene las posiciones actuales de los vehículos
        posiciones = vehiculo(tablero)
        
        # Si el vehículo no existe, ignora el movimiento
        if vehicle_id not in posiciones:
            continue
        
        pos_list = posiciones[vehicle_id]
        
        # Extrae filas y columnas ocupadas por el vehículo
        rows = [r for r, _ in pos_list]
        cols = [c for _, c in pos_list]
        
        # Un vehículo es horizontal si todas las filas son iguales
        is_horizontal = len(set(rows)) == 1

        # --- Lógica de Movimiento y Validación Específica ---
        
        # Movimiento horizontal a la derecha (+)
        if is_horizontal and direction == '+':
            new_cols = [c + steps for c in cols]
            current_cols = set(cols)
            
            # Comprueba límites del tablero y colisiones
            is_valid = (
                max(new_cols) < 6 and 
                all(
                    0 <= c < 6 and
                    (c in current_cols or tablero[rows[0]][c] == 'o')
                    for c in new_cols
                )
            )
            
            # Aplica el movimiento si es válido
            if is_valid:
                for r, c in pos_list:
                    tablero[r][c] = 'o'
                for c in new_cols:
                    tablero[rows[0]][c] = vehicle_id
        
        # Movimiento horizontal a la izquierda (-)
        elif is_horizontal and direction == '-':
            new_cols = [c - steps for c in cols]
            current_cols = set(cols)
            
            is_valid = (
                min(new_cols) >= 0 and
                all(
                    0 <= c < 6 and
                    (c in current_cols or tablero[rows[0]][c] == 'o')
                    for c in new_cols
                )
            )
                
            if is_valid:
                for r, c in pos_list:
                    tablero[r][c] = 'o'
                for c in new_cols:
                    tablero[rows[0]][c] = vehicle_id
        
        # Movimiento vertical hacia abajo (-)
        elif not is_horizontal and direction == '-':
            new_rows = [r + steps for r in rows]
            current_rows = set(rows)
            
            is_valid = (
                max(new_rows) < 6 and
                all(
                    0 <= r < 6 and
                    (r in current_rows or tablero[r][cols[0]] == 'o')
                    for r in new_rows
                )
            )
                
            if is_valid:    
                for r, c in pos_list:
                    tablero[r][c] = 'o'
                for r in new_rows:
                    tablero[r][cols[0]] = vehicle_id
        
        # Movimiento vertical hacia arriba (+)
        elif not is_horizontal and direction == '+':
            new_rows = [r - steps for r in rows]
            current_rows = set(rows)
            
            is_valid = (
                min(new_rows) >= 0 and
                all(
                    0 <= r < 6 and
                    (r in current_rows or tablero[r][cols[0]] == 'o')
                    for r in new_rows
                )
            )

            if is_valid:    
                for r, c in pos_list:
                    tablero[r][c] = 'o'
                for r in new_rows:
                    tablero[r][cols[0]] = vehicle_id
        
    # Convierte el tablero modificado de nuevo a cadena plana
    return ''.join(''.join(row) for row in tablero)

# QUE: Calcula y devuelve la lista de sucesores válidos (acción, estado, costo).
# POR QUE: Genera todas las transiciones legales desde el estado actual para la expansión en la búsqueda.
def successors(s):
    # Convierte la cadena plana en una matriz 6x6
    tablero = def_tablero(s)
    
    # Obtiene las posiciones de todos los vehículos del tablero
    posiciones = vehiculo(tablero)
    
    # Lista donde se almacenarán los sucesores generados
    successors_list = []
    
    # Lista ordenada de vehículos (para asegurar orden determinista)
    vehiculos = sorted(k for k in posiciones if k != 'o')
    
    # Se analiza cada vehículo de forma independiente
    for vehiculo_temp in vehiculos:
        pos_list = posiciones[vehiculo_temp]
        
        # Filas y columnas ocupadas por el vehículo
        rows = [r for r, c in pos_list]
        cols = [c for r, c in pos_list]
        
        # Determina la orientación del vehículo
        horizontal = len(set(rows)) == 1
       
        # Límites actuales del vehículo
        min_col = min(cols) if horizontal else 0
        max_col = max(cols) if horizontal else 0
        min_row = min(rows) if not horizontal else 0
        max_row = max(rows) if not horizontal else 0
        
        # Fila o columna fija según orientación
        row = rows[0] if horizontal else 0
        col = cols[0] if not horizontal else 0

        # Contadores de espacios libres disponibles
        max_izq = max_der = max_arriba = max_abajo = 0

        if horizontal:  
            # Cuenta casillas libres a la izquierda
            c = min_col - 1
            while c >= 0 and tablero[row][c] == 'o':
                max_izq += 1
                c -= 1
            
            # Cuenta casillas libres a la derecha
            c = max_col + 1
            while c < 6 and tablero[row][c] == 'o':
                max_der += 1
                c += 1
        else:
            # Cuenta casillas libres hacia arriba
            r = min_row - 1
            while r >= 0 and tablero[r][col] == 'o':
                max_arriba += 1
                r -= 1
            
            # Cuenta casillas libres hacia abajo
            r = max_row + 1
            while r < 6 and tablero[r][col] == 'o':
                max_abajo += 1
                r += 1
        
        # --- Generación de sucesores ---
        # Para cada dirección posible se generan estados intermedios por número de pasos
        
        # Movimiento horizontal a la izquierda
        if horizontal and max_izq > 0:
            for steps in range(1, max_izq + 1):
                new_cols = [c - steps for c in cols]
                
                # Aplica movimiento temporal
                for r, c in pos_list:
                    tablero[r][c] = 'o'
                for c in new_cols:
                    tablero[row][c] = vehiculo_temp
                
                # Construye nuevo estado
                new_state = ''.join(''.join(r) for r in tablero)
                
                # Revierte tablero
                for c in new_cols:
                    tablero[row][c] = 'o'
                for r, c in pos_list:
                    tablero[r][c] = vehiculo_temp
                
                # Añade sucesor (acción, estado, coste)
                successors_list.append([f"{vehiculo_temp}-{steps}", new_state, 6 - steps])
        
        # Movimiento horizontal a la derecha
        if horizontal and max_der > 0:
            for steps in range(1, max_der + 1):
                new_cols = [c + steps for c in cols]
                
                for r, c in pos_list:
                    tablero[r][c] = 'o'
                for c in new_cols:
                    tablero[row][c] = vehiculo_temp
                
                new_state = ''.join(''.join(r) for r in tablero)
                
                for c in new_cols:
                    tablero[row][c] = 'o'
                for r, c in pos_list:
                    tablero[r][c] = vehiculo_temp
                
                successors_list.append([f"{vehiculo_temp}+{steps}", new_state, 6 - steps])
        
        # Movimiento vertical hacia arriba
        if not horizontal and max_arriba > 0:
            for steps in range(1, max_arriba + 1):
                new_rows = [r - steps for r in rows]
                
                for r, c in pos_list:
                    tablero[r][c] = 'o'
                for r in new_rows:
                    tablero[r][col] = vehiculo_temp
                
                new_state = ''.join(''.join(row) for row in tablero)
                
                for r in new_rows:
                    tablero[r][col] = 'o'
                for r, c in pos_list:
                    tablero[r][c] = vehiculo_temp
                
                successors_list.append([f"{vehiculo_temp}+{steps}", new_state, 6 - steps])
        
        # Movimiento vertical hacia abajo
        if not horizontal and max_abajo > 0:
            for steps in range(1, max_abajo + 1):
                new_rows = [r + steps for r in rows]
                
                for r, c in pos_list:
                    tablero[r][c] = 'o'
                for r in new_rows:
                    tablero[r][col] = vehiculo_temp
                
                new_state = ''.join(''.join(row) for row in tablero)
                
                for r in new_rows:
                    tablero[r][col] = 'o'
                for r, c in pos_list:
                    tablero[r][c] = vehiculo_temp
                
                successors_list.append([f"{vehiculo_temp}-{steps}", new_state, 6 - steps])
    
    # --- Ordenación final ---
    # Garantiza una salida estable e idéntica entre ejecuciones
    def clave_orden(item):
        accion = item[0]
        veh = accion[0]
        dir_char = accion[1] if len(accion) > 1 and accion[1] in '+-' else ''
        try:
            num = int(accion[2:])
        except:
            num = 0
        return (veh, dir_char, num)

    successors_list.sort(key=clave_orden)
    return successors_list
