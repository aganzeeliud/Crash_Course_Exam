import requests
import json

def fetch_schools_drc():
    # The Overpass API URL
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # The query: 
    # 1. Look for the area named 'République démocratique du Congo'
    # 2. Find all nodes, ways, and relations tagged as 'amenity=school' inside that area
    # 3. 'out center' gives us a single coordinate for each school, even if it's a large area
    overpass_query = """
    [out:json][timeout:180];
    area["name"="République démocratique du Congo"]->.searchArea;
    (
      node["amenity"="school"](area.searchArea);
      way["amenity"="school"](area.searchArea);
      relation["amenity"="school"](area.searchArea);
    );
    out center;
    """
    
    print("Sending query to Overpass API... This might take a minute.")
    headers = {
        'User-Agent': 'GeminiCLI-SchoolFetcher/1.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(overpass_url, data={'data': overpass_query}, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: API returned status code {response.status_code}")
        return
    
    data = response.json()
    
    # Now we convert the OpenStreetMap JSON format to GeoJSON
    # GeoJSON is a standard format for map data that most map tools understand
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for element in data.get('elements', []):
        # Determine the location (latitude and longitude)
        if element['type'] == 'node':
            lon = element['lon']
            lat = element['lat']
        else:
            # For ways and relations, 'out center' puts the coordinates in 'center'
            lon = element['center']['lon']
            lat = element['center']['lat']
            
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": element.get('tags', {})
        }
        # Add some extra info from OSM
        feature["properties"]["osm_id"] = element["id"]
        feature["properties"]["osm_type"] = element["type"]
        
        geojson["features"].append(feature)
    
    # Save the result to a file
    output_filename = "data/schools_drc.geojson"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, indent=2)
        
    print(f"Successfully saved {len(geojson['features'])} schools to {output_filename}")

if __name__ == "__main__":
    fetch_schools_drc()
