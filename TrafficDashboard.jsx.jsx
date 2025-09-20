import React, { useState, useEffect } from "react";
import "./TrafficDashboard.css";

const initialTrafficData = [
  { id: 1, type: "Car", count: 12 },
  { id: 2, type: "Bus", count: 3 },
  { id: 3, type: "Ambulance", count: 1 },
];

const TrafficDashboard = () => {
  const [trafficData, setTrafficData] = useState(initialTrafficData);

  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate real-time updates by incrementing counts
      setTrafficData((prevData) =>
        prevData.map((vehicle) => ({
          ...vehicle,
          count: vehicle.count + Math.floor(Math.random() * 3), // Increment by a random number
        }))
      );
    }, 2000); // Update every 2 seconds

    return () => clearInterval(interval); // Cleanup interval on component unmount
  }, []);

  return (
    <div className="dashboard">
      <h1>Live Traffic Dashboard</h1>
      <ul>
        {trafficData.map((vehicle) => (
          <li key={vehicle.id}>
            {vehicle.type}: {vehicle.count}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TrafficDashboard;