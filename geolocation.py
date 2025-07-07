import requests
from decouple import config

def get_my_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Unknown"


def get_client_ip(request):
    # Get client IP from request headers
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_geolocation(ip):
    try:
        response = requests.get(f'https://api.ipinfo.io/lite/{ip}?token={config("IPinfo_Token")}')
        return response.json()
    except requests.RequestException:
        return {}
