"""
crear_audios.py — Genera los MP3 de respaldo para modo offline.
Ejecutar una sola vez con conexión a internet:
    python3 crear_audios.py
"""

from gtts import gTTS
import os

AUDIO_DIR = "/home/mosco/ajedrez/audios"
os.makedirs(AUDIO_DIR, exist_ok=True)

FRASES = {
    "bienvenido":   "Bienvenido al ajedrez inteligente.",
    "turno":        "Es tu turno. Di tu jugada.",
    "jugada":       "Jugada realizada.",
    "ilegal":       "Movimiento ilegal. Intenta de nuevo.",
    "jaque_mate":   "¡Jaque mate!",
    "tablas":       "Tablas. Empate.",
    "pensando":     "Pensando...",
    "apagando":     "Apagando el sistema. Hasta pronto.",
    "gracias":      "Gracias por jugar.",
    "turno_blancas":"Turno de blancas.",
    "turno_negras": "Turno de negras.",
    "nivel":        "Nivel de dificultad ajustado.",
    "victoria":     "¡Felicidades! Ganaste.",
    "derrota":      "La máquina ganó. ¡Sigue practicando!",
    "modo_1p":      "Modo un jugador activado. Juegas con las piezas blancas.",
    "modo_2p":      "Modo dos jugadores activado.",
}

print("Generando archivos de audio offline...")
for nombre, texto in FRASES.items():
    ruta = os.path.join(AUDIO_DIR, f"{nombre}.mp3")
    gTTS(text=texto, lang="es", tld="com.mx").save(ruta)
    print(f"  ✓ {nombre}.mp3")

print(f"\n{len(FRASES)} archivos generados en {AUDIO_DIR}")
