import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import paho.mqtt.client as mqtt
import json

# ==========================================
# 1. FUZZY LOGIC SETUP (TRAPEZOIDAL - 3 VARIABLES)
# ==========================================
temperature = ctrl.Antecedent(np.arange(60, 130, 1), 'temperature')
speed = ctrl.Antecedent(np.arange(0, 130, 1), 'speed')
oil_pressure = ctrl.Antecedent(np.arange(0, 100, 1), 'oil_pressure')
risk_score = ctrl.Consequent(np.arange(0, 100, 1), 'risk_score')

temperature['normal'] = fuzz.trapmf(temperature.universe, [60, 60, 85, 95])
temperature['high'] = fuzz.trapmf(temperature.universe, [85, 95, 105, 115])
temperature['critical'] = fuzz.trapmf(temperature.universe, [105, 115, 130, 130])

speed['slow'] = fuzz.trapmf(speed.universe, [0, 0, 20, 40])
speed['medium'] = fuzz.trapmf(speed.universe, [20, 40, 70, 90])
speed['fast'] = fuzz.trapmf(speed.universe, [70, 90, 130, 130])

oil_pressure['low'] = fuzz.trapmf(oil_pressure.universe, [0, 0, 20, 35])
oil_pressure['normal'] = fuzz.trapmf(oil_pressure.universe, [25, 40, 70, 85])
oil_pressure['high'] = fuzz.trapmf(oil_pressure.universe, [75, 85, 100, 100])

risk_score['safe'] = fuzz.trapmf(risk_score.universe, [0, 0, 30, 45])
risk_score['warning'] = fuzz.trapmf(risk_score.universe, [30, 45, 70, 85])
risk_score['danger'] = fuzz.trapmf(risk_score.universe, [70, 85, 100, 100])

# 27 Logic Combinations condensed into optimized rules
rule1 = ctrl.Rule(oil_pressure['low'], risk_score['danger']) # Loss of oil = Engine Death
rule2 = ctrl.Rule(temperature['critical'] & speed['slow'], risk_score['danger'])
rule3 = ctrl.Rule(temperature['critical'] & speed['fast'], risk_score['warning'])
rule4 = ctrl.Rule(temperature['high'] & speed['slow'] & oil_pressure['normal'], risk_score['warning'])
rule5 = ctrl.Rule(temperature['normal'] & oil_pressure['normal'], risk_score['safe'])

engine_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
engine_sim = ctrl.ControlSystemSimulation(engine_ctrl)

# ==========================================
# 2. MQTT IoT ROUTING
# ==========================================
broker = "broker.hivemq.com"
port = 1883
raw_topic = "fleet/telemetry/raw"
pro_topic = "fleet/telemetry/pro"

def on_connect(client, userdata, flags, rc):
    print("✅ Cloud AI Engine Online. Listening for raw sensor data...")
    client.subscribe(raw_topic)

def on_message(client, userdata, msg):
    try:
        # 1. Receive Raw Data from Simulator
        packet = json.loads(msg.payload.decode())
        
        # 2. Feed data to Fuzzy Logic Brain
        engine_sim.input['temperature'] = packet['temp']
        engine_sim.input['speed'] = packet['speed']
        engine_sim.input['oil_pressure'] = packet['oil_pressure']
        engine_sim.compute()
        
        calc_risk = round(engine_sim.output['risk_score'], 1)
        
        # 3. Determine Status Label
        status = "STABLE"
        if calc_risk >= 75:
            status = "CRITICAL"
        elif calc_risk >= 45:
            status = "WARNING"
            
        # 4. Add AI logic back into the payload
        packet['risk_score'] = calc_risk
        packet['engine_status'] = status
        
        # 5. Forward Processed Data to HTML Dashboard
        client.publish(pro_topic, json.dumps(packet))
        print(f"🧠 Processed & Sent: Risk {calc_risk}% | Status: {status}")
        
    except Exception as e:
        print("⚠️ Error processing fuzzy logic:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)
client.loop_forever() # Keep listening continuously