import paho.mqtt.client as mqtt
import json
import time
import random

broker = "broker.hivemq.com"
port = 1883
topic = "fleet/telemetry/raw"

client = mqtt.Client()
client.connect(broker, port, 60)
print("✅ Simulator Online. Generating raw sensor data...")

try:
    while True:
        # Generate Fake Telemetry Data
        payload = {
            "vehicle_id": "KL-01-AJ-2000",
            "temp": random.randint(70, 120),
            "speed": random.randint(0, 100),
            "oil_pressure": random.randint(15, 80),
            "rpm": random.randint(1000, 7000),
            "fuel": random.randint(10, 100),
            "battery": round(random.uniform(11.5, 14.5), 1),
            "vibration": round(random.uniform(0.5, 8.5), 1),
            "lat": 9.4500 + random.uniform(-0.01, 0.01),
            "lon": 76.4400 + random.uniform(-0.01, 0.01)
        }
        
        # Publish Raw Data
        client.publish(topic, json.dumps(payload))
        print(f"📡 Sent RAW Data: Temp {payload['temp']}°C | Speed {payload['speed']} km/h | Oil {payload['oil_pressure']} PSI")
        
        time.sleep(2) # Send data every 2 seconds

except KeyboardInterrupt:
    print("\n🛑 Simulator Shutting Down.")