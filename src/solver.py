# solver.py
import time
from nodo import Nodo
from frontera import Frontera
from estado import Estado

# QUE: Clase auxiliar para recopilar y mostrar estadísticas del proceso de búsqueda.
# POR QUE: Permite medir el rendimiento del algoritmo.
class Estadisticas:
    def __init__(self):
        # Tiempo total de ejecución (microsegundos)
        self.tiempo = 0
        
        # TN: Total de nodos generados
        self.tn = 0
        
        # EN: Total de nodos expandidos
        self.en = 0
        
        # CN: Total de nodos podados/descartados
        self.cn = 0
        
        # DF: Profundidad máxima alcanzada
        self.df = 0

    # Incrementa el contador de nodos generados
    def generar(self):
        self.tn += 1
    
    # Incrementa el contador de nodos expandidos
    def expandir(self):
        self.en += 1
    
    # Incrementa el contador de nodos descartados
    def podar(self):
        self.cn += 1

    # Representación textual de las estadísticas
    def __str__(self):
        return f"ET: {self.tiempo}\nTN: {self.tn}\nEN: {self.en}\nCN: {self.cn}\nDF: {self.df}"

# QUE: Función principal que ejecuta la búsqueda en espacio de estados según la estrategia indicada.
# POR QUE: Es el núcleo del solucionador del puzzle Rush Hour.
def buscar(inicio_cadena, estrategia, profundidad_max=None, heuristic_type=None):
    # Crea el estado inicial a partir de la cadena
    inicio = Estado(inicio_cadena)

    # Caso especial: el estado inicial ya es meta
    if inicio.es_meta():
        raiz = Nodo(inicio)
        stats = Estadisticas()
        stats.generar()
        stats.df = 0
        return raiz.camino(), stats

    # Cálculo inicial de heurística si la estrategia lo requiere
    h_inicial = 0
    if estrategia in ["GBF", "AStar"]:
        h_inicial = inicio.heuristica(heuristic_type)

    # Valor inicial del nodo según la estrategia
    valor_inicial = h_inicial

    # Nodo raíz del árbol de búsqueda
    raiz = Nodo(
        inicio,
        profundidad=0,
        heuristica=h_inicial,
        valor=valor_inicial
    )

    # Inicializa la frontera (cola de prioridad)
    frontera = Frontera(estrategia)
    frontera.insertar(raiz)

    # Conjunto de estados visitados (para BFS, UC, GBF, A*)
    visitados = set()
    
    # Diccionario de mejor profundidad alcanzada por estado (usado en DFS)
    mejor_profundidad = {}

    # Inicializa estadísticas
    stats = Estadisticas()
    stats.generar()

    # Marca el inicio del tiempo de ejecución
    t0 = time.perf_counter_ns()

    # Bucle principal de búsqueda
    while not frontera.vacia():
        # Extrae el siguiente nodo según la estrategia
        actual = frontera.extraer()

        # Comprueba si se ha alcanzado la meta
        if actual.estado.es_meta():
            t1 = time.perf_counter_ns()
            stats.tiempo = (t1 - t0) // 1000
            stats.df = max(stats.df, actual.profundidad)
            return actual.camino(), stats

        # Clave única del estado (cadena del tablero)
        clave = actual.estado.cadena

        # Gestión de estados repetidos
        if estrategia == "DFS":
            # En DFS se permite revisitar estados si se alcanza menor profundidad
            if clave in mejor_profundidad and mejor_profundidad[clave] <= actual.profundidad:
                stats.podar()
                continue
            mejor_profundidad[clave] = actual.profundidad
        else:
            # En el resto de estrategias no se permiten estados repetidos
            if clave in visitados:
                stats.podar()
                continue
            visitados.add(clave)

        # Comprobación del límite de profundidad (solo relevante para DFS)
        if profundidad_max is not None and actual.profundidad >= profundidad_max:
            stats.podar()
            continue

        # Marca el nodo como expandido
        stats.expandir()
        stats.df = max(stats.df, actual.profundidad)

        # Genera los sucesores del estado actual
        for accion, nueva_cadena, coste_accion in actual.estado.successors():
            nueva_prof = actual.profundidad + 1

            # Poda por límite de profundidad
            if profundidad_max is not None and nueva_prof > profundidad_max:
                stats.podar()
                continue

            # Cálculo de heurística del sucesor si procede
            h = 0
            if estrategia in ["GBF", "AStar"]:
                nuevo_estado_temp = Estado(nueva_cadena)
                h = nuevo_estado_temp.heuristica(heuristic_type)

            # Cálculo del valor según la estrategia seleccionada
            if estrategia == "DFS":
                valor = -nueva_prof
            elif estrategia == "BFS":
                valor = nueva_prof
            elif estrategia == "UC":
                valor = actual.costo + coste_accion
            elif estrategia == "GBF":
                valor = h
            elif estrategia == "AStar":
                valor = actual.costo + coste_accion + h

            # Crea el nuevo estado y nodo hijo
            nuevo_estado = Estado(nueva_cadena)

            hijo = Nodo(
                estado=nuevo_estado,
                padre=actual,
                accion=accion,
                costo=actual.costo + coste_accion,
                profundidad=nueva_prof,
                heuristica=h,
                valor=valor
            )

            # Actualiza estadísticas y añade a la frontera
            stats.generar()
            stats.df = max(stats.df, nueva_prof)
            frontera.insertar(hijo)

    # Si no se encuentra solución
    t1 = time.perf_counter_ns()
    stats.tiempo = (t1 - t0) // 1000
    return None, stats
