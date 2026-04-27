import pandas as pd

def clean_conflict_data(file_path):
    print(f"Reading {file_path}...")
    try:
        # 1. Load the data
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please make sure it's in this folder.")
        return

    # 2. Standardize Column Names (The "Cleaning" Part)
    # We convert all column names to lowercase to avoid "Lat" vs "lat" issues
    df.columns = [col.lower().strip() for col in df.columns]
    
    # We create a dictionary of "Old Name": "New Name"
    # This covers common variations used by ACLED and UCDP
    column_mapping = {
        'event_date': 'date',
        'date_start': 'date',
        'event_type': 'conflict_type',
        'type_of_violence': 'conflict_type',
        'best': 'fatalities',      # UCDP uses 'best' for fatality counts
        'lat': 'latitude',
        'lon': 'longitude',
        'long': 'longitude'
    }
    
    # Apply the renaming (errors='ignore' means it won't crash if a name is missing)
    df = df.rename(columns=column_mapping)
    
    # 3. Standardize Country Names
    # Some datasets use "DRC", others use the full formal name. 
    # We convert them all to one standard: "DR Congo"
    drc_aliases = [
        'dr congo', 'drc', 'democratic republic of congo', 
        'congo, democratic republic of the', 'congo-kinshasa'
    ]
    
    # We find every variation and rename them to "DR Congo"
    # We use .str.lower() so it doesn't matter if it's "drc" or "DRC"
    df.loc[df['country'].str.lower().isin(drc_aliases), 'country'] = 'DR Congo'
    
    # 4. Filter for only DR Congo
    filtered_df = df[df['country'] == 'DR Congo'].copy()
    
    # 5. Save the cleaned file
    output_name = 'cleaned_drc_conflict_data.csv'
    filtered_df.to_csv(output_name, index=False)
    
    print(f"--- SUCCESS ---")
    print(f"Cleaned file saved as: {output_name}")
    print(f"Total DRC events found: {len(filtered_df)}")
    print(f"Standardized columns: {list(filtered_df.columns)}")

if __name__ == "__main__":
    clean_conflict_data('conflict_event.csv')
