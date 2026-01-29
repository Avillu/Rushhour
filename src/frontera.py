# frontera.py 
import heapq

# QUE: Estructura de datos que gestiona los nodos a expandir (cola de prioridad unificada).
# POR QUE: Implementa la lógica de orden por valor e ID para todas las estrategias.
class Frontera:
    def __init__(self, estrategia="BFS"):
        # Lista que actúa como heap de prioridad
        self.items = []
        
        # Estrategia usada (informativa, el orden real depende de nodo.valor)
        self.estrategia = estrategia

    # QUE: Añade un nodo a la frontera con inserción ordenada.
    # POR QUE: Mantiene el orden por valor (primero) e ID (desempate) sin reordenar todo.
    def insertar(self, nodo):
        # heapq mantiene siempre el elemento mínimo en la raíz
        heapq.heappush(self.items, (nodo.valor, nodo.id, nodo))

    # QUE: Obtiene y elimina el siguiente nodo a expandir (menor valor, menor ID).
    # POR QUE: Es la operación central del bucle de búsqueda.
    def extraer(self):
        # Si la frontera está vacía no se puede extraer ningún nodo
        if not self.items:
            return None
        
        # Devuelve solo el nodo, ignorando valor e id
        return heapq.heappop(self.items)[2]

    # QUE: Verifica si no quedan nodos pendientes de expansión.
    # POR QUE: Condición de terminación cuando no se encuentra solución.
    def vacia(self):
        return len(self.items) == 0
