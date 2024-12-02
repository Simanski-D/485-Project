document.addEventListener('DOMContentLoaded', function () {
    const fileName = localStorage.getItem('fileName');
    console.log('File name retrieved from localStorage:', fileName);
    const fullPath = "./outputfiles/" + fileName;

    // Initialize the map and set its view to a specific location and zoom level
    const map = L.map('map').setView([0, -10], 1);
    // Add a tile layer to the map (using OpenStreetMap tiles)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
            data.forEach(function(row) {
                let lat = row.client.geo.location.lat; 
                let lon = row.client.geo.location.lon;
                L.marker([lat, lon]).addTo(map)
                    .bindPopup('<b>Location:</b> ' + row.name);
            });
});