import { useEffect, useState } from "react";

function App() {
  const [trafficData, setTrafficData] = useState({
    green_lane: "",
    north_count: 0,
    south_count: 0,
    north_emergency: false,
    south_emergency: false,
    phase: "",
    timer: 0
  });

  const [flash, setFlash] = useState(false); // for emergency flashing

  // Fetch traffic JSON every 1 second
  useEffect(() => {
    const interval = setInterval(() => {
      fetch("http://127.0.0.1:5000/traffic_data")
        .then((res) => res.json())
        .then((data) => setTrafficData(data))
        .catch((err) => console.error(err));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // Flash emergency every 0.5s
  useEffect(() => {
    const flashInterval = setInterval(() => setFlash((f) => !f), 500);
    return () => clearInterval(flashInterval);
  }, []);

  const getLaneColor = (lane) => {
    const isGreen = trafficData.green_lane === lane && trafficData.phase === "green";
    const isYellow = trafficData.green_lane === lane && trafficData.phase === "yellow";
    const isRed = trafficData.green_lane !== lane;

    if (lane === "North" && trafficData.north_emergency && flash) return "red";
    if (lane === "South" && trafficData.south_emergency && flash) return "red";

    if (isGreen) return "green";
    if (isYellow) return "yellow";
    if (isRed) return "grey";
  };

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>Smart Traffic Dashboard</h1>

      <div style={{ display: "flex", gap: 20 }}>
        {/* Video Feed */}
        <div>
          <h2>Live Video Feed</h2>
          <img
            src="http://127.0.0.1:5000/video_feed"
            alt="Traffic Video Feed"
            style={{ border: "2px solid black", width: 700 }}
          />
        </div>

        {/* Traffic Data */}
        <div>
          <h2>Traffic Signals</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            <div
              style={{
                backgroundColor: getLaneColor("North"),
                padding: 20,
                width: 200,
                color: "white",
                fontWeight: "bold",
                textAlign: "center",
                borderRadius: 8
              }}
            >
              North Lane: {trafficData.north_count} vehicles
              <br />
              Emergency: {trafficData.north_emergency ? "Yes" : "No"}
            </div>

            <div
              style={{
                backgroundColor: getLaneColor("South"),
                padding: 20,
                width: 200,
                color: "white",
                fontWeight: "bold",
                textAlign: "center",
                borderRadius: 8
              }}
            >
              South Lane: {trafficData.south_count} vehicles
              <br />
              Emergency: {trafficData.south_emergency ? "Yes" : "No"}
            </div>
          </div>

          <div style={{ marginTop: 20 }}>
            <p>
              <strong>Phase:</strong> {trafficData.phase} <br />
              <strong>Green Lane:</strong> {trafficData.green_lane} <br />
              <strong>Timer:</strong> {trafficData.timer}s
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
