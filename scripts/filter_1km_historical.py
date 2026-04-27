import json
import csv
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def filter_1km():
    school_file = 'data/schools_drc.geojson'
    conflict_file = 'data/conflict_drc_2000.csv'
    
    with open(school_file, 'r', encoding='utf-8') as f:
        schools = json.load(f)
    
    conflicts = []
    with open(conflict_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            conflicts.append({
                'lat': float(row['latitude']),
                'lon': float(row['longitude']),
                'year': row['year'],
                'type': row['event_type'],
                'location': row['location']
            })
    
    results = []
    for school in schools['features']:
        s_lon, s_lat = school['geometry']['coordinates']
        
        for conflict in conflicts:
            dist = haversine(s_lat, s_lon, conflict['lat'], conflict['lon'])
            if dist <= 1.0: # 1km threshold
                row = {
                    'name': school['properties'].get('name', 'Unnamed School'),
                    'latitude': s_lat,
                    'longitude': s_lon,
                    'dist_km': round(dist, 2),
                    'conflict_year': conflict['year'],
                    'conflict_type': conflict['type'],
                    'conflict_location': conflict['location']
                }
                results.append(row)
                break # Move to next school once one near conflict is found
    
    # Save results
    if results:
        keys = results[0].keys()
        with open('data/schools_1km_historical.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
    
    print(f"Found {len(results)} schools within 1km of historical conflicts.")

if __name__ == "__main__":
    filter_1km()
