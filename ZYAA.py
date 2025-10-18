from flask import Flask, render_template, request, redirect
from ZYAA import speak
import requests
import random

app = Flask(__name__)

# Initial mock values
fan_status = "OFF"
appliance_type = 0  # 0 = Fan, 1 = Light (you can toggle this if needed)

def get_temperature():
    return random.randint(24, 32)

def get_ai_suggestion(temp, fan_status):
    if temp > 30 and fan_status == "OFF":
        return "It’s hot! You should turn on the fan."
    elif temp < 26 and fan_status == "ON":
        return "It’s cool already! Consider turning off the fan."
    else:
        return "Temperature is optimal. No action needed."

# ML Prediction using Manash2.py server
def get_predictions(hours_used, day_of_week, room_temp, appliance_type):
    features = [hours_used, day_of_week, room_temp, appliance_type]

    try:
        # Call current prediction
        current_res = requests.post("http://127.0.0.1:5000/predict/current", json={"features": features})
        predicted_current = current_res.json().get("predicted_current", None)

        # Call appliance usage prediction
        usage_res = requests.post("http://127.0.0.1:5000/predict/appliance", json={"features": features})
        predicted_usage = usage_res.json().get("predicted_appliance_usage", None)

        return round(predicted_current, 3), predicted_usage

    except Exception as e:
        print(f"[ERROR] ML Prediction failed: {e}")
        return None, None

@app.route('/')
def home():
    temp = get_temperature()
    suggestion = get_ai_suggestion(temp, fan_status)

    # Example random input for ML model
    hours_used = random.randint(1, 12)
    day_of_week = random.randint(0, 6)
    room_temp = float(temp)

    # Call prediction
    predicted_current, predicted_usage = get_predictions(hours_used, day_of_week, room_temp, appliance_type)

    data = {
        'temperature': temp,
        'fan_status': fan_status,
        'suggestion': suggestion,
        'predicted_current': predicted_current,
        'predicted_usage': predicted_usage
    }

    return render_template('Manash.html', data=data)

@app.route('/control', methods=['POST'])
def control():
    global fan_status

    action = request.form['action']

    if action == "turn_on":
        fan_status = "ON"
        speak("Turning on the fan.")
        print("[ACTION] Fan turned ON")

    elif action == "turn_off":
        fan_status = "OFF"
        speak("Turning off the fan.")
        print("[ACTION] Fan turned OFF")

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
