document.addEventListener("DOMContentLoaded", () => {
  // 1. Start feed ticker simulation
  const ticker = document.querySelector(".ticker");
  setInterval(() => {
    ticker.textContent = new Date().toLocaleTimeString() +
      " — Phishing URL detected: http://evil.example.com";
  }, 2000);

  // 2. Initialize map (e.g. Leaflet or D3, later)
  // 3. Render charts (Chart.js, D3)
  // …and so on for each widget
});
