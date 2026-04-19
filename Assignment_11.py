def parse_nmea(sentence):
    parts = sentence.split(',')
    
    if sentence.startswith('$GPGGA'):
        # GPGGA index 9 is Altitude, index 1 is Time (HHMMSS)
        if len(parts) > 9 and parts[9]:
            time_raw = parts[1]
            time_formatted = f"{time_raw[0:2]}:{time_raw[2:4]}:{time_raw[4:6]}"
            altitude = parts[9]
            print(f"Time (UTC): {time_formatted}, Elevation: {altitude} meters")
            
    elif sentence.startswith('$GPRMC'):
        # GPRMC index 7 is Speed in knots, index 9 is Date (DDMMYY)
        if len(parts) > 9 and parts[7] and parts[9]:
            speed_knots = float(parts[7])
            speed_kmh = speed_knots * 1.852 # Convert to km/h
            date_raw = parts[9]
            date_formatted = f"20{date_raw[4:6]}-{date_raw[2:4]}-{date_raw[0:2]}"
            print(f"Date: {date_formatted}, Speed: {speed_kmh:.2f} km/h")

# Test with standard NMEA sentences
if __name__ == "__main__":
    parse_nmea("$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47")
    parse_nmea("$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A")