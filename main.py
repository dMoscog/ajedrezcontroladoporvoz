"""
Ajedrez con IA y Control por Voz
main.py — Proceso principal: gestiona el juego, los turnos y la lógica
"""

import chess
import chess.engine
import os
import time
import subprocess
from base_datos import BaseDatos
from conocimiento import Conocimiento
from motor_grafico import MotorGrafico
from boca import Boca

STOCKFISH_PATH = "/usr/games/stockfish"
JUGADA_FILE    = "/home/mosco/ajedrez/jugada.txt"
DB_PATH        = "/home/mosco/ajedrez/ajedrez_inteligente.db"
NIVEL_DEFAULT  = 5

def leer_jugada():
    """Lee el archivo de jugada escrito por oido.py y lo limpia."""
    try:
        with open(JUGADA_FILE, "r") as f:
            texto = f.read().strip().lower()
        if texto:
            with open(JUGADA_FILE, "w") as f:
                f.write("")
        return texto
    except FileNotFoundError:
        return ""

def seleccionar_modo(boca: Boca) -> str:
    """Pregunta por voz si es modo 1 jugador o 2 jugadores."""
    boca.decir("Bienvenido al ajedrez inteligente. ¿Quieres jugar contra la máquina o en modo dos jugadores?")
    time.sleep(1)
    for _ in range(10):
        cmd = leer_jugada()
        if "dos" in cmd or "2" in cmd or "humano" in cmd:
            boca.decir("Modo dos jugadores activado.")
            return "2p"
        if "maquina" in cmd or "ia" in cmd or "computadora" in cmd or "uno" in cmd or "1" in cmd:
            boca.decir("Modo un jugador activado. Juegas con las piezas blancas.")
            return "1p"
        time.sleep(0.5)
    boca.decir("Iniciando modo un jugador por defecto.")
    return "1p"

def jugada_ia(tablero: chess.Board, engine, nivel: int) -> chess.Move:
    """Calcula el mejor movimiento de Stockfish según el nivel."""
    limite = chess.engine.Limit(depth=nivel)
    resultado = engine.play(tablero, limite)
    return resultado.move

def anunciar_jaque_mate(boca: Boca, tablero: chess.Board):
    if tablero.is_checkmate():
        ganador = "Blancas" if tablero.turn == chess.BLACK else "Negras"
        boca.decir(f"¡Jaque mate! Ganaron las {ganador}.")
    elif tablero.is_stalemate():
        boca.decir("Tablas por ahogado.")
    elif tablero.is_insufficient_material():
        boca.decir("Tablas por material insuficiente.")

def main():
    # Inicialización
    db   = BaseDatos(DB_PATH)
    con  = Conocimiento()
    graf = MotorGrafico()
    boca = Boca()

    # Inicializar archivo de jugada
    with open(JUGADA_FILE, "w") as f:
        f.write("")

    # Proceso de escucha en paralelo
    proceso_oido = subprocess.Popen(
        ["python3", "/home/mosco/ajedrez/oido.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    try:
        # Motor de IA
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

        # Selección de modo
        modo = seleccionar_modo(boca)

        # Perfil / nivel
        nivel = db.obtener_nivel() or NIVEL_DEFAULT
        boca.decir(f"Nivel de dificultad: {nivel}.")

        tablero = chess.Board()
        graf.dibujar(tablero)

        turno_humano = True  # En modo 1p: True = blancas (humano)

        while not tablero.is_game_over():
            if modo == "1p" and not turno_humano:
                # Turno de la IA
                boca.decir("Pensando...")
                mov = jugada_ia(tablero, engine, nivel)
                tablero.push(mov)
                graf.dibujar(tablero)
                boca.decir(f"Máquina juega {mov.uci()}")
                turno_humano = True
                continue

            # Turno humano
            color = "Blancas" if tablero.turn == chess.BLACK is False else "Negras"
            boca.decir(f"Turno de {color}. Di tu jugada.")

            movimiento_hecho = False
            tiempo_espera = 0

            while not movimiento_hecho and tiempo_espera < 60:
                cmd = leer_jugada()

                if cmd:
                    # Intentar traducir voz a movimiento
                    mov_san = con.traducir(cmd, tablero)
                    if mov_san:
                        try:
                            mov = tablero.parse_san(mov_san)
                            tablero.push(mov)
                            graf.dibujar(tablero)
                            boca.decir(f"Jugada: {mov_san}")
                            movimiento_hecho = True
                            if modo == "1p":
                                turno_humano = False
                        except ValueError:
                            boca.decir("Movimiento ilegal. Intenta de nuevo.")
                            graf.borde_rojo()
                    else:
                        boca.decir("No entendí la jugada. Intenta de nuevo.")

                time.sleep(0.3)
                tiempo_espera += 0.3

            if not movimiento_hecho:
                boca.decir("Tiempo agotado. Turno perdido.")
                if modo == "1p":
                    turno_humano = False

        # Fin del juego
        anunciar_jaque_mate(boca, tablero)
        resultado = tablero.result()
        db.guardar_partida(resultado, nivel)

        # Ajuste de nivel adaptativo
        if resultado == "1-0":
            db.subir_nivel()
        elif resultado == "0-1":
            db.bajar_nivel()

        boca.decir("Gracias por jugar.")
        engine.quit()

    except KeyboardInterrupt:
        boca.decir("Apagando el sistema.")
    finally:
        proceso_oido.terminate()
        graf.apagar()

if __name__ == "__main__":
    main()
