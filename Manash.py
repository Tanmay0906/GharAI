from flask import Flask, request, jsonify, Response
import joblib
import pickle
import numpy as np
import datetime
import threading
import time
import random
from collections import deque

app = Flask(__name__)

# === Load Models safely ===
def safe_load(path):
    try:
        return joblib.load(path)
    except:
        with open(path, "rb") as f:
            return pickle.load(f, fix_imports=True, encoding="latin1")

current_model = safe_load("Models/Current_Prediction_Model.pkl")
appliance_model = safe_load("Models/Appliance_Usage_Prediction_Model.pkl")
# Check if models are loaded
if current_model is None or appliance_model is None:
    raise RuntimeError("Failed to load one or both models. Please check the model files.")

# === Global States ===
sensor_data = deque(maxlen=200)  # store recent sensor values
appliance_states = {
    "fan": {"on": True, "watt": 75, "runtime": 0},
    "light": {"on": True, "watt": 40, "runtime": 0},
    "ac": {"on": False, "watt": 1500, "runtime": 0},
    "tv": {"on": False, "watt": 120, "runtime": 0},
}

lock = threading.Lock()

# === Background Data Stream (Synthetic for Demo) ===
def _accumulate_appliance_runtime():
    """Increase runtime counter for ON appliances"""
    with lock:
        for name, info in appliance_states.items():
            if info["on"]:
                info["runtime"] += 1  # +1 second runtime

def synthetic_stream():
    while True:
        with lock:
            current = sum(info["watt"] / 230.0 for info in appliance_states.values() if info["on"])
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            sensor_data.append({"time": ts, "current": round(current, 2)})
        _accumulate_appliance_runtime()
        time.sleep(1)

threading.Thread(target=synthetic_stream, daemon=True).start()

# === API Endpoints ===
@app.route("/predict/current", methods=["POST"])
def predict_current():
    data = request.get_json()
    features = data.get("features", [])

    if current_model and len(features) == 4:
        input_array = np.array(features).reshape(1, -1)
        pred = current_model.predict(input_array)[0]
        return jsonify({"predicted_current": float(pred), "status": "success"})
    else:
        return jsonify({"predicted_current": 0.65, "status": "fallback"})

@app.route("/predict/appliance", methods=["POST"])
def predict_appliance():
    data = request.get_json()
    features = data.get("features", [])

    if appliance_model and len(features) == 4:
        input_array = np.array(features).reshape(1, -1)
        pred = appliance_model.predict(input_array)[0]
        return jsonify({"predicted_appliance_usage": float(pred), "status": "success"})
    else:
        return jsonify({"predicted_appliance_usage": 2.5, "status": "fallback"})

@app.route("/api/current")
def api_current():
    with lock:
        return jsonify(sensor_data[-1] if sensor_data else {"time": None, "current": 0})

@app.route("/api/sensor_data")
def api_sensor_data():
    with lock:
        return jsonify(list(sensor_data))

@app.route("/api/anomalies")
def api_anomalies():
    with lock:
        values = [d["current"] for d in sensor_data]
    if len(values) < 10:
        return jsonify([])
    mean = np.mean(values)
    std = np.std(values)
    anomalies = [d for d in sensor_data if abs(d["current"] - mean) > 2 * std]
    return jsonify(anomalies)

@app.route("/update/appliance", methods=["POST"])
def update_appliance():
    data = request.get_json()
    name = data.get("name")
    on = data.get("on")
    watt = data.get("watt")

    with lock:
        if name in appliance_states:
            if on is not None:
                appliance_states[name]["on"] = bool(on)
            if watt is not None:
                appliance_states[name]["watt"] = float(watt)
    return jsonify(appliance_states)

@app.route("/api/energy")
def api_energy():
    with lock:
        breakdown = {
            name: {"runtime_s": info["runtime"], "energy_Wh": (info["runtime"] * info["watt"] / 3600.0)}
            for name, info in appliance_states.items()
        }
    return jsonify(breakdown)

@app.route("/system/status")
def system_status():
    return jsonify({
        "current_model_loaded": current_model is not None,
        "appliance_model_loaded": appliance_model is not None,
        "appliances": appliance_states
    })

@app.route("/dashboard")
def dashboard():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Energy Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h2>Live Current Consumption</h2>
        <canvas id="chart" width="600" height="300"></canvas>
        <script>
        const ctx = document.getElementById('chart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: { labels: [], datasets: [{ label: 'Current (A)', data: [], borderColor: 'blue' }] },
        });
        async function updateChart() {
            let res = await fetch('/api/sensor_data');
            let data = await res.json();
            chart.data.labels = data.map(d => d.time);
            chart.data.datasets[0].data = data.map(d => d.current);
            chart.update();
        }
        setInterval(updateChart, 1000);
        </script>
    </body>
    </html>
    """
    return Response(html, mimetype="text/html")

# === Run Flask Server ===
if __name__ == "__main__":
    print("🚀 Starting Enhanced Flask ML Server on port 5000...")
    print("📊 Available Endpoints:")
    print("   POST /predict/current     - Predict current consumption")
    print("   POST /predict/appliance   - Predict appliance usage")
    print("   GET  /api/current         - Get current sensor value")
    print("   GET  /api/sensor_data     - Get historical sensor data")
    print("   GET  /api/anomalies       - Check for anomalies (z-score)")
    print("   POST /update/appliance    - Update appliance states")
    print("   GET  /api/energy          - Get energy usage breakdown")
    print("   GET  /system/status       - Get system status")
    print("   GET  /dashboard           - Minimal live dashboard (Chart.js)")
    app.run(host="0.0.0.0", port=5000, debug=True)
