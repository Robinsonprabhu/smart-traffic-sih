import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

export default function TrafficDashboard() {
  const [lanes, setLanes] = useState({ N: 0, S: 0, E: 0, W: 0 });
  const [signal, setSignal] = useState("Loading...");

  // Fetch from backend every 1 sec
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("http://127.0.0.1:5000/traffic");
        const data = await res.json();
        setLanes(data.lanes);
        setSignal(data.signal);
      } catch (err) {
        console.error("Backend not reachable:", err);
      }
    };

    fetchData(); // initial fetch
    const interval = setInterval(fetchData, 1000);
    return () => clearInterval(interval);
  }, []);

  // Lane labels + counts
  const laneNames = Object.keys(lanes);
  const vehicleCounts = Object.values(lanes);

  // Signal color
  const getSignalColor = (signal) => {
    if (!signal) return "black";
    if (signal.includes("Green")) return "green";
    if (signal.includes("Red")) return "red";
    return "orange";
  };

  return (
    <div style={{ textAlign: "center", fontFamily: "Arial" }}>
      <h1>🚦 Live Traffic Dashboard</h1>

      <h2 style={{ color: getSignalColor(signal) }}>
        {signal}
      </h2>

      <Plot
        data={[
          {
            x: laneNames,
            y: vehicleCounts,
            type: "bar",
            marker: { color: "orange" },
          },
        ]}
        layout={{
          title: "Traffic Flow per Lane (# of Vehicles)",
          yaxis: { title: "Vehicles" },
        }}
        style={{ width: "80%", margin: "auto" }}
      />
    </div>
  );
}
