// Initialize the map and set its view to a specific location and zoom level
const map = L.map('map').setView([0, -10], 1);  // Starting view of the map

// Add a tile layer (OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Fetch points from the backend API (/api/points)
fetch('/api/points')
    .then(response => response.json())  // Parse JSON response
    .then(points => {
        // Loop through the points and add them to the map as markers
        points.forEach(point => {
            // Format the timestamp
            const timestamp = new Date(point.logTime).toLocaleString();

            // Bind a popup with the label and timestamp
            L.marker(point.coords)
                .addTo(map)
                .bindPopup(`<b>${point.label}</b><br>Timestamp: ${logTime}`);
        });
    })
    .catch(error => {
        console.error('Error fetching points:', error);
    });