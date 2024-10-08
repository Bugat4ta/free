import numpy as np

def geo_to_eci(latitude, longitude):
    """Convert geographic coordinates to ECI coordinates."""
    lat_rad = np.radians(latitude)
    lon_rad = np.radians(longitude)
    R = 6371e3  
    x = R * np.cos(lat_rad) * np.cos(lon_rad)
    y = R * np.cos(lat_rad) * np.sin(lon_rad)
    z = R * np.sin(lat_rad)
    return np.array([x, y, z])

def compute_position(inclination, raan, eccentricity, arg_perigee, mean_anomaly):
    """Compute the ECI position of a satellite based on its orbital elements."""
    G = 6.67430e-11
    M_earth = 5.972e24  
    inclination = np.radians(inclination)
    raan = np.radians(raan)
    arg_perigee = np.radians(arg_perigee)
    
    n = (2 * np.pi) / 5400 
    a = (G * M_earth / (n ** 2)) ** (1/3) 
    
    M = np.radians(mean_anomaly)
    r = a * (1 - eccentricity ** 2) / (1 + eccentricity * np.cos(M))
    
    x_orbit = r * np.cos(M)
    y_orbit = r * np.sin(M)
    
    position_eci = np.array([
        x_orbit * (np.cos(raan) * np.cos(arg_perigee) - np.sin(raan) * np.sin(arg_perigee) * np.cos(inclination)),
        y_orbit * (np.sin(raan) * np.cos(arg_perigee) + np.cos(raan) * np.sin(arg_perigee) * np.cos(inclination)),
        y_orbit * (np.sin(arg_perigee) * np.sin(inclination))
    ])
    
    return position_eci

def calculate_mean_anomaly(longitude):
    """Calculate a simple approximation of mean anomaly based on longitude."""
    return longitude % 360 

def calculate_distance_and_time(inclination, raan, eccentricity, arg_perigee, M1, M2):
    """Calculate distance and time difference between two satellite positions."""
    position1 = compute_position(inclination, raan, eccentricity, arg_perigee, M1)
    position2 = compute_position(inclination, raan, eccentricity, arg_perigee, M2)
    
    distance = np.linalg.norm(position2 - position1)
    
    n = (2 * np.pi) / 5400
    M1_rad = np.radians(M1)
    M2_rad = np.radians(M2)
    
    time_difference = (M2_rad - M1_rad) / n
    if time_difference < 0:
        time_difference += (2 * np.pi) / n
    
    return distance, time_difference

latitude_1 = float(input("Enter the latitude for point 1 (degrees): "))
longitude_1 = float(input("Enter the longitude for point 1 (degrees): "))
latitude_2 = float(input("Enter the latitude for point 2 (degrees): "))
longitude_2 = float(input("Enter the longitude for point 2 (degrees): "))

M1 = calculate_mean_anomaly(longitude_1)
M2 = calculate_mean_anomaly(longitude_2)

inclination = float(input("Enter the satellite's inclination (degrees): "))
raan = float(input("Enter the RAAN (degrees): "))
eccentricity = float(input("Enter the satellite's eccentricity: "))
arg_perigee = float(input("Enter the argument of perigee (degrees): "))

distance, time_difference = calculate_distance_and_time(inclination, raan, eccentricity, arg_perigee, M1, M2)

print("------------------------------------------------------------------")

print(f"Coordinates 1 Mean Anomaly (M1): {M1:.2f} degrees")
print(f"Coordinates 2 Mean Anomaly (M2): {M2:.2f} degrees")
print(f"ECI Distance between points: {distance:.2f} meters")
print(f"Time to move from M1 to M2: {time_difference:.2f} seconds")
