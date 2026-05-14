import time
import json
import random
import paho.mqtt.client as mqtt
from fuzzy_engine import get_health_score

# 1. Edge Communication Gateway Target
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
TOPIC = "fleet/telemetry/pro"

# 2. Comprehensive State Highway 11 (AC Road) Interconnection Path Array
# Traces a highly granular long-distance trajectory directly from Changanassery down into Alappuzha
AC_ROAD_CORRIDOR = [
    (9.445000, 76.540000), # Path Node 1: Changanassery Origin (Perunna Junction framework)
    (9.442000, 76.520000), # Path Node 2: Passing Paippad Eastern Approach
    (9.435000, 76.480000), # Path Node 3: Kidangara Bridge Crossing Vector
    (9.428000, 76.450000), # Path Node 4: Traversing Veliyanad Wetlands Stretch
    (9.420000, 76.420000), # Path Node 5: Ramankary / Mankombu Core Arterial Sector
    (9.418000, 76.405000), # Path Node 6: Moncompu Junction Pathway Convergence
    (9.430000, 76.385000), # Path Node 7: Approaching Champakulam Access Corridor
    (9.440000, 76.365000), # Path Node 8: Nedumudi / Pallathuruthy River Interface
    (9.465000, 76.350000), # Path Node 9: Entering Kainakary Border Stretch
    (9.498100, 76.338800), # Path Node 10: Alappuzha Destination Terminus (Finishing Point / Mullakkal Sector)
]

def interpolate_position(start, end, fraction):
    """Calculates granular dynamic spatial steps between primary regional tracking nodes."""
    lat = start[0] + (end[0] - start[0]) * fraction
    lon = start[1] + (end[1] - start[1]) * fraction
    return lat, lon

# Connect MQTT edge routing engine protocols
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

try:
    print(f"Connecting to Data Gateway: {MQTT_BROKER}...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("Network Connection Established Securely.")
    print("Abhirami's Core AC-Road Telemetry Engine Running. Press Ctrl+C to Exit.\n")

    corridor_index = 0
    step_fraction = 0.0
    step_increment = 0.15  # Dynamic regional route crawling speed assertions
    cycle_counter = 0

    while True:
        cycle_counter += 1

        # --- COMBINATORIAL ENGINE SCENARIO PROFILER ---
        # Seamlessly rotates cruising vectors with critical urban path traffic stagnation hazards
        if cycle_counter % 12 < 8:
            # OPTIMAL PROFILE: HIGH-SPEED CRUISE ALONG AC ROAD STRETCH
            temperature = random.uniform(72.5, 86.0)
            speed = random.uniform(45.0, 72.0)
            engine_state = "STABLE"
            step_increment = 0.18 # Vehicle advances rapidly across highway segments
        else:
            # HAZARD PROFILE: BRIDGE BOTTLENECK TRAFFIC OVERLOAD SCENARIO
            temperature = random.uniform(111.5, 121.8)
            speed = random.uniform(0.0, 4.5)
            engine_state = "CRITICAL"
            step_increment = 0.02 # Ground map marker dynamically decelerates/crawls visibly

        # Extrapolate physical regional path points
        current_waypoint = AC_ROAD_CORRIDOR[corridor_index]
        next_waypoint = AC_ROAD_CORRIDOR[(corridor_index + 1) % len(AC_ROAD_CORRIDOR)]
        
        target_lat, target_lon = interpolate_position(current_waypoint, next_waypoint, step_fraction)
        
        # Increment step calculations cleanly
        step_fraction += step_increment
        if step_fraction >= 1.0:
            step_fraction = 0.0
            corridor_index = (corridor_index + 1) % len(AC_ROAD_CORRIDOR)

        # Process native risk indices via Abhirami's integrated Fuzzy rule matrices
        risk_score = get_health_score(temperature, speed)
        status_assertion = "CRITICAL" if risk_score > 75 else "STABLE"

        # Frame telemetry target blocks
        telemetry_frame = {
            "vehicle_id": "KL-01-AJ-2000",
            "temp": round(temperature, 2),
            "speed": round(speed, 2),
            "risk_score": round(risk_score, 2),
            "engine_status": status_assertion,
            "lat": round(target_lat, 6),
            "lon": round(target_lon, 6),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Transmit target state structures across standard socket gateways
        payload_bytes = json.dumps(telemetry_frame)
        client.publish(TOPIC, payload_bytes)

        # Print output assertions exclusively using clean professional English string assertions
        if status_assertion == "CRITICAL":
            print(f"[CRITICAL TRAJECTORY] Payload Sent -> State: {status_assertion} | Temp: {telemetry_frame['temp']}C | Speed: {telemetry_frame['speed']}km/h | Hazard Score: {telemetry_frame['risk_score']}%")
        else:
            print(f"[OPTIMAL CRUISE] Payload Sent -> State: {status_assertion} | Temp: {telemetry_frame['temp']}C | Speed: {telemetry_frame['speed']}km/h | Hazard Score: {telemetry_frame['risk_score']}%")

        # Cycle core ingestion sleep loop throttles
        time.sleep(3)

except Exception as err:
    print(f"\nRuntime Ingestion Error: {err}")
finally:
    client.disconnect()
    print("\nNetwork Port Terminated. Edge Layer Closed.")