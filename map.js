// 1. Initialize the map centered on DR Congo
const map = L.map('map').setView([-4.0383, 21.7587], 5);

// 2. Add a background map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// 3. Create Layers
const conflictLayer = L.layerGroup().addTo(map);
const schoolLayer = L.layerGroup().addTo(map);

// --- HISTORICAL CONFLICT DATA LOGIC ---
function getConflictColor(type) {
    switch (type) {
        case 'Battle': return '#e67e22';
        case 'Violence against civilians': return '#e74c3c';
        case 'Protest': return '#3498db';
        default: return '#9b59b6'; // Purple for others
    }
}

Papa.parse("DRC Conflict.csv", {
    download: true,
    header: true,
    complete: function(results) {
        results.data.forEach(row => {
            if (row.latitude && row.longitude) {
                const circle = L.circleMarker([row.latitude, row.longitude], {
                    radius: 6 + (Math.sqrt(parseInt(row.fatalities)) || 0), // Logarithmic scale for better visual
                    color: '#fff',
                    weight: 1,
                    fillColor: getConflictColor(row.event_type),
                    fillOpacity: 0.8
                });
                
                const popup = `
                    <div style="font-family: sans-serif; width: 200px;">
                        <h4 style="margin:0; color:#c0392b;">${row.event_type} (${row.year})</h4>
                        <hr>
                        <strong>Location:</strong> ${row.location}<br>
                        <strong>Fatalities:</strong> ${row.fatalities}<br>
                        <strong>Source:</strong> ${row.source}<br><br>
                        <em>${row.description || ''}</em>
                    </div>
                `;
                circle.bindPopup(popup);
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
                const schoolMarker = L.circleMarker([row.latitude, row.longitude], {
                    radius: 5,
                    color: '#2c3e50',
                    weight: 1,
                    fillColor: '#34495e',
                    fillOpacity: 0.9
                });
                schoolMarker.bindPopup(`<strong>School: ${row.school_name}</strong><br>Level: ${row.level}`);
                schoolLayer.addLayer(schoolMarker);
            }
        });
    }
});

// 4. Layer Control
L.control.layers(null, {
    "Historical Conflicts": conflictLayer,
    "Schools": schoolLayer
}).addTo(map);

// 5. Updated Legend
const legend = L.control({position: 'bottomright'});
legend.onAdd = function (map) {
    const div = L.DomUtil.create('div', 'info legend');
    div.innerHTML = `
        <div style="background: white; padding: 10px; border-radius: 5px; border: 1px solid #ccc; line-height:1.6;">
            <strong>Map Legend</strong><br>
            <i style="background: #e74c3c; width: 10px; height: 10px; display: inline-block;"></i> Violence Against Civilians<br>
            <i style="background: #e67e22; width: 10px; height: 10px; display: inline-block;"></i> Battle<br>
            <i style="background: #9b59b6; width: 10px; height: 10px; display: inline-block;"></i> Other Conflict Type<br>
            <i style="background: #34495e; width: 10px; height: 10px; display: inline-block;"></i> School Location
        </div>
    `;
    return div;
};
legend.addTo(map);
