"""
FRIDAY AI Assistant — Flask Web Server
Serves the holographic UI and manages real-time WebSocket events.
"""

import psutil
import datetime
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

# Import extended API routes
try:
    from web.api import register_api_routes
except ImportError:
    register_api_routes = None

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = "friday-secret-2024"

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Register extended API routes if available
if register_api_routes:
    register_api_routes(app)

# Will be set by main.py
friday_core = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status")
def status():
    """Return current system status for the UI."""
    cpu     = psutil.cpu_percent(interval=0.5)
    ram     = psutil.virtual_memory().percent
    disk    = psutil.disk_usage("/").percent
    battery = None
    try:
        b = psutil.sensors_battery()
        if b:
            battery = {"percent": b.percent, "plugged": b.power_plugged}
    except Exception:
        pass

    return jsonify({
        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "battery": battery,
        "time": datetime.datetime.now().strftime("%I:%M:%S %p"),
        "date": datetime.datetime.now().strftime("%A, %B %d, %Y"),
    })


@socketio.on("connect")
def on_connect():
    emit("status_update", {"state": "connected", "message": "FRIDAY connected."})


@socketio.on("user_message")
def on_user_message(data):
    """Handle text command from the UI chat box."""
    text = data.get("message", "").strip()
    if not text or not friday_core:
        return

    emit("status_update", {"state": "processing", "message": "Processing..."})
    reply = friday_core.process(text, source="text")
    emit("friday_reply", {"message": reply, "source": "text"})
    emit("status_update", {"state": "idle", "message": "Ready"})


@socketio.on("voice_trigger")
def on_voice_trigger():
    """UI button pressed — start listening."""
    if friday_core:
        emit("status_update", {"state": "listening", "message": "Listening..."})
        text = friday_core.voice.listen_once(timeout=8)
        if text:
            emit("user_message_echo", {"message": text})
            emit("status_update", {"state": "processing", "message": "Processing..."})
            reply = friday_core.process(text, source="voice")
            emit("friday_reply", {"message": reply, "source": "voice"})
        else:
            emit("friday_reply", {"message": "I didn't catch that. Could you repeat?", "source": "voice"})
        emit("status_update", {"state": "idle", "message": "Ready"})


@socketio.on("clear_memory")
def on_clear_memory():
    if friday_core:
        reply = friday_core.brain.clear_memory()
        emit("friday_reply", {"message": reply, "source": "system"})


def broadcast_voice_state(state: str, message: str):
    """Called from main thread to push voice state to UI."""
    socketio.emit("status_update", {"state": state, "message": message})


def broadcast_message(role: str, text: str):
    """Push a message to all connected UI clients."""
    if role == "user":
        socketio.emit("user_message_echo", {"message": text})
    else:
        socketio.emit("friday_reply", {"message": text, "source": "voice"})
