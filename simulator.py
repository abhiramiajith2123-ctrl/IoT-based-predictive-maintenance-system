import paho.mqtt.client as mqtt
import json
import time
import random

broker = "broker.hivemq.com"
port = 1883
topic = "fleet/telemetry/raw"

client = mqtt.Client()
client.connect(broker, port, 60)
print("✅ Multi-Vehicle Simulator Online. Generating raw sensor data...")

# ADD ALL YOUR VEHICLE IDs HERE (Must exactly match the IDs in the dashboard)
ACTIVE_VEHICLES = [
    "KL-01-AJ-2000", 
    "KL-07-BM-3100", 
    "KL-33-5560", 
    "KL-6754", 
    "KL M 12899"
]

try:
    while True:
        # Loop through each vehicle and generate data
        for vid in ACTIVE_VEHICLES:
            payload = {
                "vehicle_id": vid,
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
            
            # Publish Raw Data for the specific vehicle
            client.publish(topic, json.dumps(payload))
            print(f"📡 Sent RAW Data for {vid}: Temp {payload['temp']}°C | Speed {payload['speed']} km/h")
            
            time.sleep(0.5) # Half-second delay between each vehicle's transmission
            
        print("-" * 50)
        time.sleep(2) # Wait 2 seconds before generating the next batch for all vehicles

except KeyboardInterrupt:
    print("\n🛑 Simulator Shutting Down.")