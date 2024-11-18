// Initialize the map and set its view to a specific location and zoom level
const map = L.map('map').setView([-10, 10], 1);

// Add a tile layer to the map (using OpenStreetMap tiles)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

// Define an array of points to project on the map
const points = [
    { coords: [44.8113, -91.498], label: 'Point 1' },
];

// Loop through the points and add them to the map
points.forEach(point => {
    L.marker(point.coords)
        .addTo(map)
        .bindPopup(point.label)
        .openPopup();
});