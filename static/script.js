// Initialize the map and set its view to a specific location and zoom level
const map2 = L.map('map2').setView([0, -10], 0.5);

// Add a tile layer to the map (using OpenStreetMap tiles)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map2);

// Define an array of points to project on the map
const points2 = [
    { coords: [44.8113, -91.498], label: 'Point 1' },
];

// Loop through the points and add them to the map
points2.forEach(point => {
    L.marker(point.coords)
        .addTo(map2)
        .bindPopup(point.label)
        .openPopup();
});