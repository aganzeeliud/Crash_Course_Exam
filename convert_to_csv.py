import json
import csv

def geojson_to_csv(input_file, output_file):
    # 1. Open and read the GeoJSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    features = data.get('features', [])
    if not features:
        print("No data found in GeoJSON.")
        return

    # 2. Collect all possible column headers
    # Since different schools might have different information (tags),
    # we look through all of them to find every possible column name.
    all_keys = set()
    for feature in features:
        all_keys.update(feature['properties'].keys())
    
    # We want Latitude and Longitude to be at the start for easy reading
    header = ['osm_id', 'osm_type', 'latitude', 'longitude'] + sorted(list(all_keys))
    
    # 3. Write to the CSV file
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        
        for feature in features:
            # Flatten the data into a single row
            row = feature['properties'].copy()
            row['osm_id'] = feature['properties'].get('osm_id')
            row['osm_type'] = feature['properties'].get('osm_type')
            row['longitude'] = feature['geometry']['coordinates'][0]
            row['latitude'] = feature['geometry']['coordinates'][1]
            
            writer.writerow(row)
            
    print(f"Successfully converted {len(features)} schools to {output_file}")

if __name__ == "__main__":
    geojson_to_csv('schools_drc.geojson', 'DRC_All_SCHool.csv')
