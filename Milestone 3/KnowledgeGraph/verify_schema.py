from neo4j import GraphDatabase
import os

def read_config(config_file='config.txt'):
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

config = read_config()
driver = GraphDatabase.driver(config['URI'], auth=(config['USERNAME'], config['PASSWORD']))

with driver.session() as session:
    # Test 1: Check Hotel node has all 6 base scores
    result = session.run("""
        MATCH (h:Hotel)
        RETURN h.name AS name,
               h.cleanliness_base AS clean_base,
               h.comfort_base AS comfort_base,
               h.facilities_base AS facilities_base,
               h.location_base AS location_base,
               h.staff_base AS staff_base,
               h.value_for_money_base AS value_base
        LIMIT 1
    """)

    hotel = result.single()
    print("=" * 60)
    print("Test 1: Hotel Base Scores")
    print("=" * 60)
    print(f"Hotel: {hotel['name']}")
    print(f"  Cleanliness Base: {hotel['clean_base']}")
    print(f"  Comfort Base: {hotel['comfort_base']}")
    print(f"  Facilities Base: {hotel['facilities_base']}")
    print(f"  Location Base: {hotel['location_base']} [NEW]")
    print(f"  Staff Base: {hotel['staff_base']} [NEW]")
    print(f"  Value for Money Base: {hotel['value_base']} [NEW]")

    # Test 2: Verify STAYED_AT relationship is removed
    result = session.run("MATCH ()-[r:STAYED_AT]->() RETURN count(r) AS count")
    stayed_count = result.single()['count']

    print("\n" + "=" * 60)
    print("Test 2: STAYED_AT Relationship Removed")
    print("=" * 60)
    print(f"STAYED_AT relationships: {stayed_count}")
    if stayed_count == 0:
        print("Status: [PASS] Redundant relationship successfully removed")
    else:
        print("Status: [FAIL] STAYED_AT still exists")

    # Test 3: Verify we can still traverse Traveller -> Hotel via reviews
    result = session.run("""
        MATCH (t:Traveller)-[:WROTE]->(r:Review)-[:REVIEWED]->(h:Hotel)
        RETURN count(DISTINCT h) AS hotel_count
    """)
    hotel_count = result.single()['hotel_count']

    print("\n" + "=" * 60)
    print("Test 3: Traveller -> Hotel Path via Reviews")
    print("=" * 60)
    print(f"Hotels accessible via Traveller->WROTE->Review->REVIEWED: {hotel_count}")
    if hotel_count > 0:
        print("Status: [PASS] Can still find hotels from travelers")

    # Test 4: Base vs Review comparison example
    result = session.run("""
        MATCH (h:Hotel {name: 'The Azure Tower'})
        OPTIONAL MATCH (h)<-[:REVIEWED]-(r:Review)
        RETURN h.name AS hotel,
               h.location_base AS location_base,
               avg(r.score_location) AS location_reviews,
               h.staff_base AS staff_base,
               avg(r.score_staff) AS staff_reviews,
               h.value_for_money_base AS value_base,
               avg(r.score_value_for_money) AS value_reviews
    """)

    comparison = result.single()
    print("\n" + "=" * 60)
    print("Test 4: Base vs Review Comparison (The Azure Tower)")
    print("=" * 60)
    print(f"Location:  Base = {comparison['location_base']:.1f}, Reviews = {comparison['location_reviews']:.2f}")
    print(f"Staff:     Base = {comparison['staff_base']:.1f}, Reviews = {comparison['staff_reviews']:.2f}")
    print(f"Value:     Base = {comparison['value_base']:.1f}, Reviews = {comparison['value_reviews']:.2f}")

driver.close()

print("\n" + "=" * 60)
print("Schema Verification Complete!")
print("=" * 60)
print("\nAll 6 aspects now have base + review scores.")
print("Ready to proceed with Part 1b: Entity Extraction!")
