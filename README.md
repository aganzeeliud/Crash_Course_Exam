# DRC Conflict & Schools Analysis

This project analyzes the proximity of schools in the Democratic Republic of the Congo to known conflict events.

## 🌍 Live Map
You can view the interactive map here:
**[https://aganzeeliud.github.io/Crash_Course_Exam/](https://aganzeeliud.github.io/Crash_Course_Exam/)**

## 📊 Features
- **Map View**: Interactive Leaflet map showing schools that are located near conflict events.
- **Data Analysis**: 
  - **At-Risk Schools**: Schools within 10km of a conflict event.
  - **Safe Schools**: Schools further than 10km from conflict events.
- **Data Sources**:
  - Schools: Fetched from OpenStreetMap via Overpass API.
  - Conflicts: Provided via CSV.

## 📁 Project Structure
- `/data`: Contains the processed CSV and GeoJSON datasets.
- `/scripts`: Python scripts used for data fetching, conversion, and risk analysis.
- `index.html` & `map.js`: The code for the interactive web map.

## 🛠 Tools Used
- **Python**: For data processing and Haversine distance calculations.
- **Leaflet.js**: For the interactive mapping interface.
- **GitHub Pages**: For hosting the live analysis.
