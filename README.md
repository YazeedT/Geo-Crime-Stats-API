# Geo Crime Stats API

The Geo Crime Stats API provides comprehensive crime statistics for any given ZIP code in the United States. It does this by utilizing the `nominatim.openstreetmap.org` and `crimeometer.com` APIs to fetch geographical coordinates and crime data respectively. The reported crime data is for a 6 month period.

## API Endpoint

- **Endpoint:** `URL/get-csi?zipcode=YOUR_ZIP_CODE&distance=DISTANCE_IN_MILES`
REQUIRED: Replace `YOUR_ZIP_CODE` with the actual ZIP code for which you want to get the crime data.
OPTIONAL: Replace `DISTANCE_IN_MILES` with the diameter of the search area from the center of the ZIP code. Defaults to 1 mile.

## JSON Response Structure
The JSON returned by the API endpoint has the following structure:

- `distance`: An integer indicating the data's area radius, measured in miles.
  
- `population_count`: An integer representing the total population of a one-mile radius from the center point of the provided ZIP code.

- `incidents_count`: An integer indicating the total number of reported crime incidents in the specified area over the last 6 months.

- `incidents_types`: An array containing individual incident reports. Each report is a dictionary with three fields:
  - `incident_type`: A string specifying the type of crime incident.
  - `incident_type_count`: An integer indicating the total number of reported incidents of this type in the last 6 months.
  - `incident_type_ratio`: A decimal (percentage) that represents the proportion of this incident type out of all reported incidents.

- `incidents_types_ratio`: A decimal value representing the ratio of the total number of incidents to the population size. This ratio provides a sense of the prevalence of crime incidents relative to the size of the population.

- `csi`: A decimal value between 0-100, with 50 being the US average, that represents the Crime Safety Index for the area. The CSI is calculated based on the number of reported incidents, their types, and the population size. It provides a measure of the overall safety level of the area.
