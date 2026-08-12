"""
oido.py — Reconocimiento de voz (proceso independiente)
Escucha continuamente y escribe el texto reconocido en jugada.txt.
Se pausa mientras boca.py habla (archivo lock /tmp/hablando.lock).
Soporta también entrada por teclado en paralelo (hilo daemon).
"""

import speech_recognition as sr
import os
import time
import threading

JUGADA_FILE = "/home/mosco/ajedrez/jugada.txt"
JUGADA_TMP  = "/home/mosco/ajedrez/jugada.tmp"
LOCK_FILE   = "/tmp/hablando.lock"

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.6
recognizer.energy_threshold = 300

def escribir_jugada(texto: str):
    """Escritura atómica para evitar condiciones de carrera."""
    with open(JUGADA_TMP, "w") as f:
        f.write(texto)
    os.replace(JUGADA_TMP, JUGADA_FILE)

def hilo_teclado():
    """Lee comandos del teclado como alternativa a la voz."""
    while True:
        try:
            cmd = input()
            if cmd.strip():
                escribir_jugada(cmd.strip().lower())
        except EOFError:
            break

def main():
    # Hilo daemon para entrada por teclado
    t = threading.Thread(target=hilo_teclado, daemon=True)
    t.start()

    with sr.Microphone() as fuente:
        recognizer.adjust_for_ambient_noise(fuente, duration=1)
        print("[oido] Escuchando...")

        while True:
            # Pausar si boca.py está hablando
            if os.path.exists(LOCK_FILE):
                time.sleep(0.1)
                continue

            try:
                audio = recognizer.listen(fuente, timeout=3, phrase_time_limit=5)
                texto = recognizer.recognize_google(audio, language="es-MX")
                texto = texto.strip().lower()
                print(f"[oido] Reconocido: {texto}")
                escribir_jugada(texto)

            except sr.WaitTimeoutError:
                pass  # Silencio normal
            except sr.UnknownValueError:
                pass  # No se entendió
            except sr.RequestError as e:
                print(f"[oido] Error Google API: {e}")
                time.sleep(2)

if __name__ == "__main__":
    main()
