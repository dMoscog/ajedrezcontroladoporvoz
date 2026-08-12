"""
boca.py — Síntesis de voz híbrida
Intenta gTTS online; si falla, usa MP3 pregrabados offline.
Usa /tmp/hablando.lock para pausar el micrófono mientras habla (anti-eco).
"""

import os
import socket
import subprocess
import tempfile

LOCK_FILE  = "/tmp/hablando.lock"
AUDIO_DIR  = "/home/mosco/ajedrez/audios"

def _hay_internet() -> bool:
    try:
        socket.setdefaulttimeout(2)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except OSError:
        return False

class Boca:
    def __init__(self):
        self.online = _hay_internet()

    def decir(self, texto: str):
        """Reproduce texto por voz. Lock activo durante la reproducción."""
        # Activar lock anti-eco
        open(LOCK_FILE, "w").close()
        try:
            if self.online:
                self._gtts(texto)
            else:
                self._offline(texto)
        except Exception as e:
            print(f"[boca] Error de audio: {e}")
        finally:
            # Liberar lock
            if os.path.exists(LOCK_FILE):
                os.remove(LOCK_FILE)

    def _gtts(self, texto: str):
        """Síntesis online con Google TTS."""
        from gtts import gTTS
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tmp = f.name
        gTTS(text=texto, lang="es", tld="com.mx").save(tmp)
        subprocess.run(["mpg123", "-q", tmp], check=True)
        os.unlink(tmp)

    def _offline(self, texto: str):
        """Reproduce MP3 pregrabado más cercano al texto."""
        # Mapa simple de frases clave a archivos de audio
        mapa = {
            "bienvenido":  "bienvenido.mp3",
            "turno":       "turno.mp3",
            "jugada":      "jugada.mp3",
            "ilegal":      "ilegal.mp3",
            "jaque mate":  "jaque_mate.mp3",
            "tablas":      "tablas.mp3",
            "pensando":    "pensando.mp3",
            "apagando":    "apagando.mp3",
            "gracias":     "gracias.mp3",
        }
        for clave, archivo in mapa.items():
            if clave in texto.lower():
                ruta = os.path.join(AUDIO_DIR, archivo)
                if os.path.exists(ruta):
                    subprocess.run(["mpg123", "-q", ruta])
                    return
        print(f"[boca-offline] Sin audio para: {texto}")
