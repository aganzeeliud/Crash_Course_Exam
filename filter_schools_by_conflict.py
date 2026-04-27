import json
import csv
import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the distance in kilometers between two points on Earth.
    """
    R = 6371  # Earth radius in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def find_schools_near_conflicts(school_file, conflict_file, radius_km=5.0):
    # 1. Load the schools we already downloaded
    with open(school_file, 'r', encoding='utf-8') as f:
        school_data = json.load(f)
    
    # 2. Load the conflict events from CSV
    conflicts = []
    with open(conflict_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # We only care about events in DRC (different names used in file)
            if row['country'].lower() in ['democratic republic of congo', 'drc', 'congo-kinshasa']:
                conflicts.append({
                    'lat': float(row['lat']),
                    'lon': float(row['lon']),
                    'date': row['event_date'],
                    'type': row['event_type']
                })
    
    print(f"Loaded {len(conflicts)} conflict events in DRC.")
    
    # 3. Filter schools that are within the radius of ANY conflict
    nearby_schools = []
    for school in school_data['features']:
        s_lon, s_lat = school['geometry']['coordinates']
        
        is_near = False
        closest_conflict = None
        min_dist = float('inf')
        
        for conflict in conflicts:
            dist = haversine(s_lat, s_lon, conflict['lat'], conflict['lon'])
            if dist <= radius_km:
                is_near = True
                if dist < min_dist:
                    min_dist = dist
                    closest_conflict = conflict
        
        if is_near:
            # Add conflict info to the school's properties
            new_school = json.loads(json.dumps(school)) # Deep copy
            new_school['properties']['nearest_conflict_dist_km'] = round(min_dist, 2)
            new_school['properties']['conflict_type'] = closest_conflict['type']
            new_school['properties']['conflict_date'] = closest_conflict['date']
            nearby_schools.append(new_school)
            
    print(f"Found {len(nearby_schools)} schools within {radius_km}km of a conflict event.")
    
    # 4. Save as GeoJSON
    output_geojson = {
        "type": "FeatureCollection",
        "features": nearby_schools
    }
    with open('schools_near_conflicts.geojson', 'w', encoding='utf-8') as f:
        json.dump(output_geojson, f, indent=2)
        
    # 5. Save as CSV
    if nearby_schools:
        all_keys = set()
        for s in nearby_schools:
            all_keys.update(s['properties'].keys())
        
        header = ['osm_id', 'latitude', 'longitude'] + sorted(list(all_keys))
        
        with open('schools_near_conflicts.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            for s in nearby_schools:
                row = s['properties'].copy()
                row['longitude'], row['latitude'] = s['geometry']['coordinates']
                writer.writerow(row)
                
    print("Saved results to schools_near_conflicts.geojson and schools_near_conflicts.csv")

if __name__ == "__main__":
    find_schools_near_conflicts('schools_drc.geojson', 'conflict_event.csv')
