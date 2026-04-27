// 1. Initialize the map centered on DR Congo
const map = L.map('map').setView([-4.0383, 21.7587], 5);

// 2. Add a background map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// 3. Create "Groups" to hold our markers (this allows us to toggle them on/off)
const conflictLayer = L.layerGroup().addTo(map);
const schoolLayer = L.layerGroup().addTo(map);

// --- CONFLICT DATA LOGIC ---
function getConflictColor(cause) {
    switch (cause) {
        case 'Battle': return '#e67e22';
        case 'Violence against civilians': return '#e74c3c';
        case 'Protest': return '#3498db';
        default: return '#95a5a6';
    }
}

Papa.parse("cleaned_drc_conflict_data.csv", {
    download: true,
    header: true,
    complete: function(results) {
        results.data.forEach(row => {
            if (row.latitude && row.longitude) {
                const circle = L.circleMarker([row.latitude, row.longitude], {
                    radius: 5 + (parseInt(row.severity) || 0),
                    color: '#fff',
                    weight: 1,
                    fillColor: getConflictColor(row.cause),
                    fillOpacity: 0.7
                });
                circle.bindPopup(`<strong>Conflict: ${row.cause}</strong><br>Fatalities: ${row.severity}`);
                conflictLayer.addLayer(circle);
            }
        });
    }
});

// --- SCHOOL DATA LOGIC ---
Papa.parse("school_drc.csv", {
    download: true,
    header: true,
    complete: function(results) {
        results.data.forEach(row => {
            if (row.latitude && row.longitude) {
                // Schools will be Blue squares (diamond shape)
                const schoolMarker = L.circleMarker([row.latitude, row.longitude], {
                    radius: 6,
                    color: '#2c3e50',
                    weight: 1,
                    fillColor: '#34495e', // Dark blue/gray
                    fillOpacity: 0.9
                });
                schoolMarker.bindPopup(`<strong>School: ${row.school_name}</strong><br>Level: ${row.level}<br>Status: ${row.status}`);
                schoolLayer.addLayer(schoolMarker);
            }
        });
    }
});

// 4. Add a Toggle Box (Layer Control) in the top right
const overlayMaps = {
    "Conflict Events": conflictLayer,
    "Schools": schoolLayer
};
L.control.layers(null, overlayMaps).addTo(map);

// 5. Update the Legend
const legend = L.control({position: 'bottomright'});
legend.onAdd = function (map) {
    const div = L.DomUtil.create('div', 'info legend');
    div.innerHTML = `
        <div style="background: white; padding: 10px; border-radius: 5px; border: 1px solid #ccc;">
            <strong>Map Legend</strong><br>
            <i style="background: #e74c3c; width: 10px; height: 10px; display: inline-block;"></i> Conflict (Violence)<br>
            <i style="background: #e67e22; width: 10px; height: 10px; display: inline-block;"></i> Conflict (Battle)<br>
            <i style="background: #34495e; width: 10px; height: 10px; display: inline-block;"></i> <strong>School</strong> (Location)
        </div>
    `;
    return div;
};
legend.addTo(map);
