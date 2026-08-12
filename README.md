# ♟️ Ajedrez con IA y Control por Voz

Sistema de ajedrez físico controlado completamente por voz, con inteligencia artificial adaptativa, tablero LED de 64×64 píxeles y base de datos de historial de partidas. Desarrollado en Python sobre Raspberry Pi 4.

---

## 🎬 Demo

> Dices **"peón a cuatro"** → el sistema reconoce la voz → valida el movimiento → actualiza el tablero LED → la IA responde.

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                    Raspberry Pi 4                    │
│                                                     │
│  ┌──────────┐    jugada.txt    ┌──────────────────┐ │
│  │ oido.py  │ ──────────────► │    main.py       │ │
│  │ (escucha │                 │ (lógica del      │ │
│  │  voz)    │                 │  juego)          │ │
│  └──────────┘                 │                  │ │
│                               │  ┌─────────────┐ │ │
│  ┌──────────┐   /tmp/lock     │  │ Stockfish   │ │ │
│  │ boca.py  │ ◄─────────────  │  │ (IA)        │ │ │
│  │ (síntesis│                 │  └─────────────┘ │ │
│  │  voz)    │                 └──────────────────┘ │
│  └──────────┘                                      │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │          Matriz LED RGB 64×64 (HUB75)        │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Tecnologías

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3 |
| Hardware | Raspberry Pi 4 (4GB RAM) |
| Pantalla | Matriz LED RGB 64×64 (HUB75) |
| IA de ajedrez | Stockfish (Minimax + Alfa-Beta) |
| Reconocimiento de voz | Google Speech-to-Text API |
| Síntesis de voz | gTTS (online) + MP3 offline |
| Base de datos | SQLite |
| Lógica de ajedrez | python-chess |
| Control GPIO | rpi-rgb-led-matrix |

---

## 📁 Estructura del proyecto

```
ajedrez/
├── main.py           # Proceso principal — flujo del juego
├── oido.py           # Reconocimiento de voz (proceso independiente)
├── boca.py           # Síntesis de voz híbrida (online/offline)
├── motor_grafico.py  # Renderizado en matriz LED 64×64
├── conocimiento.py   # Traducción de voz → SAN + 30 aperturas
├── base_datos.py     # Persistencia SQLite (historial y nivel)
├── crear_audios.py   # Generador de MP3 offline
├── requirements.txt
└── audios/           # MP3 pregrabados para modo offline
```

---

## 🚀 Instalación

### 1. Dependencias del sistema
```bash
sudo apt update
sudo apt install stockfish mpg123 python3-pip
```

### 2. Librería LED (rpi-rgb-led-matrix)
```bash
git clone https://github.com/hzeller/rpi-rgb-led-matrix
cd rpi-rgb-led-matrix
make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)
```

### 3. Permisos GPIO
```bash
sudo chmod 777 /dev/mem
sudo chmod 777 /dev/gpiomem
```

### 4. Dependencias Python
```bash
pip3 install -r requirements.txt
```

### 5. Generar audios offline (una sola vez, con internet)
```bash
python3 crear_audios.py
```

### 6. Ejecutar
```bash
python3 main.py
```

---

## 🎮 Comandos de voz

| Dices | Acción |
|---|---|
| "peón a cuatro" | Mueve peón a a4 |
| "caballo a f tres" | Mueve caballo a Nf3 |
| "torre a uno" | Mueve torre a a1 |
| "apertura italiana" | Ejecuta secuencia de apertura italiana |
| "dos jugadores" | Activa modo 2 jugadores |

---

## ⚙️ Características

- ✅ **Modo 1 jugador** — contra Stockfish con nivel adaptativo (1-20)
- ✅ **Modo 2 jugadores** — dos humanos frente a frente
- ✅ **Anti-eco** — lock file pausa el micrófono mientras el sistema habla
- ✅ **Escritura atómica** — `os.replace()` previene condiciones de carrera
- ✅ **Modo offline** — MP3 pregrabados cuando no hay internet
- ✅ **30+ aperturas** clásicas en español
- ✅ **Historial de partidas** en SQLite
- ✅ **Nivel adaptativo** — sube con victorias, baja con derrotas

---

## 👤 Autor

**David Mosco Gasca** — Ingeniero en Sistemas Computacionales, UNITEC  
jesusmosco12@gmail.com  
linkedin.com/in/david-mosco-gasca

---

## 📄 Licencia

MIT License — libre para usar, modificar y distribuir.
