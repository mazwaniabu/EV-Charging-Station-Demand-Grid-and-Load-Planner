import math

# Centroids of Malaysian states for coordinate-based geocoding
STATE_CENTROIDS = {
    'W.P. Kuala Lumpur': (3.1390, 101.6869),
    'Selangor': (3.0738, 101.5183),
    'Johor': (1.4854, 103.7618),
    'Pulau Pinang': (5.4141, 100.3292),
    'Perak': (4.5921, 101.0901),
    'Kedah': (6.1254, 100.3673),
    'Perlis': (6.4449, 100.2048),
    'Negeri Sembilan': (2.7258, 101.9422),
    'Melaka': (2.1896, 102.2501),
    'Pahang': (3.8077, 103.3268),
    'Kelantan': (6.1254, 102.2381),
    'Terengganu': (5.3117, 103.1324),
    'Sabah': (5.9788, 116.0753),
    'Sarawak': (1.5533, 110.3592)
}

# Standardized state names mapping for existing names
STATE_NAME_MAPPING = {
    'kuala lumpur': 'W.P. Kuala Lumpur',
    'wilayah persekutuan kuala lumpur': 'W.P. Kuala Lumpur',
    'w.p. kuala lumpur': 'W.P. Kuala Lumpur',
    'wilayah persekutuan': 'W.P. Kuala Lumpur',
    'putrajaya': 'W.P. Kuala Lumpur',
    'wilayah persekutuan putrajaya': 'W.P. Kuala Lumpur',
    'selangor': 'Selangor',
    'selangor darul ehsan': 'Selangor',
    'johor': 'Johor',
    'johor darul ta\'zim': 'Johor',
    'pulau pinang': 'Pulau Pinang',
    'penang': 'Pulau Pinang',
    'perak': 'Perak',
    'kedah': 'Kedah',
    'perlis': 'Perlis',
    'negeri sembilan': 'Negeri Sembilan',
    'melaka': 'Melaka',
    'malacca': 'Melaka',
    'malaka': 'Melaka',
    'pahang': 'Pahang',
    'kelantan': 'Kelantan',
    'terengganu': 'Terengganu',
    'sabah': 'Sabah',
    'sarawak': 'Sarawak',
    'malaysia': 'Selangor' # Default fallback if raw state is generic country string
}

# City-to-state mapping
CITY_TO_STATE = {
    'kuala lumpur': 'W.P. Kuala Lumpur',
    'cheras': 'W.P. Kuala Lumpur',
    'mont kiara': 'W.P. Kuala Lumpur',
    'segambut': 'W.P. Kuala Lumpur',
    'ampang': 'W.P. Kuala Lumpur',
    'setapak': 'W.P. Kuala Lumpur',
    'kepong': 'W.P. Kuala Lumpur',
    'sentul': 'W.P. Kuala Lumpur',
    'keramat': 'W.P. Kuala Lumpur',
    'bangsar': 'W.P. Kuala Lumpur',
    'titiwangsa': 'W.P. Kuala Lumpur',
    'jln tun razak': 'W.P. Kuala Lumpur',
    'jln ampang': 'W.P. Kuala Lumpur',
    'bukit damansara a': 'W.P. Kuala Lumpur',
    'petaling jaya': 'Selangor',
    'shah alam': 'Selangor',
    'puchong': 'Selangor',
    'subang jaya': 'Selangor',
    'subang': 'Selangor',
    'kajang': 'Selangor',
    'seri kembangan': 'Selangor',
    'klang': 'Selangor',
    'cyberjaya': 'Selangor',
    'bangi': 'Selangor',
    'rawang': 'Selangor',
    'semenyih': 'Selangor',
    'gombak': 'Selangor',
    'damansara': 'Selangor',
    'sepang': 'Selangor',
    'bandar baru bangi': 'Selangor',
    'johor bahru': 'Johor',
    'iskandar puteri': 'Johor',
    'muar': 'Johor',
    'batu pahat': 'Johor',
    'skudai': 'Johor',
    'senai': 'Johor',
    'kluang': 'Johor',
    'pontian': 'Johor',
    'pasir gudang': 'Johor',
    'george town': 'Pulau Pinang',
    'georgetown': 'Pulau Pinang',
    'bayan lepas': 'Pulau Pinang',
    'jelutong': 'Pulau Pinang',
    'tanjung tokong': 'Pulau Pinang',
    'butterworth': 'Pulau Pinang',
    'perai': 'Pulau Pinang',
    'bukit mertajam': 'Pulau Pinang',
    'seberang perai': 'Pulau Pinang',
    'batu ferringhi': 'Pulau Pinang',
    'tanjung bungah': 'Pulau Pinang',
    'penang hill': 'Pulau Pinang',
    'bedong': 'Kedah',
    'ipoh': 'Perak',
    'taiping': 'Perak',
    'teluk intan': 'Perak',
    'kampar': 'Perak',
    'alor setar': 'Kedah',
    'sungai petani': 'Kedah',
    'kulim': 'Kedah',
    'langkawi': 'Kedah',
    'kangar': 'Perlis',
    'seremban': 'Negeri Sembilan',
    'nilai': 'Negeri Sembilan',
    'port dickson': 'Negeri Sembilan',
    'melaka': 'Melaka',
    'malacca': 'Melaka',
    'alor gajah': 'Melaka',
    'jasin': 'Melaka',
    'kuantan': 'Pahang',
    'temerloh': 'Pahang',
    'bentong': 'Pahang',
    'kota bharu': 'Kelantan',
    'kubang kerian': 'Kelantan',
    'kuala terengganu': 'Terengganu',
    'kemaman': 'Terengganu',
    'dungun': 'Terengganu',
    'kota kinabalu': 'Sabah',
    'penampang': 'Sabah',
    'sandakan': 'Sabah',
    'tawau': 'Sabah',
    'kuching': 'Sarawak',
    'miri': 'Sarawak',
    'sibu': 'Sarawak',
    'bintulu': 'Sarawak'
}

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculates simple Euclidean distance (sufficient for local state resolution)."""
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

def geocode_coordinate_to_state(lat, lon, city_name=None, raw_state=None):
    """
    Reverse geocodes coordinate + city + state to the standardized Malaysian state.
    """
    # 1. Clean raw state if valid and recognized
    if raw_state:
        clean_rs = str(raw_state).strip().lower()
        if clean_rs in STATE_NAME_MAPPING:
            return STATE_NAME_MAPPING[clean_rs]
            
    # 2. Check city mapping
    if city_name:
        clean_city = str(city_name).strip().lower()
        if clean_city in CITY_TO_STATE:
            return CITY_TO_STATE[clean_city]
            
    # 3. Fallback: Distance-based geocoding
    # Distinguish East vs West Malaysia first using longitude
    is_east_malaysia = lon > 109.0
    
    min_dist = float('inf')
    best_state = 'Selangor'  # Default fallback state
    
    for state, centroid in STATE_CENTROIDS.items():
        state_lon = centroid[1]
        state_is_east = state_lon > 109.0
        
        # Keep comparison within East/West boundary
        if is_east_malaysia == state_is_east:
            dist = calculate_distance(lat, lon, centroid[0], centroid[1])
            if dist < min_dist:
                min_dist = dist
                best_state = state
                
    return best_state
