// Initialize the map and set its view to a specific location and zoom level
const map = L.map('map').setView([0, -10], 1);

// Add a tile layer to the map (using OpenStreetMap tiles)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Define an array of points to project on the map
const points = [
    { coords: [44.8113, -91.498], label: 'Point 1' },
    { coords: [-79.69945802, 53.58869902], label: 'Point 2' },
    { coords: [22.52146577, 78.13385823], label: 'Point 3' },
    { coords: [-24.22448156, 150.9585045], label: 'Point 4' },
    { coords: [9.510528056,    -75.8855839], label: 'Point 5' },
    { coords: [65.96210701,    42.84632654], label: 'Point 6' },
];

// Loop through the points and add them to the map
points.forEach(point => {
    L.marker(point.coords)
        .addTo(map)
        .bindPopup(point.label);
});
