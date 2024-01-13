import requests
import geocoder

def get_my_ip_and_location():
    # Get public IP address
    response = requests.get('https://api.ipify.org?format=json')
    ip = response.json()['ip']

    # Get location
    g = geocoder.ip(ip)
    location = g.latlng

    return ip, location

# Test the function
ip, location = get_my_ip_and_location()
print(f'IP: {ip}\nLocation: {location}')
