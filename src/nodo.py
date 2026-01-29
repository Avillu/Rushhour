# nodo.py

# QUE: Representa un nodo en el árbol de búsqueda 
# POR QUE: Almacena el historial (padre, acción), el costo y el valor para la búsqueda.
class Nodo:
    # Contador global para asignar IDs únicos a cada nodo
    contador_id = 0

    def __init__(self, estado, padre=None, accion='___', costo=0, profundidad=0, heuristica=0, valor=0):
        # Identificador único del nodo (utilizado para desempate en la frontera)
        self.id = Nodo.contador_id
        Nodo.contador_id += 1
        
        # Estado del problema asociado al nodo
        self.estado = estado
        
        # Nodo padre desde el que se genera este nodo
        self.padre = padre
        
        # Acción aplicada para llegar a este estado
        self.accion = accion
        
        # Costo acumulado desde la raíz
        self.costo = costo 
        
        # Profundidad del nodo en el árbol de búsqueda
        self.profundidad = profundidad
        
        # Valor heurístico del estado
        self.heuristic = heuristica
        
        # Valor utilizado para ordenar en la frontera
        self.valor = valor

    # QUE: Reconstruye la secuencia de nodos desde la raíz hasta el nodo actual.
    # POR QUE: Permite mostrar la solución encontrada.
    def camino(self):
        camino = []
        actual = self
        
        # Recorre los padres hasta llegar a la raíz
        while actual:
            camino.append(actual)
            actual = actual.padre
        
        # Se invierte para obtener el camino raíz → solución
        camino.reverse()
        return camino

    # QUE: Formato de impresión del nodo [id, padre_id, accion, estado, costo, profundidad, heuristica, valor].
    # POR QUE: Para una salida estándar de la solución.
    def __str__(self):
        padre_id = self.padre.id if self.padre else 'none'
        return f"[{self.id},{padre_id},{self.accion},{self.estado},{self.costo},{self.profundidad},{self.heuristic},{self.valor}]"
