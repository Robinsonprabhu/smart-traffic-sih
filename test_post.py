import requests, time, random

while True:
    payload = {
        "time": int(time.time()),
        "lane_data": {
            "north_0": {"count": random.randint(5, 20), "speed": round(random.uniform(10, 30), 2)},
            "south_1": {"count": random.randint(3, 15), "speed": round(random.uniform(10, 25), 2)},
        },
        "emergency_detected": random.choice([False, False, False, True])  # rare emergency
    }
    res = requests.post("http://127.0.0.1:5000/update", json=payload)
    print("Sent:", payload)
    time.sleep(3)
