from neo4j import GraphDatabase
import csv
import os

# ============= Read Configuration =================

def read_config(config_file='config.txt'):
    """Read Neo4j configuration from config file"""
    config = {}
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, config_file)
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:
                key, value = line.split('=', 1)
                config[key] = value
    return config

# ============= Load CSV =================

def load_csv(filename):
    """Load a CSV file and return list of dictionaries"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

# ============= Configuration =================

config = read_config()
uri = config['URI']
user = config['USERNAME']
password = config['PASSWORD']
driver = GraphDatabase.driver(uri, auth=(user, password))
print("Connected to Neo4j database")

# ============= Data Loading =================

hotels = load_csv('Dataset/hotels.csv')
users = load_csv('Dataset/users.csv')
reviews = load_csv('Dataset/reviews.csv')
visas = load_csv('Dataset/visa.csv')

print(f"Loaded {len(hotels)} hotels, {len(users)} users, {len(reviews)} reviews, {len(visas)} visa records")

# ============= Knowledge Graph =================

session = driver.session()
session.run("MATCH (n) DETACH DELETE n")
print("Database cleared")

# ============= Nodes =================

# Country
countries = set()
for hotel in hotels:
    countries.add(hotel['country'])
for user in users:
    countries.add(user['country'])

for country in countries:
    session.run("CREATE (c:Country {name: $name})", name=country)
print(f"Created {len(countries)} Country nodes")

# City
cities = {}
for hotel in hotels:
    city_name = hotel['city']
    country_name = hotel['country']
    if city_name not in cities:
        cities[city_name] = country_name

for city_name in cities.keys():
    session.run("CREATE (city:City {name: $city_name})", city_name=city_name)
print(f"Created {len(cities)} City nodes")

# Traveller
for user in users:
    session.run("""
        CREATE (t:Traveller {
            user_id: $user_id,
            age: $age,
            type: $type,
            gender: $gender
        })
    """,
        user_id=user['user_id'],
        age=user['age_group'],
        type=user['traveller_type'],
        gender=user['user_gender']
    )
print(f"Created {len(users)} Traveller nodes")

# Hotel - UPDATED: Added location_base, staff_base, value_for_money_base
hotel_avg_scores = {}
for review in reviews:
    hotel_id = review['hotel_id']
    score = float(review['score_overall'])
    if hotel_id not in hotel_avg_scores:
        hotel_avg_scores[hotel_id] = []
    hotel_avg_scores[hotel_id].append(score)

for hotel_id in hotel_avg_scores:
    avg = sum(hotel_avg_scores[hotel_id]) / len(hotel_avg_scores[hotel_id])
    hotel_avg_scores[hotel_id] = round(avg, 2)

for hotel in hotels:
    hotel_id = hotel['hotel_id']
    avg_score = hotel_avg_scores.get(hotel_id, 0.0)

    session.run("""
        CREATE (h:Hotel {
            hotel_id: $hotel_id,
            name: $name,
            star_rating: $star_rating,
            cleanliness_base: $cleanliness_base,
            comfort_base: $comfort_base,
            facilities_base: $facilities_base,
            location_base: $location_base,
            staff_base: $staff_base,
            value_for_money_base: $value_for_money_base,
            average_reviews_score: $average_reviews_score
        })
    """,
        hotel_id=hotel_id,
        name=hotel['hotel_name'],
        star_rating=float(hotel['star_rating']),
        cleanliness_base=float(hotel['cleanliness_base']),
        comfort_base=float(hotel['comfort_base']),
        facilities_base=float(hotel['facilities_base']),
        location_base=float(hotel['location_base']),
        staff_base=float(hotel['staff_base']),
        value_for_money_base=float(hotel['value_for_money_base']),
        average_reviews_score=avg_score
    )
print(f"Created {len(hotels)} Hotel nodes with all 6 base aspect scores")

# Review
print("Creating Review nodes...")
batch_size = 5000
for i in range(0, len(reviews), batch_size):
    batch = reviews[i:i+batch_size]
    batch_data = []
    for review in batch:
        batch_data.append({
            'review_id': review['review_id'],
            'text': review['review_text'],
            'date': review['review_date'],
            'score_overall': float(review['score_overall']),
            'score_cleanliness': float(review['score_cleanliness']),
            'score_comfort': float(review['score_comfort']),
            'score_facilities': float(review['score_facilities']),
            'score_location': float(review['score_location']),
            'score_staff': float(review['score_staff']),
            'score_value_for_money': float(review['score_value_for_money'])
        })

    session.run("""
        UNWIND $batch as row
        CREATE (r:Review {
            review_id: row.review_id,
            text: row.text,
            date: row.date,
            score_overall: row.score_overall,
            score_cleanliness: row.score_cleanliness,
            score_comfort: row.score_comfort,
            score_facilities: row.score_facilities,
            score_location: row.score_location,
            score_staff: row.score_staff,
            score_value_for_money: row.score_value_for_money
        })
    """, batch=batch_data)

    print(f"  Processed {min(i+batch_size, len(reviews))}/{len(reviews)} reviews")

# ============= Relationships =================

# Create indexes for faster lookups
session.run("CREATE INDEX traveller_user_id IF NOT EXISTS FOR (t:Traveller) ON (t.user_id)")
session.run("CREATE INDEX hotel_hotel_id IF NOT EXISTS FOR (h:Hotel) ON (h.hotel_id)")
session.run("CREATE INDEX review_review_id IF NOT EXISTS FOR (r:Review) ON (r.review_id)")
session.run("CREATE INDEX city_name IF NOT EXISTS FOR (c:City) ON (c.name)")
session.run("CREATE INDEX country_name IF NOT EXISTS FOR (c:Country) ON (c.name)")
print("Created indexes for faster relationship creation")

# (City)-[:LOCATED_IN]->(Country)
for city_name, country_name in cities.items():
    session.run("""
        MATCH (city:City {name: $city_name})
        MATCH (country:Country {name: $country_name})
        CREATE (city)-[:LOCATED_IN]->(country)
    """, city_name=city_name, country_name=country_name)
print(f"Created {len(cities)} LOCATED_IN relationships (City->Country)")

# (Traveller)-[:FROM_COUNTRY]->(Country)
for user in users:
    session.run("""
        MATCH (t:Traveller {user_id: $user_id})
        MATCH (country:Country {name: $country})
        CREATE (t)-[:FROM_COUNTRY]->(country)
    """,
        user_id=user['user_id'],
        country=user['country']
    )
print(f"Created {len(users)} FROM_COUNTRY relationships")

# (Hotel)-[:LOCATED_IN]->(City)
for hotel in hotels:
    session.run("""
        MATCH (h:Hotel {hotel_id: $hotel_id})
        MATCH (city:City {name: $city})
        CREATE (h)-[:LOCATED_IN]->(city)
    """,
        hotel_id=hotel['hotel_id'],
        city=hotel['city']
    )
print(f"Created {len(hotels)} LOCATED_IN relationships (Hotel->City)")

# (Traveller)-[:WROTE]->(Review), (Review)-[:REVIEWED]->(Hotel)
# REMOVED: (Traveller)-[:STAYED_AT]->(Hotel) - redundant relationship
print("Creating Review relationships...")
batch_size = 5000
for i in range(0, len(reviews), batch_size):
    batch = reviews[i:i+batch_size]
    batch_data = []
    for review in batch:
        batch_data.append({
            'review_id': review['review_id'],
            'user_id': review['user_id'],
            'hotel_id': review['hotel_id']
        })

    session.run("""
        UNWIND $batch as row
        MATCH (t:Traveller {user_id: row.user_id})
        MATCH (r:Review {review_id: row.review_id})
        MATCH (h:Hotel {hotel_id: row.hotel_id})
        CREATE (t)-[:WROTE]->(r)
        CREATE (r)-[:REVIEWED]->(h)
    """, batch=batch_data)

    print(f"  Processed {min(i+batch_size, len(reviews))}/{len(reviews)} review relationships")

# (Country)-[:NEEDS_VISA]->(Country)
visa_count = 0
for visa in visas:
    if visa['requires_visa'].lower() == 'yes':
        session.run("""
            MATCH (from:Country {name: $from_country})
            MATCH (to:Country {name: $to_country})
            CREATE (from)-[:NEEDS_VISA {visa_type: $visa_type}]->(to)
        """,
            from_country=visa['from'],
            to_country=visa['to'],
            visa_type=visa['visa_type']
        )
        visa_count += 1
print(f"Created {visa_count} NEEDS_VISA relationships")

session.close()
driver.close()

print("\n" + "=" * 60)
print("Knowledge Graph created successfully for Milestone 3!")
print("=" * 60)
print("\nUpdates from Milestone 2:")
print("  [+] Added location_base, staff_base, value_for_money_base to Hotel nodes")
print("  [-] Removed redundant STAYED_AT relationship")
print("\nAll 6 aspect scores now available:")
print("  - Base scores (from Hotel node)")
print("  - Review scores (from Review aggregation)")
print("=" * 60)
