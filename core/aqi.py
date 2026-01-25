"""
Logic for calculating Air Quality Index (AQI) based on EPA (and potentially WHO) standards.
This is a pure Python module independent of Django.
"""

def calculate_aqi_epa(p_conc, p_type):
    """
    Calculates AQI for a given pollutant concentration and type using EPA standard.
    
    Formula: I = ((I_high - I_low) / (C_high - C_low)) * (C - C_low) + I_low
    
    p_type should be one of: 'pm25', 'pm10', 'co', 'no2', 'so2', 'o3'
    """
    
    breakpoints = {
        'pm25': [
            (0.0, 12.0, 0, 50),
            (12.1, 35.4, 51, 100),
            (35.5, 55.4, 101, 150),
            (55.5, 150.4, 151, 200),
            (150.5, 250.4, 201, 300),
            (250.5, 350.4, 301, 400),
            (350.5, 500.4, 401, 500)
        ],
        'pm10': [
            (0, 54, 0, 50),
            (55, 154, 51, 100),
            (155, 254, 101, 150),
            (255, 354, 151, 200),
            (355, 424, 201, 300),
            (425, 504, 301, 400),
            (505, 604, 401, 500)
        ],
        'co': [
            (0.0, 4.4, 0, 50),
            (4.5, 9.4, 51, 100),
            (9.5, 12.4, 101, 150),
            (12.5, 15.4, 151, 200),
            (15.4, 30.4, 201, 300),
            (30.5, 40.4, 301, 400),
            (40.5, 50.4, 401, 500)
        ]
        # Add other pollutants as needed
    }
    
    if p_type not in breakpoints:
        return None
    
    for (c_low, c_high, i_low, i_high) in breakpoints[p_type]:
        if c_low <= p_conc <= c_high:
            aqi = ((i_high - i_low) / (c_high - c_low)) * (p_conc - c_low) + i_low
            return round(aqi)
            
    return None

def get_aqi_category(aqi):
    """Returns the human-readable category for a given AQI value."""
    if aqi is None: return "Inconnu"
    if 0 <= aqi <= 50: return "Bon"
    if 51 <= aqi <= 100: return "Modéré"
    if 101 <= aqi <= 150: return "Mauvais pour les groupes sensibles"
    if 151 <= aqi <= 200: return "Mauvais"
    if 201 <= aqi <= 300: return "Très mauvais"
    return "Dangereux"

def calculate_global_aqi(measurements):
    """
    Given a dict of measurements {'pm25': x, 'pm10': y, ...},
    returns the highest AQI value among them.
    """
    aqis = []
    for p_type, p_conc in measurements.items():
        if p_conc is not None:
            aqi = calculate_aqi_epa(p_conc, p_type)
            if aqi is not None:
                aqis.append(aqi)
                
    return max(aqis) if aqis else None
