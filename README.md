# 🏠 GharAI: Smart Home Automation with an Adaptive Security Framework

**GharAI** is a next-generation smart home automation and analytics system that integrates **Voice Control (via ZYAA)**, **Machine Learning**, and **IoT** to automate, optimize, and secure home environments intelligently.  

It enables users to control appliances through natural voice commands, predicts energy consumption trends, and provides adaptive security responses through its intelligent assistant — **ZYAA**.

---

## ⚙️ Key Features

- 🎙️ **Voice Assistant — ZYAA**  
  GharAI’s personal AI assistant **ZYAA** allows hands-free control of home appliances using natural voice commands.  
  Example commands:  
  - “Hey ZYAA, turn on the light.”  
  - “ZYAA, switch off the fan.”  
  - “ZYAA, predict current usage.”  

- 🤖 **Machine Learning Integration**  
  Uses trained ML models (`.pkl` files) for energy analytics and appliance behavior prediction.

- ⚡ **Energy Usage Prediction**  
  - `Appliance_Usage_Prediction_Model.pkl` → predicts ON/OFF patterns  
  - `Current_Prediction_Model.pkl` → estimates power/current draw

- 🔒 **Adaptive Security Framework**  
  Detects unusual activity (like irregular power spikes or device misuse) and notifies the user via voice alerts.

- 💡 **Smart Recommendations**  
  Suggests efficient energy patterns and schedules to reduce wastage.

- 📊 **Real-Time Monitoring**  
  Displays live appliance status and energy data through a web interface.

- 💻 **User Interface (UI)**  
  Built using **HTML + CSS + JavaScript** with Python backend (Flask/Tkinter).

- ☁️ **IoT Integration (ESP8266 Ready)**  
  Future-ready framework for cloud connectivity and real-time remote control.

---

## 🧩 Components Used

| Category | Components |
|-----------|-------------|
| **Controller** | ESP8266|
| **Appliances** | Light, Fan|
| **Sensors (optional)** | ACS712 (Current), Tempreature and Humidity Sensor (DHT11), Relay Module |
| **ML Models** | Appliance_Usage_Prediction_Model.pkl, Current_Prediction_Model.pkl |
| **Software / Libraries** | Python, scikit-learn, pandas, numpy, pyttsx3, speechrecognition |
| **Voice Assistant** | **ZYAA** An integrated voice AI for control and feedback |
| **Frontend** | HTML, CSS, JS (`Manash.html`) |

---

## 🧠 Machine Learning Workflow

1. **Data Collection:** Energy usage data collected and stored in `GharAI_dataset.csv`  
2. **Preprocessing:** Cleaning, scaling, and feature extraction  
3. **Training:**  
   - `Appliance_Usage_Prediction_Model.pkl` → learns ON/OFF appliance behavior  
   - `Current_Prediction_Model.pkl` → predicts power/current usage  
4. **Inference:**  
   Models loaded in Python (`ZYAA.py`) for real-time prediction  
5. **Control:**  
   Voice command from **ZYAA** triggers corresponding appliance state and updates dashboard

---

## 🗂️ Project Structure

GharAI/
│
├── GharAI_dataset.csv
├── Appliance_Usage_Prediction_Model.pkl
├── Current_Prediction_Model.pkl
├── Manash.py # Main backend logic
├── ZYAA.py # Voice assistant (ZYAA)
├── Manash.html # Dashboard UI
├── main # Executable placeholder
└── .venv/ # Virtual environment folder

## 🚀 How to Run the Project

### 🟦1️⃣ Install Dependencies***
```bash
pip install pandas numpy scikit-learn pyttsx3 speechrecognition flask

###🟩 2️⃣ Run the Main Script***
python Manash.py

###🟨3️⃣ Activate Voice Assistant (ZYAA)***
python ZYAA.py

Once ZYAA is active, say:

“Turn on the light”

“Switch off the fan”

“Show current usage”

“Predict appliance consumption”

###🟨System Architecture***
[User Voice] 
   ↓
[ZYAA Voice Assistant]
   ↓
[Speech Recognition → Python Logic]
   ↓
[ML Model Prediction]
   ↓
[Appliance Control + Web Dashboard]

###🟩 Project Members***

Manash Jyoti Mahanta

Ashraful Hoque Barbhuiya

Dhitiman Das

Jyotishman Kalita


###🟩 Future Enhancements***

🔌 IoT control using ESP8266 and cloud connectivity

📱 Mobile app integration for remote monitoring

🌐 Cloud-based energy usage analytics

🔒 Smart intrusion/security detection through ZYAA’s adaptive AI

🧠 Integration with GRIHAI (Energy optimization & analytics module)
