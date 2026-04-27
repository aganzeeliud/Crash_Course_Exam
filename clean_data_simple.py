import csv

def clean_conflict_data(input_path, output_path):
    drc_aliases = {'dr congo', 'drc', 'democratic republic of congo', 'congo, democratic republic of the', 'congo-kinshasa'}
    
    with open(input_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        # Standardize fieldnames
        fieldnames = [f.lower().strip() for f in reader.fieldnames]
        
        # Mapping variations to standard names
        mapping = {'lat': 'latitude', 'lon': 'longitude', 'long': 'longitude', 'event_type': 'cause', 'fatalities': 'severity'}
        
        clean_fields = []
        for f in fieldnames:
            clean_fields.append(mapping.get(f, f))
            
        with open(output_path, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=clean_fields)
            writer.writeheader()
            
            for row in reader:
                # Create a new row with lowercase keys
                new_row = {mapping.get(k.lower().strip(), k.lower().strip()): v for k, v in row.items()}
                
                if new_row.get('country', '').lower() in drc_aliases:
                    new_row['country'] = 'DR Congo'
                    writer.writerow(new_row)

if __name__ == "__main__":
    clean_conflict_data('conflict_event.csv', 'cleaned_drc_conflict_data.csv')
    print("Data cleaned successfully using built-in CSV module.")
