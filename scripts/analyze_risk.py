import json
import csv
import math
import os

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the distance in kilometers between two points on Earth
    using the Haversine formula.
    """
    R = 6371  # Earth radius in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def analyze_school_risk():
    school_file = 'data/schools_drc.geojson'
    conflict_file = 'data/conflict_event.csv'
    
    # 1. Load school data
    with open(school_file, 'r', encoding='utf-8') as f:
        school_data = json.load(f)
    
    # 2. Load conflict data
    conflicts = []
    with open(conflict_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['country'].lower() in ['democratic republic of congo', 'drc', 'congo-kinshasa']:
                conflicts.append({
                    'lat': float(row['lat']),
                    'lon': float(row['lon']),
                    'type': row['event_type'],
                    'date': row['event_date']
                })
    
    print(f"Analyzing {len(school_data['features'])} schools against {len(conflicts)} conflict events...")

    at_risk_list = []
    safe_list = []

    # 3. Process each school
    for school in school_data['features']:
        s_lon, s_lat = school['geometry']['coordinates']
        
        min_dist = float('inf')
        nearest_event = None
        
        for conflict in conflicts:
            dist = haversine(s_lat, s_lon, conflict['lat'], conflict['lon'])
            if dist < min_dist:
                min_dist = dist
                nearest_event = conflict
        
        # Determine risk status (0-10km is at-risk)
        risk_status = "at-risk" if min_dist <= 10.0 else "safe"
        
        # Prepare the data row
        row = {
            'name': school['properties'].get('name', 'Unnamed School'),
            'latitude': s_lat,
            'longitude': s_lon,
            'risk_status': risk_status,
            'distance_km': round(min_dist, 2),
            'nearest_conflict_type': nearest_event['type'] if nearest_event else 'N/A',
            'nearest_conflict_date': nearest_event['date'] if nearest_event else 'N/A',
            'osm_id': school['properties'].get('osm_id')
        }
        
        if risk_status == "at-risk":
            at_risk_list.append(row)
        else:
            safe_list.append(row)

    # 4. Save the files
    fieldnames = ['name', 'latitude', 'longitude', 'risk_status', 'distance_km', 'nearest_conflict_type', 'nearest_conflict_date', 'osm_id']
    
    with open('data/at_risk_schools.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(at_risk_list)
        
    with open('data/safe_schools.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(safe_list)
            
    print(f"Analysis complete:")
    print(f"- At-risk schools: {len(at_risk_list)}")
    print(f"- Safe schools: {len(safe_list)}")
    print("Files saved: data/at_risk_schools.csv and data/safe_schools.csv")

if __name__ == "__main__":
    analyze_school_risk()
