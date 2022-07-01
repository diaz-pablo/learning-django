const map = L.map('map').setView([-24.72823906, -65.4059906], 17);  

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

const markers = JSON.parse(document.getElementById('markers-data').textContent);

let feature = L.geoJSON(markers).bindPopup(function (layer) {
    return layer.feature.properties.name;
}).addTo(map);

map.fitBounds(feature.getBounds(), { padding: [100, 100] });