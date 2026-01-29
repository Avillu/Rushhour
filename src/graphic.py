# graphic.py
import pygame
import time

# QUE: Muestra una animación gráfica automática de la solución completa usando Pygame.
# POR QUE: Proporciona una visualización atractiva e interactiva de cómo se resuelve el puzzle paso a paso        

def visualizar_grafico(camino):
    """
    Reproduce la solución completa en una ventana gráfica con animación automática.
    
    Args:
        camino: Lista de objetos Nodo desde el estado inicial hasta la meta (obtenida de solver.buscar)
    """
    if not camino:
        print("No hay solución para mostrar gráficamente.")
        return

    # Mensajes de depuración para confirmar que Pygame se inicia correctamente
    print("Inicializando Pygame...")
    pygame.init()
    print("Pygame inicializado.")

    # Configuración de la ventana
    CELL_SIZE = 100                  # Tamaño de cada casilla en píxeles
    MARGIN = 50                      # Margen alrededor del tablero
    WIDTH = HEIGHT = 6 * CELL_SIZE + 2 * MARGIN  # Dimensiones totales de la ventana
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rush Hour - Animación de Solución")
    clock = pygame.time.Clock()      # Control de frames por segundo

    # Fuentes para texto
    font = pygame.font.SysFont(None, 40)      # Fuente normal para información de paso
    big_font = pygame.font.SysFont(None, 60)  # Fuente grande para mensaje de victoria

    # Paleta de colores para los vehículos (cíclica para más de 8 vehículos)
    COLORES = [
        (255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100),
        (255, 100, 255), (100, 255, 255), (255, 200, 100), (200, 100, 255)
    ]
    color_map = {}   # Diccionario para asignar un color único a cada vehículo la primera vez que aparece
    color_idx = 0    # Índice para recorrer la paleta

    paso = 0                         # Paso actual de la animación
    total = len(camino) - 1           # Número total de pasos (excluyendo el inicial)
    running = True                   # Control del bucle principal

    print(f"Reproduciendo {total + 1} pasos...")

    # Bucle principal de la animación
    while running and paso <= total:
        # Gestión de eventos (cerrar ventana o pulsar tecla)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
                    running = False  # Permite salir prematuramente con Escape o Espacio

        # Obtener el estado actual
        nodo = camino[paso]
        cadena = nodo.estado.cadena

        # Fondo de la ventana
        screen.fill((30, 30, 60))  # Color azul oscuro elegante

        # Dibujar la cuadrícula del tablero
        for i in range(7):
            pygame.draw.line(screen, (120, 120, 140),
                             (MARGIN + i * CELL_SIZE, MARGIN),
                             (MARGIN + i * CELL_SIZE, HEIGHT - MARGIN), 4)
            pygame.draw.line(screen, (120, 120, 140),
                             (MARGIN, MARGIN + i * CELL_SIZE),
                             (WIDTH - MARGIN, MARGIN + i * CELL_SIZE), 4)

        # Marcar la salida (casilla fila 2, columna 5) con un rectángulo rojo sólido
        pygame.draw.rect(screen, (255, 50, 50),
                         (MARGIN + 5 * CELL_SIZE, MARGIN + 2 * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)

        # Dibujar todos los vehículos del estado actual
        color_idx = 0
        for r in range(6):
            for c in range(6):
                ch = cadena[r * 6 + c]
                if ch == 'o':  # Casilla vacía
                    continue

                # Asignar color único la primera vez que se ve el vehículo
                if ch not in color_map:
                    if ch == 'A':
                        color_map[ch] = (220, 20, 20)  # Rojo intenso para el coche objetivo
                    else:
                        color_map[ch] = COLORES[color_idx % len(COLORES)]
                        color_idx += 1

                color = color_map[ch]
                x = MARGIN + c * CELL_SIZE
                y = MARGIN + r * CELL_SIZE

                # Dibujar el bloque del vehículo con bordes redondeados
                pygame.draw.rect(screen, color,
                                 (x + 10, y + 10, CELL_SIZE - 20, CELL_SIZE - 20),
                                 border_radius=15)

                # Dibujar la letra del vehículo en el centro
                text = font.render(ch, True, (255, 255, 255))
                screen.blit(text, text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2)))

        # Información del paso actual
        paso_text = font.render(f"Paso {paso}/{total} - {nodo.accion}", True, (255, 255, 200))
        screen.blit(paso_text, (MARGIN, 20))

        # Mensaje de victoria al llegar al último paso
        if paso == total:
            win_text = big_font.render("¡RESUELTO!", True, (0, 255, 0))
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 50))

        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(30)  # Limitar a 30 FPS para suavidad

        # Pausa entre pasos para que la animación sea visible
        time.sleep(1.0)

        # Avanzar al siguiente paso
        paso += 1

    # Después de la animación, esperar a que el usuario cierre la ventana
    print("Esperando a que cierres la ventana...")
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

    pygame.quit()
    print("Ventana cerrada.")