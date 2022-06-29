// const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
// const map = L.map('map')
// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution:
// attribution }).addTo(map);
// const markers = JSON.parse(document.getElementById('markers-data').textContent);
// let feature = L.geoJSON(markers).bindPopup(function (layer) { return
// layer.feature.properties.name; }).addTo(map);
// map.fitBounds(feature.getBounds(), { padding: [100, 100] });

var map = L.map('map').setView([-24.72823906, -65.4059906], 60);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

L.marker([-24.72823906, -65.4059906]).addTo(map)
    .bindPopup('Universidad Nacional de Salta.<br> Mi sabiduría viene de esta tierra.')
    .openPopup();