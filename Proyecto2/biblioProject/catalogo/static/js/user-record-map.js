const map = L.map('map').setView([-24.72823906, -65.4059906], 17);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

let oneMarket = false;

map.on('dblclick', function(event) {
    if (! oneMarket) {
        oneMarket = true;

        let latitude = document.getElementById('id_latitude');
        let longitude = document.getElementById('id_longitude');
    
        let marker = L.marker([event.latlng.lat, event.latlng.lng],{
            draggable: true
        }).addTo(map);

        latitude.value = marker.getLatLng().lat;
        longitude.value = marker.getLatLng().lng;
    
        marker.on('moveend', () => {
            latitude.value = marker.getLatLng().lat;
            longitude.value = marker.getLatLng().lng;
        });   
    }               
});
