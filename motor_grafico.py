"""
motor_grafico.py — Renderizado en matriz LED RGB 64×64
Dibuja el tablero de ajedrez y las piezas en la pantalla LED via GPIO (HUB75).
"""

import chess
import time

# Colores del tablero
COLOR_CASILLA_CLARA = (200, 200, 200)
COLOR_CASILLA_OSCURA = (50, 50, 50)
COLOR_BLANCAS        = (255, 200, 0)    # Amarillo
COLOR_NEGRAS         = (0, 255, 200)    # Cian
COLOR_SELECCION      = (255, 100, 0)    # Naranja
COLOR_BORDE_ROJO     = (255, 0, 0)

# Tamaño de cada casilla en la matriz 64x64 (8 casillas × 8 píxeles)
TAMANO_CASILLA = 8

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    from PIL import Image, ImageDraw

    class MotorGrafico:
        def __init__(self):
            options = RGBMatrixOptions()
            options.rows = 64
            options.cols = 64
            options.chain_length = 1
            options.parallel = 1
            options.hardware_mapping = "regular"
            options.gpio_slowdown = 2
            self.matrix = RGBMatrix(options=options)
            self.image = Image.new("RGB", (64, 64))
            self.draw = ImageDraw.Draw(self.image)

        def dibujar(self, tablero: chess.Board):
            """Renderiza el estado completo del tablero en la matriz LED."""
            self.image = Image.new("RGB", (64, 64))
            self.draw = ImageDraw.Draw(self.image)

            for fila in range(8):
                for col in range(8):
                    casilla = chess.square(col, 7 - fila)
                    x = col * TAMANO_CASILLA
                    y = fila * TAMANO_CASILLA

                    # Color base de la casilla
                    if (fila + col) % 2 == 0:
                        color_fondo = COLOR_CASILLA_CLARA
                    else:
                        color_fondo = COLOR_CASILLA_OSCURA

                    self.draw.rectangle(
                        [x, y, x + TAMANO_CASILLA - 1, y + TAMANO_CASILLA - 1],
                        fill=color_fondo
                    )

                    # Dibujar pieza si existe
                    pieza = tablero.piece_at(casilla)
                    if pieza:
                        color_pieza = COLOR_BLANCAS if pieza.color == chess.WHITE else COLOR_NEGRAS
                        # Dibujar punto central representando la pieza
                        cx = x + TAMANO_CASILLA // 2
                        cy = y + TAMANO_CASILLA // 2
                        self.draw.ellipse(
                            [cx - 2, cy - 2, cx + 2, cy + 2],
                            fill=color_pieza
                        )

            self.matrix.SetImage(self.image)

        def borde_rojo(self):
            """Muestra un borde rojo brevemente para indicar movimiento ilegal."""
            img_error = self.image.copy()
            draw_e = ImageDraw.Draw(img_error)
            draw_e.rectangle([0, 0, 63, 63], outline=COLOR_BORDE_ROJO, width=2)
            self.matrix.SetImage(img_error)
            time.sleep(0.5)
            self.matrix.SetImage(self.image)

        def apagar(self):
            """Apaga todos los LEDs."""
            self.matrix.Clear()

except ImportError:
    # Modo simulación (sin hardware)
    print("[motor_grafico] Modo simulación — rgbmatrix no disponible")

    class MotorGrafico:
        def dibujar(self, tablero):
            print(tablero)

        def borde_rojo(self):
            print("[motor_grafico] ¡Movimiento ilegal!")

        def apagar(self):
            print("[motor_grafico] Apagado.")
