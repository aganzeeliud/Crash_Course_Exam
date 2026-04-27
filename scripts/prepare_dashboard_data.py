import csv
import json
from collections import Counter, defaultdict

def prepare_dashboard_data():
    input_file = 'data/conflict_drc_2000.csv'
    
    events_per_year = Counter()
    severity_per_year = defaultdict(list)
    causes = Counter()
    regions = Counter()
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = row['year']
            fatalities = int(row['fatalities']) if row['fatalities'] else 0
            event_type = row['event_type']
            location = row['location']
            
            events_per_year[year] += 1
            severity_per_year[year].append(fatalities)
            causes[event_type] += 1
            regions[location] += 1
            
    # Sort years
    sorted_years = sorted(events_per_year.keys())
    
    # Calculate average fatalities per year
    avg_severity = [sum(severity_per_year[y])/len(severity_per_year[y]) for y in sorted_years]
    
    dashboard_data = {
        "years": sorted_years,
        "event_counts": [events_per_year[y] for y in sorted_years],
        "avg_severity": avg_severity,
        "causes": {
            "labels": list(causes.keys()),
            "data": list(causes.values())
        },
        "top_regions": {
            "labels": [r[0] for r in regions.most_common(10)],
            "data": [r[1] for r in regions.most_common(10)]
        }
    }
    
    with open('data/dashboard_data.json', 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2)
    
    print("Dashboard data prepared successfully.")

if __name__ == "__main__":
    prepare_dashboard_data()
