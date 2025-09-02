from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def get_location_details(address):
    """
    Fetches location details for a given address using the Nominatim geocoder.

    Args:
        address (str): The address to geocode (e.g., "1600 Amphitheatre Parkway, Mountain View, CA").

    Returns:
        dict: A dictionary containing location details, or None if the request fails.
    """
    geolocator = Nominatim(user_agent="location_fetcher")
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return {
                "address": location.address,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "raw_data": location.raw
            }
        else:
            print(f"Could not find coordinates for: {address}")
            return None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding service error: {e}")
        return None
