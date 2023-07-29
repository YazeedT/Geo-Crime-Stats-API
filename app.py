import requests
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/get-crime-data', methods=['GET'])
def get_crime_data():
    # Extract the value of 'zipcode' from the URL
    ZIP_CODE                    = request.args.get('zipcode', type = str)
    
    # Extract the value of 'distance' from the URL, convert it to meters for the API. Defaults to 1 mile.
    DISTANCE_MILES              = request.args.get('distance', default = 1, type = int)
    DISTANCE                    = str(DISTANCE_MILES) + "mi"
    
    # API endpoints and key
    OPENSTREET_API_ENDPOINT     = f'http://nominatim.openstreetmap.org/search?format=json&postalcode={ZIP_CODE}&country=us'
    CRIMEOMETER_API_ENDPOINT    = 'https://api.crimeometer.com/v2/incidents/stats'
    CRIMEOMETER_API_KEY         = 'mAeNM6nfZj9lFn3rD3eqc9MeohmAGWDE6FYxwgbn'

    # Error handling for missing ZIP code
    if not ZIP_CODE:
        return jsonify(error='A ZIP code must be provided.'), 400

    # Get coordinates from ZIP code
    response = requests.get(OPENSTREET_API_ENDPOINT)
    # Check if the HTTP request to the API endpoint was successful or not
    response.raise_for_status()
    # Save response in a variable
    data = response.json()

    # Error handling for missing response
    if not data:
        return jsonify(error='Could not find coordinates for the given ZIP code.'), 404

    # Save coordinates in variables
    lat = data[0]['lat']
    lon = data[0]['lon']
    
    # Get the time now and 6 months ago
    datetime_end = datetime.now()
    datetime_ini = datetime_end - timedelta(days=180)

    # Use the coordinates and time to get the CSI
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': CRIMEOMETER_API_KEY
    }
    params = {
        'lat': lat,
        'lon': lon,
        'datetime_ini': datetime_ini.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z',
        'datetime_end': datetime_end.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z',
        'distance': DISTANCE
    }
    
    response = requests.get(CRIMEOMETER_API_ENDPOINT, headers=headers, params=params)
    response.raise_for_status()
    results = response.json()
    
    # Check if there is data for this ZIP code
    csi = results.get('csi')
    count = results.get('incidents_count')
    if csi == 0 and count == 0:
        return jsonify(error='There is no data for this ZIP code.'), 404

    # Add distance to results
    results['distance'] = DISTANCE_MILES
    return results

if __name__ == '__main__':
    app.run(debug=True)
