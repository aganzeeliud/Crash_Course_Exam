import requests
import json

def fetch_drc_schools():
    # 1. The Overpass Query
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

    url = "https://overpass-api.de/api/interpreter"
    
    print("Connecting to Overpass API to fetch DRC schools...")
    try:
        response = requests.get(url, params={'data': overpass_query}, timeout=200)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # 2. Convert to GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for element in data.get('elements', []):
        # Overpass returns 'lat'/'lon' for nodes, or 'center' for ways/relations
        lat = element.get('lat') or element.get('center', {}).get('lat')
        lon = element.get('lon') or element.get('center', {}).get('lon')

        if lat and lon:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat] # GeoJSON uses [Lon, Lat]
                },
                "properties": {
                    "name": element.get('tags', {}).get('name', 'Unnamed School'),
                    "type": element.get('tags', {}).get('amenity', 'school'),
                    "osm_id": element.get('id')
                }
            }
            geojson["features"].append(feature)

    # 3. Save to file
    with open('drc_schools.geojson', 'w') as f:
        json.dump(geojson, f, indent=2)

    print(f"Success! {len(geojson['features'])} schools saved to drc_schools.geojson")

if __name__ == "__main__":
    fetch_drc_schools()
