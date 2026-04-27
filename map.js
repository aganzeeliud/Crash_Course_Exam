// 1. Initialize the map centered on DR Congo
const map = L.map('map').setView([-4.0383, 21.7587], 5);

// 2. Add a background map (OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// 3. Load the data from our CSV file
Papa.parse("data/schools_near_conflicts.csv", {
    download: true,
    header: true,
    complete: function(results) {
        console.log("Loaded " + results.data.length + " rows");
        
        results.data.forEach(row => {
            // Check if we have valid coordinates
            if (row.latitude && row.longitude) {
                // Create a circle marker for each school
                const marker = L.circleMarker([parseFloat(row.latitude), parseFloat(row.longitude)], {
                    radius: 6,
                    fillColor: "#ff4d4d", // Red color
                    color: "#fff",
                    weight: 1,
                    fillOpacity: 0.8
                });

                // Add a popup with the details
                // row.name is the school name
                // row.conflict_date, row.conflict_type, and row.nearest_conflict_dist_km come from our processing
                const schoolName = row.name || "Unnamed School";
                const popupContent = `
                    <div style="font-family: Arial, sans-serif;">
                        <h4 style="margin: 0 0 5px 0; color: #d32f2f;">${schoolName}</h4>
                        <hr>
                        <b>Recent Conflict:</b> ${row.conflict_type || 'Unknown'}<br>
                        <b>Date:</b> ${row.conflict_date || 'Unknown'}<br>
                        <b>Distance to event:</b> ${row.nearest_conflict_dist_km} km<br>
                        <small style="color: #666;">ID: ${row.osm_id}</small>
                    </div>
                `;

                marker.bindPopup(popupContent);
                marker.addTo(map);
            }
        });
    }
});
