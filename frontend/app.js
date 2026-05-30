// app.js
const API = "http://127.0.0.1:8000";

// Initialize map centered on Kampala
const map = L.map("map").setView([0.3136, 32.5811], 13);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap contributors"
}).addTo(map);

let circleLayer = L.layerGroup().addTo(map);

// Slider label update
const slider = document.getElementById("timestepSlider");
const label = document.getElementById("timestepLabel");

slider.addEventListener("input", () => {
  const h = parseInt(slider.value);
  const day = Math.floor(h / 24);
  const hour = h % 24;
  const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  label.textContent = `${days[day]} ${hour}:00`;
});

// Get color based on congestion score
function getColor(score) {
  if (score < 0.35) return "#2ecc71";
  if (score < 0.65) return "#f39c12";
  return "#e74c3c";
}

// Load and render predictions
document.getElementById("loadBtn").addEventListener("click", async () => {
  const timestep = slider.value;
  const btn = document.getElementById("loadBtn");

  btn.textContent = "Loading...";
  btn.disabled = true;

  try {
    const res = await fetch(`${API}/predict/${timestep}`);
    const data = await res.json();

    // Clear previous layer
    circleLayer.clearLayers();

    let total = 0;
    let high = 0;

    data.nodes.forEach(node => {
      const color = getColor(node.congestion);
      L.circleMarker([node.lat, node.lon], {
        radius: 4,
        fillColor: color,
        color: color,
        weight: 0,
        fillOpacity: 0.8
      })
      .bindPopup(`
        <b>Node ${node.id}</b><br/>
        Congestion: ${(node.congestion * 100).toFixed(1)}%<br/>
        Lat: ${node.lat.toFixed(5)}<br/>
        Lon: ${node.lon.toFixed(5)}
      `)
      .addTo(circleLayer);

      total += node.congestion;
      if (node.congestion > 0.65) high++;
    });

    // Update stats
    document.getElementById("nodeCount").textContent = data.nodes.length.toLocaleString();
    document.getElementById("avgCongestion").textContent = (total / data.nodes.length * 100).toFixed(1) + "%";
    document.getElementById("highCount").textContent = high.toLocaleString();

  } catch (err) {
    alert("Error connecting to API. Make sure the backend is running.");
    console.error(err);
  }

  btn.textContent = "Load Predictions";
  btn.disabled = false;
});