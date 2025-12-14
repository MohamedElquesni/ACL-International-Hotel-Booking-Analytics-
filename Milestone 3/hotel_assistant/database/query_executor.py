"""Query Execution Logic"""
from typing import Dict, Any, List
from .neo4j_connection import Neo4jConnection
from .query_library import QueryLibrary

class Neo4jConnection:
    def __init__(self, config_path=None):
        if config_path is None:
            possible_paths = [
                os.path.join('KnowledgeGraph', 'config.txt'),
                os.path.join('Milestone 3', 'KnowledgeGraph', 'config.txt'),
            ]
            config_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    config_path = path
                    break
        
        config = {}
        with open(config_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    config[key] = value
        
        self.driver = GraphDatabase.driver(config['URI'], auth=(config['USERNAME'], config['PASSWORD']))
    
    def execute_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [dict(record) for record in result]
    
    def close(self):
        self.driver.close()

print("Neo4jConnection class defined")

def select_and_execute_query(conn: Neo4jConnection, intent: str, entities: Dict[str, Any]):
    if intent == "LIST_HOTELS":
        city, country, star_rating = entities.get('city'), entities.get('country'), entities.get('star_rating')
        if city and star_rating:
            return QueryLibrary.template_L4_list_by_city_and_rating(conn, city, star_rating)
        elif country and star_rating:
            return QueryLibrary.template_L5_list_by_country_and_rating(conn, country, star_rating)
        elif city:
            return QueryLibrary.template_L1_list_by_city(conn, city)
        elif country:
            return QueryLibrary.template_L2_list_by_country(conn, country)
        elif star_rating:
            return QueryLibrary.template_L3_list_by_rating(conn, star_rating)
    
    elif intent == "RECOMMEND_HOTEL":
        city = entities.get('city')
        traveller_type = entities.get('traveller_type')
        aspects = entities.get('aspects')
        star_rating = entities.get('star_rating')
        age_group = entities.get('age_group')
        user_gender = entities.get('user_gender')
        
        if city:
            if traveller_type and aspects:
                return QueryLibrary.template_R4_recommend_by_traveller_and_aspects(
                    conn, city, traveller_type, aspects, age_group, user_gender, star_rating)
            elif aspects:
                return QueryLibrary.template_R3_recommend_by_aspects(
                    conn, city, aspects, age_group, user_gender, star_rating)
            elif star_rating and traveller_type:
                return QueryLibrary.template_R1_recommend_by_location(conn, city, star_rating)
            elif star_rating:
                return QueryLibrary.template_R5_recommend_with_rating_filter(conn, city, star_rating)
            elif traveller_type:
                return QueryLibrary.template_R1_recommend_by_location(conn, city)
            else:
                return QueryLibrary.template_R1_recommend_by_location(conn, city)
    
    elif intent == "DESCRIBE_HOTEL":
        hotel_name, aspects = entities.get('hotel_name'), entities.get('aspects')
        if hotel_name:
            return QueryLibrary.template_D2_describe_specific_aspects(conn, hotel_name, aspects) if aspects else QueryLibrary.template_D1_describe_all_aspects(conn, hotel_name)
    
    elif intent == "COMPARE_HOTELS":
        hotel1, hotel2, traveller_type, aspects = entities.get('hotel1'), entities.get('hotel2'), entities.get('traveller_type'), entities.get('aspects')
        if hotel1 and hotel2:
            return QueryLibrary.template_C2_compare_with_traveller_type(conn, hotel1, hotel2, traveller_type, aspects) if traveller_type else QueryLibrary.template_C1_compare_all_aspects(conn, hotel1, hotel2, aspects)
    
    elif intent == "CHECK_VISA":
        from_country, to_country = entities.get('from_country'), entities.get('to_country')
        if from_country and to_country:
            return QueryLibrary.template_V1_check_visa_requirement(conn, from_country, to_country)
    
    return []

print("Query selector defined")