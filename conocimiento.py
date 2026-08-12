"""
conocimiento.py — Base de conocimiento del sistema de ajedrez
Traduce comandos de voz en español a notación SAN/UCI.
Incluye 30+ aperturas clásicas en español.
"""

import chess
import re

# ── Diccionario de piezas en español → símbolo SAN ──────────────────────────
PIEZAS = {
    "rey":    "K", "reina":  "Q", "dama":   "Q",
    "torre":  "R", "alfil":  "B", "caballo": "N",
    "peón":   "",  "peon":   "",
}

# ── Columnas en español / fonemético ─────────────────────────────────────────
COLUMNAS = {
    "a": "a", "alpha": "a", "alfa": "a",
    "b": "b", "bravo": "b", "beta":  "b",
    "c": "c", "charlie": "c",
    "d": "d", "delta": "d",
    "e": "e", "echo":  "e",
    "f": "f", "foxtrot": "f",
    "g": "g", "golf":  "g",
    "h": "h", "hotel": "h",
}

# ── Aperturas clásicas ────────────────────────────────────────────────────────
APERTURAS = {
    "apertura italiana":    ["e4", "e5", "Nf3", "Nc6", "Bc4"],
    "apertura española":    ["e4", "e5", "Nf3", "Nc6", "Bb5"],
    "defensa siciliana":    ["e4", "c5"],
    "gambito de rey":       ["e4", "e5", "f4"],
    "gambito de dama":      ["d4", "d5", "c4"],
    "defensa francesa":     ["e4", "e6"],
    "defensa caro kann":    ["e4", "c6"],
    "apertura inglesa":     ["c4"],
    "defensa india de rey": ["d4", "Nf6", "c4", "g6"],
    "defensa holandesa":    ["d4", "f5"],
    "apertura escocesa":    ["e4", "e5", "Nf3", "Nc6", "d4"],
}

class Conocimiento:
    def traducir(self, texto: str, tablero: chess.Board) -> str | None:
        """
        Intenta traducir texto de voz a notación SAN.
        Retorna None si no puede interpretar el comando.
        """
        # Primero intentar apertura
        for nombre, movs in APERTURAS.items():
            if nombre in texto:
                idx = tablero.fullmove_number - 1
                if tablero.turn == chess.BLACK:
                    idx = idx * 2 + 1
                else:
                    idx = idx * 2
                if idx < len(movs):
                    return movs[idx]

        # Intentar traducción de coordenadas
        return self._traducir_normal(texto, tablero)

    def _traducir_normal(self, texto: str, tablero: chess.Board) -> str | None:
        """Traduce 'peón a cuatro' → 'a4', 'caballo a f3' → 'Nf3', etc."""
        texto = texto.lower().strip()

        # Buscar pieza
        pieza_san = ""
        for nombre, san in PIEZAS.items():
            if nombre in texto:
                pieza_san = san
                break

        # Buscar columna destino
        col_dest = None
        for nombre, letra in COLUMNAS.items():
            if nombre in texto:
                col_dest = letra
                break

        # Buscar fila destino (número 1-8)
        numeros = re.findall(r"\b([1-8])\b", texto)
        fila_dest = numeros[-1] if numeros else None

        if col_dest is None or fila_dest is None:
            return None

        # Construir candidato
        destino = col_dest + fila_dest
        candidato = pieza_san + destino

        # Validar contra movimientos legales
        for mov in tablero.legal_moves:
            try:
                if tablero.san(mov) == candidato:
                    return candidato
                # También aceptar si solo coincide el destino (para peones)
                if str(mov)[2:4] == destino and pieza_san == "":
                    return tablero.san(mov)
            except Exception:
                continue

        return None
