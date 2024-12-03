/*document.addEventListener('DOMContentLoaded', function () {
    const map = L.map('map').setView([0, -10], 1);
    // Add a tile layer to the map (using OpenStreetMap tiles)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    const fileName = localStorage.getItem('fileName');
    if(fileName !== null){
        console.log('File name retrieved from localStorage:', fileName);
        const fullPath = "./outputfiles/" + fileName;
        d3.csv(fullPath).then(function(data) {
            data.forEach(function(row) {
                let lat = row["client.geo.location.lat"]; 
                let lon = row["client.geo.location.lon"];
                
                // Add a marker at each coordinate
                L.marker([lat, lon]).addTo(map)
                  .bindPopup('<b>Location:</b> ' + row.name);
              });
            });
        }
}); */