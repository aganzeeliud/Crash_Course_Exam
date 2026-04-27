// 1. Initialize the map centered on DR Congo
const map = L.map('map').setView([-2.0, 25.0], 5);

// 2. Add a background map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// 3. Load the 1km Historical Risk data
Papa.parse("data/schools_1km_historical.csv", {
    download: true,
    header: true,
    complete: function(results) {
        results.data.forEach(row => {
            if (row.latitude && row.longitude) {
                // Circle markers for schools
                const marker = L.circleMarker([parseFloat(row.latitude), parseFloat(row.longitude)], {
                    radius: 7,
                    fillColor: "#e74c3c", // Bright red for high risk
                    color: "#000",
                    weight: 1,
                    fillOpacity: 0.9
                });

                const popupContent = `
                    <div style="font-family: Arial, sans-serif;">
                        <h4 style="margin:0; color:#c0392b;">${row.name}</h4>
                        <hr>
                        <b style="color:#d35400;">High Risk Area (within 1km)</b><br>
                        <b>Historical Conflict:</b> ${row.conflict_type}<br>
                        <b>Year:</b> ${row.conflict_year}<br>
                        <b>Location:</b> ${row.conflict_location}<br>
                        <b>Exact Distance:</b> ${row.dist_km} km
                    </div>
                `;

                marker.bindPopup(popupContent);
                marker.addTo(map);
            }
        });
    }
});
