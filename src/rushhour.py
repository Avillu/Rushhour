# rushhour.py
import argparse
from movimientos import vehiculo, successors, apply_moves
from tablero import def_tablero, print_tablero

# QUE: Verifica si la cadena representa un nivel válido y retorna un código de error o 0 si es válido.
# POR QUE: Para implementar la acción 'verify' que comprueba la validez del nivel según las reglas especificadas.
def verify(s):
    # Comprueba longitud y caracteres válidos
    if len(s) != 36 or not all(c.isupper() or c == 'o' for c in s):
        return 1 if len(s) != 36 else 2

    tablero = def_tablero(s)
    posiciones = vehiculo(tablero)

    # El coche rojo debe existir
    if 'A' not in posiciones:
        return 3

    # Comprobación específica del coche rojo
    a_pos = posiciones['A']
    a_rows = {r for r, _ in a_pos}
    a_cols = {c for _, c in a_pos}

    # Debe ser horizontal, estar en fila 2 y ser contiguo
    if any(r != 2 for r, c in a_pos) or len(a_rows) != 1 or a_cols != set(range(min(a_cols), min(a_cols) + len(a_pos))):
        return 4 if all(r != 2 for r, _ in a_pos) else 5

    # Validación del resto de vehículos
    for vehiculo_id, pos in posiciones.items():
        if vehiculo_id == 'o':
            continue

        tamano = len(pos)
        rows = {r for r, _ in pos}
        cols = {c for _, c in pos}

        is_horizontal = len(rows) == 1
        is_vertical = len(cols) == 1

        # Tamaño permitido: 2 o 3
        if tamano < 2 or tamano > 3:
            if is_horizontal or is_vertical:
                return 6

        # Debe ser estrictamente horizontal o vertical
        if not is_horizontal and not is_vertical:
            return 7

        # Debe ocupar posiciones contiguas
        if is_horizontal and cols != set(range(min(cols), min(cols) + tamano)):
            return 7
        if is_vertical and rows != set(range(min(rows), min(rows) + tamano)):
            return 7

    return 0

# QUE: Método para hacer cuestiones de nivel y mostrar las respuestas.
# POR QUE: Para implementar la acción 'question' que responde a consultas específicas sobre el estado del tablero.
def question(s, args):
    tablero = def_tablero(s)
    posiciones = vehiculo(tablero)

    # Diccionario de acciones disponibles
    actions = {
        'whereis': lambda: ''.join(f'({r},{c})' for r, c in sorted(posiciones.get(args.whereis, []))),
        'what': lambda: tablero[int(args.what.split(',')[0])][int(args.what.split(',')[1])],
        'size': lambda: len(posiciones.get(args.size, [])),
        'howmany': lambda: len(posiciones),
        'goal': lambda: 'TRUE' if any(r == 2 and c == 5 for r, c in posiciones.get('A', [])) else 'FALSE',
        'move': lambda: apply_moves(s, args.move.split(',')) if args.move else s
    }

    # Ejecuta la acción solicitada
    for arg in actions:
        if getattr(args, arg, False):
            print(actions[arg]())
            break

# QUE: Configura el parser de argumentos y ejecuta la accion correspondiente basada en la linea de comandos.
# POR QUE: Para manejar la entrada desde la linea de comandos de manera estructurada y flexible.
def rushhour():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='action', required=True)

    # Subcomando verify
    verify_parser = subparsers.add_parser('verify')
    verify_parser.add_argument('-s', required=True)

    # Subcomando question
    question_parser = subparsers.add_parser('question')
    question_parser.add_argument('-s', required=True)

    group = question_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--whereis')
    group.add_argument('--what')
    group.add_argument('--size')
    group.add_argument('--howmany', action='store_true')
    group.add_argument('--goal', action='store_true')
    group.add_argument('--move')

    # Subcomando successors
    successors_parser = subparsers.add_parser('successors')
    successors_parser.add_argument('-s', required=True)

    # Subcomando solver
    solve_parser = subparsers.add_parser('solver')
    solve_parser.add_argument('-s', required=True)
    solve_parser.add_argument('--strategy', choices=['BFS', 'DFS', 'UC', 'GBF', 'AStar'], required=True)
    solve_parser.add_argument('--depth', type=int)
    solve_parser.add_argument('--heuristic', type=int, choices=[0,1,2])
    solve_parser.add_argument('--stats', action='store_true')
    solve_parser.add_argument('--graphic', action='store_true',
                              help='Muestra una animación gráfica bonita de la solución (requiere Pygame)')
    args = parser.parse_args()

    # Ejecuta la acción correspondiente
    if args.action == 'verify':
        print(verify(args.s))

    elif args.action == 'question':
        question(args.s, args)

    elif args.action == 'successors':
        for accion, estado, costo in successors(args.s):
            print(f"[{accion},{estado},{costo}]")

    elif args.action == 'solver':
        from solver import buscar

        # Validación de heurística
        if args.strategy in ['GBF', 'AStar'] and args.heuristic is None:
            print("Se requiere --heuristic para estrategias GBF y AStar")
            exit(1)

        profundidad_max = args.depth if args.strategy == 'DFS' else None
        heuristic_type = args.heuristic if args.strategy in ['GBF', 'AStar'] else None

        camino, stats = buscar(args.s, args.strategy, profundidad_max, heuristic_type)

        if camino:

            for nodo in camino:
                print(nodo)

            if args.stats:
                print(stats)

            # Visualización gráfica 
            if args.graphic:
                print("\n=== INICIANDO VISUALIZACIÓN GRÁFICA ===")
                try:
                    # Importamos el módulo solo cuando se necesita (así no falla si Pygame no está instalado)
                    from graphic import visualizar_grafico
                    visualizar_grafico(camino)
                    print("=== VISUALIZACIÓN GRÁFICA FINALIZADA ===")
                except ImportError as e:
                    if 'pygame' in str(e).lower():
                        print("Error: Pygame no está instalado.")
                        print("Instálalo con: pip install pygame")
                        print("Después vuelve a ejecutar el comando con --graphic")
                    else:
                        print(f"Error al cargar graphic.py: {e}")
                        print("Asegúrate de que el archivo 'graphic.py' está en la misma carpeta.")
                except Exception as e:
                    print(f"Error durante la visualización gráfica: {e}")
        else:
            print("Sin solución")
            if args.stats:
                print(stats)

# Punto de entrada del programa
if __name__ == '__main__':
    rushhour()
