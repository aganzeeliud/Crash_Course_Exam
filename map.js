// 1. Initialize the map centered on DR Congo
const map = L.map('map').setView([-4.0383, 21.7587], 5);

// 2. Add a background map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// 3. Create Layers
const conflictLayer = L.layerGroup().addTo(map);
const schoolLayer = L.layerGroup().addTo(map);

let allConflictData = []; // Store data here so we can filter it easily

// Helper function for colors
function getConflictColor(type) {
    switch (type) {
        case 'Battle': return '#e67e22';
        case 'Violence against civilians': return '#e74c3c';
        default: return '#9b59b6';
    }
}

// 4. Function to draw markers for a specific year
function updateMap(selectedYear) {
    conflictLayer.clearLayers(); // Clear old markers
    document.getElementById('current-year').innerText = selectedYear; // Update label

    allConflictData.forEach(row => {
        // Only show if the year matches the slider
        if (row.year == selectedYear && row.latitude && row.longitude) {
            const circle = L.circleMarker([row.latitude, row.longitude], {
                radius: 8 + (Math.sqrt(parseInt(row.fatalities)) || 0),
                color: '#fff',
                weight: 1,
                fillColor: getConflictColor(row.event_type),
                fillOpacity: 0.8
            });
            
            circle.bindPopup(`
                <strong>${row.event_type} (${row.year})</strong><br>
                ${row.location}<br>
                <em>${row.description}</em>
            `);
            conflictLayer.addLayer(circle);
        }
    });
}

// 5. Load Data
Papa.parse("DRC Conflict.csv", {
    download: true,
    header: true,
    complete: function(results) {
        allConflictData = results.data;
        updateMap(2024); // Show the most recent year by default
    }
});

Papa.parse("school_drc.csv", {
    download: true,
    header: true,
    complete: function(results) {
        results.data.forEach(row => {
            if (row.latitude && row.longitude) {
                const schoolMarker = L.circleMarker([row.latitude, row.longitude], {
                    radius: 4,
                    color: '#2c3e50',
                    fillColor: '#34495e',
                    fillOpacity: 0.5
                });
                schoolMarker.bindPopup(`<strong>School: ${row.school_name}</strong>`);
                schoolLayer.addLayer(schoolMarker);
            }
        });
    }
});

// 6. Connect the Slider
document.getElementById('year-slider').addEventListener('input', function(e) {
    updateMap(e.target.value);
});

// 7. Layer Control & Legend
L.control.layers(null, { "Conflicts": conflictLayer, "Schools": schoolLayer }).addTo(map);
