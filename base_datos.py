"""
base_datos.py — Persistencia SQLite
Gestiona perfiles de jugadores, ranking, victorias y nivel adaptativo.
"""

import sqlite3
import os
from datetime import datetime

class BaseDatos:
    def __init__(self, ruta: str):
        self.ruta = ruta
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        self._crear_tablas()

    def _conectar(self):
        return sqlite3.connect(self.ruta)

    def _crear_tablas(self):
        with self._conectar() as con:
            con.executescript("""
                CREATE TABLE IF NOT EXISTS configuracion (
                    clave TEXT PRIMARY KEY,
                    valor TEXT
                );

                CREATE TABLE IF NOT EXISTS partidas (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha      TEXT,
                    resultado  TEXT,
                    nivel      INTEGER,
                    movimientos INTEGER
                );

                CREATE TABLE IF NOT EXISTS ranking (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre     TEXT,
                    victorias  INTEGER DEFAULT 0,
                    derrotas   INTEGER DEFAULT 0,
                    empates    INTEGER DEFAULT 0
                );

                INSERT OR IGNORE INTO configuracion VALUES ('nivel', '5');
            """)

    def obtener_nivel(self) -> int:
        with self._conectar() as con:
            cur = con.execute("SELECT valor FROM configuracion WHERE clave='nivel'")
            row = cur.fetchone()
            return int(row[0]) if row else 5

    def subir_nivel(self):
        nivel = min(self.obtener_nivel() + 1, 20)
        with self._conectar() as con:
            con.execute("UPDATE configuracion SET valor=? WHERE clave='nivel'", (str(nivel),))

    def bajar_nivel(self):
        nivel = max(self.obtener_nivel() - 1, 1)
        with self._conectar() as con:
            con.execute("UPDATE configuracion SET valor=? WHERE clave='nivel'", (str(nivel),))

    def guardar_partida(self, resultado: str, nivel: int, movimientos: int = 0):
        with self._conectar() as con:
            con.execute(
                "INSERT INTO partidas (fecha, resultado, nivel, movimientos) VALUES (?,?,?,?)",
                (datetime.now().isoformat(), resultado, nivel, movimientos)
            )

    def obtener_historial(self, limite: int = 10):
        with self._conectar() as con:
            cur = con.execute(
                "SELECT fecha, resultado, nivel FROM partidas ORDER BY id DESC LIMIT ?",
                (limite,)
            )
            return cur.fetchall()

    def estadisticas(self):
        with self._conectar() as con:
            cur = con.execute("""
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN resultado='1-0' THEN 1 ELSE 0 END) as victorias,
                    SUM(CASE WHEN resultado='0-1' THEN 1 ELSE 0 END) as derrotas,
                    SUM(CASE WHEN resultado='1/2-1/2' THEN 1 ELSE 0 END) as empates
                FROM partidas
            """)
            return cur.fetchone()
