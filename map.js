// 1. Initialize the map centered on DR Congo
const map = L.map('map').setView([-4.0383, 21.7587], 5);

// 2. Add a background map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// 3. Define colors for different types of conflict
function getColor(cause) {
    switch (cause) {
        case 'Battle': return '#e67e22'; // Orange
        case 'Violence against civilians': return '#e74c3c'; // Red
        case 'Protest': return '#3498db'; // Blue
        case 'Strategic development': return '#2ecc71'; // Green
        default: return '#95a5a6'; // Gray for others
    }
}

// 4. Load and parse the CSV file
Papa.parse("cleaned_drc_conflict_data.csv", {
    download: true,
    header: true,
    complete: function(results) {
        const data = results.data;

        data.forEach(row => {
            if (row.latitude && row.longitude) {
                // Circle size based on severity
                const radius = 5 + (parseInt(row.severity) || 0);
                
                const circle = L.circleMarker([row.latitude, row.longitude], {
                    radius: radius,
                    color: '#fff', // White border
                    weight: 1,
                    fillColor: getColor(row.cause),
                    fillOpacity: 0.7
                }).addTo(map);

                const popupContent = `
                    <div style="font-family: sans-serif;">
                        <h4 style="margin:0 0 5px 0;">${row.cause}</h4>
                        <strong>Date:</strong> ${row.date || row.event_date}<br>
                        <strong>Fatalities:</strong> ${row.severity}
                    </div>
                `;
                circle.bindPopup(popupContent);
            }
        });
    }
});

// 5. Add a Legend to the map
const legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {
    const div = L.DomUtil.create('div', 'info legend');
    const categories = ['Battle', 'Violence against civilians', 'Protest', 'Strategic development', 'Other'];
    const colors = ['#e67e22', '#e74c3c', '#3498db', '#2ecc71', '#95a5a6'];

    div.innerHTML = '<div style="background: white; padding: 10px; border-radius: 5px; line-height: 1.5; border: 1px solid #ccc;">' +
                    '<strong>Conflict Type</strong><br>';
    
    for (let i = 0; i < categories.length; i++) {
        div.innerHTML += `<i style="background: ${colors[i]}; width: 12px; height: 12px; display: inline-block; margin-right: 5px;"></i> ${categories[i]}<br>`;
    }
    
    div.innerHTML += '</div>';
    return div;
};

legend.addTo(map);
