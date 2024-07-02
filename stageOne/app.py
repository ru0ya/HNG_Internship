"""
Fetches user location from IP address and based on this
gives weather updates of users location
"""
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
GEO_API_KEY = os.getenv('GEO_API_KEY')


@app.route('/api/hello', methods=['GET'])
def hello():
    """
    Endpoint to greet user and provide weather updates
    of current location
    """
    visitor_name = request.args.get('visitor_name', 'Guest')

    if request.headers.get('X-Forwarded-For'):
        client_ip = request.headers['X-Forwarded-For'].split(',')[0]
    else:
        client_ip = request.remote_addr

    # Get location from IP address using Geoapify
    """
    geoapi_url = f'https://api.geoapify.com/v1/ipinfo?apiKey={GEO_API_KEY}&ip={client_ip}'
    geoapi_response = requests.get(geoapi_url).json()
    location = geoapi_response.get('city', 'unknown location')
    """
    geoip_url = f'http://ip-api.com/json/{client_ip}'
    geoip_response = requests.get(geoip_url).json()
    location = geoip_response.get('city')

    # Get weather data for the location
    weather_url = f"https://api.tomorrow.io/v4/weather/forecast?location=\
            {location}&timesteps=1h&apikey={WEATHER_API_KEY}"
    weather_response = requests.get(weather_url).json()

    if 'timelines' in weather_response and 'hourly' in weather_response['timelines']:
        temperatures = [entry["values"]["temperature"] for entry in\
                weather_response["timelines"]["hourly"]]
        if temperatures:
            temperature = temperatures[0]
        else:
            temperature = "unknown"
    else:
        temperature = "unknown"



    greeting = f"Hello, {visitor_name}!, the temperature is {temperature}\
            degrees Celsius in {location}"

    response = {
            "client_ip": client_ip,
            "location": location,
            "greeting": greeting
            }

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
