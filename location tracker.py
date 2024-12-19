import requests
import gps
import platform

# Function to get the public IP address
def get_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        return response.json()["ip"]
    except requests.RequestException:
        return None

# Function to get the geolocation of the IP address
def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        
        if data["status"] == "fail":
            return None
        
        # Return relevant location information
        location = {
            "city": data.get("city"),
            "region": data.get("regionName"),
            "country": data.get("country"),
            "address": data.get("isp")  # You can use ISP or any other available field
        }
        return location
    except requests.RequestException:
        return None

# Function to display the location in human-readable format
def display_location(location, source="IP"):
    if location:
        print(f"\n{source} Location Information:")
        print(f"City: {location['city']}")
        print(f"Region: {location['region']}")
        print(f"Country: {location['country']}")
        print(f"Address: {location['address']}")
    else:
        print(f"Could not retrieve {source} location data.")

# GPS-related code (for devices with GPS modules like Raspberry Pi)
def get_gps_coordinates():
    session = gps.gps(mode=gps.WATCH_ENABLE)  # Watch for GPS data
    try:
        report = session.next()  # Get the next GPS data report
        if report['class'] == 'TPV':
            if hasattr(report, 'lat') and hasattr(report, 'lon'):
                # Returning GPS coordinates (latitude and longitude)
                return {
                    "latitude": report.lat,
                    "longitude": report.lon,
                    "city": "Unknown",
                    "region": "Unknown",
                    "country": "Unknown"
                }
            else:
                return None
    except KeyError:
        return None
    except KeyboardInterrupt:
        quit()

# Main function to run the tracker
def main():
    print("Location Tracker Started...\n")
    
    # Step 1: Try to get the IP-based location
    ip = get_ip()
    if ip:
        print(f"IP Address: {ip}")
        location = get_location(ip)
        display_location(location, source="IP")
    else:
        print("Failed to retrieve IP address.")
    
    # Step 2: Skip GPS-based location if on Windows
    if platform.system() != 'Windows':
        gps_location = get_gps_coordinates()
        if gps_location:
            display_location(gps_location, source="GPS")
        else:
            print("Failed to retrieve GPS data or GPS device not available.")
    else:
        print("GPS tracking is skipped on Windows.")

if __name__ == "__main__":
    main()
