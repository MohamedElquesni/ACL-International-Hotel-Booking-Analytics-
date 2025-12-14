"""Cypher Query Templates"""
from typing import List, Dict, Any, Optional
from .neo4j_connection import Neo4jConnection

class QueryLibrary:
    
    @staticmethod
    def template_L1_list_by_city(conn: Neo4jConnection, city: str):
        query = """MATCH (h:Hotel)-[:LOCATED_IN]->(city:City)-[:LOCATED_IN]->(country:Country)
        WHERE city.name = $city RETURN h.name AS hotel_name, city.name AS city_name, country.name AS country_name, h.star_rating AS star_rating
        ORDER BY h.star_rating DESC LIMIT 50"""
        return conn.execute_query(query, {'city': city})
    
    @staticmethod
    def template_L2_list_by_country(conn: Neo4jConnection, country: str):
        query = """MATCH (h:Hotel)-[:LOCATED_IN]->(city:City)-[:LOCATED_IN]->(country:Country)
        WHERE country.name = $country RETURN h.name AS hotel_name, city.name AS city_name, country.name AS country_name, h.star_rating AS star_rating
        ORDER BY h.star_rating DESC LIMIT 50"""
        return conn.execute_query(query, {'country': country})
    
    @staticmethod
    def template_L3_list_by_rating(conn: Neo4jConnection, star_rating: int):
        query = """MATCH (h:Hotel)-[:LOCATED_IN]->(city:City)-[:LOCATED_IN]->(country:Country)
        WHERE h.star_rating = $star_rating RETURN h.name AS hotel_name, city.name AS city_name, country.name AS country_name, h.star_rating AS star_rating
        ORDER BY h.name LIMIT 50"""
        return conn.execute_query(query, {'star_rating': star_rating})
    
    @staticmethod
    def template_L4_list_by_city_and_rating(conn: Neo4jConnection, city: str, star_rating: int):
        query = """MATCH (h:Hotel)-[:LOCATED_IN]->(city:City)-[:LOCATED_IN]->(country:Country)
        WHERE city.name = $city AND h.star_rating = $star_rating 
        RETURN h.name AS hotel_name, city.name AS city_name, country.name AS country_name, h.star_rating AS star_rating LIMIT 50"""
        return conn.execute_query(query, {'city': city, 'star_rating': star_rating})
    
    @staticmethod
    def template_L5_list_by_country_and_rating(conn: Neo4jConnection, country: str, star_rating: int):
        query = """MATCH (h:Hotel)-[:LOCATED_IN]->(city:City)-[:LOCATED_IN]->(country:Country)
        WHERE country.name = $country AND h.star_rating = $star_rating
        RETURN h.name AS hotel_name, city.name AS city_name, country.name AS country_name, h.star_rating AS star_rating LIMIT 50"""
        return conn.execute_query(query, {'country': country, 'star_rating': star_rating})
    
    @staticmethod
    def template_R1_recommend_by_location(conn: Neo4jConnection, city: str, star_rating: int = None):
        where_parts = ["city.name = $city"]
        params = {'city': city}
        if star_rating:
            where_parts.append("h.star_rating = $star_rating")
            params['star_rating'] = star_rating
        where_clause = " AND ".join(where_parts)
        
        query = f"""MATCH (h:Hotel)-[:LOCATED_IN]->(city:City)-[:LOCATED_IN]->(country:Country)
        WHERE {where_clause} OPTIONAL MATCH (h)<-[:REVIEWED]-(r:Review)
        WITH h, city, country, collect(r) AS reviews WHERE size(reviews) > 0 UNWIND reviews AS r
        RETURN h.name AS hotel_name, city.name AS city_name, country.name AS country_name, avg(r.score_overall) AS overall_review_score
        ORDER BY overall_review_score DESC LIMIT 10"""
        return conn.execute_query(query, params)
    
    @staticmethod
    def template_R3_recommend_by_aspects(conn: Neo4jConnection, city: str, aspects: List[str], 
                                        age_group=None, user_gender=None, star_rating: int = None):
        aspect_mapping = {'cleanliness': 'score_cleanliness', 'comfort': 'score_comfort', 'facilities': 'score_facilities',
                         'location': 'score_location', 'staff': 'score_staff', 'value_for_money': 'score_value_for_money'}
        
        valid_aspects = [a for a in (aspects or []) if a in aspect_mapping]
        if not valid_aspects:
            return []
        
        aspect_avg = " + ".join([f"coalesce(avg(r.{aspect_mapping[a]}), 0)" for a in valid_aspects])
        aspect_select = ", ".join([f"avg(r.{aspect_mapping[a]}) AS {a}_review" for a in valid_aspects])
        
        where_parts = ["city.name = $city"]
        params = {'city': city}
        if star_rating:
            where_parts.append("h.star_rating = $star_rating")
            params['star_rating'] = star_rating
        
        demo_conditions = []
        if age_group:
            demo_conditions.append("u.age_group = $age_group")
            params['age_group'] = age_group
        if user_gender:
            demo_conditions.append("u.gender = $user_gender")
            params['user_gender'] = user_gender
        
        where_clause = " AND ".join(where_parts)
        user_match = "<-[:WROTE]-(u:User)" if demo_conditions else ""
        demo_clause = " AND " + " AND ".join(demo_conditions) if demo_conditions else ""
        
        query = f"""MATCH (h:Hotel)-[:LOCATED_IN]->(city:City)-[:LOCATED_IN]->(country:Country)
        WHERE {where_clause} OPTIONAL MATCH (h)<-[:REVIEWED]-(r:Review){user_match} WHERE TRUE{demo_clause}
        WITH h, city, country, collect(r) AS reviews WHERE size(reviews) > 0 UNWIND reviews AS r
        RETURN h.name AS hotel_name, city.name AS city_name, country.name AS country_name, {aspect_select},
        ({aspect_avg}) / {len(valid_aspects)} AS composite_aspect_score, count(r) AS review_count
        ORDER BY composite_aspect_score DESC LIMIT 10"""
        
        return conn.execute_query(query, params)
    
    @staticmethod
    def template_R4_recommend_by_traveller_and_aspects(conn: Neo4jConnection, city: str, traveller_type: str, 
                                                       aspects: List[str], age_group=None, user_gender=None, star_rating: int = None):
        aspect_mapping = {'cleanliness': 'score_cleanliness', 'comfort': 'score_comfort', 'facilities': 'score_facilities',
                         'location': 'score_location', 'staff': 'score_staff', 'value_for_money': 'score_value_for_money'}
        
        valid_aspects = [a for a in (aspects or []) if a in aspect_mapping]
        if not valid_aspects:
            return QueryLibrary.template_R3_recommend_by_aspects(conn, city, aspects, age_group, user_gender, star_rating)
        
        aspect_avg = " + ".join([f"coalesce(avg(r.{aspect_mapping[a]}), 0)" for a in valid_aspects])
        aspect_select = ", ".join([f"avg(r.{aspect_mapping[a]}) AS {a}_review" for a in valid_aspects])
        
        where_parts = ["city.name = $city"]
        params = {'city': city, 'traveller_type': traveller_type}
        if star_rating:
            where_parts.append("h.star_rating = $star_rating")
            params['star_rating'] = star_rating
        where_clause = " AND ".join(where_parts)
        
        conditions = ["t.type = $traveller_type"]
        if age_group:
            conditions.append("u.age_group = $age_group")
            params['age_group'] = age_group
        if user_gender:
            conditions.append("u.gender = $user_gender")
            params['user_gender'] = user_gender
        
        traveller_where = " AND ".join(conditions)
        user_match = "<-[:WROTE]-(u:User)" if (age_group or user_gender) else ""
        
        query = f"""MATCH (h:Hotel)-[:LOCATED_IN]->(city:City)-[:LOCATED_IN]->(country:Country)
        WHERE {where_clause} OPTIONAL MATCH (h)<-[:REVIEWED]-(r:Review)<-[:WROTE]-(t:Traveller){user_match}
        WHERE {traveller_where} WITH h, city, country, collect(r) AS reviews WHERE size(reviews) > 0 UNWIND reviews AS r
        RETURN h.name AS hotel_name, city.name AS city_name, country.name AS country_name, {aspect_select},
        ({aspect_avg}) / {len(valid_aspects)} AS composite_aspect_score, count(r) AS review_count
        ORDER BY composite_aspect_score DESC LIMIT 10"""
        
        results = conn.execute_query(query, params)
        if not results:
            results = QueryLibrary.template_R3_recommend_by_aspects(conn, city, aspects, age_group, user_gender, star_rating)
        return results
    
    @staticmethod
    def template_R5_recommend_with_rating_filter(conn: Neo4jConnection, city: str, star_rating: int):
        query = """MATCH (h:Hotel)-[:LOCATED_IN]->(city:City)-[:LOCATED_IN]->(country:Country)
        WHERE city.name = $city AND h.star_rating = $star_rating OPTIONAL MATCH (h)<-[:REVIEWED]-(r:Review)
        WITH h, city, country, collect(r) AS reviews WHERE size(reviews) > 0 UNWIND reviews AS r
        RETURN h.name AS hotel_name, city.name AS city_name, country.name AS country_name, avg(r.score_overall) AS overall_review_score
        ORDER BY overall_review_score DESC LIMIT 10"""
        return conn.execute_query(query, {'city': city, 'star_rating': star_rating})
    
    @staticmethod
    def template_D1_describe_all_aspects(conn: Neo4jConnection, hotel_name: str):
        query = """MATCH (h:Hotel)-[:LOCATED_IN]->(city:City)-[:LOCATED_IN]->(country:Country)
        WHERE toLower(h.name) = toLower($hotel_name) OPTIONAL MATCH (h)<-[:REVIEWED]-(r:Review)
        RETURN h.name AS hotel_name, city.name AS city_name, country.name AS country_name,
        h.cleanliness_base AS cleanliness_base, h.comfort_base AS comfort_base, h.facilities_base AS facilities_base, 
        h.location_base AS location_base, h.staff_base AS staff_base, h.value_for_money_base AS value_for_money_base,
        avg(r.score_cleanliness) AS cleanliness_review, avg(r.score_comfort) AS comfort_review,
        avg(r.score_facilities) AS facilities_review, avg(r.score_location) AS location_review,
        avg(r.score_staff) AS staff_review, avg(r.score_value_for_money) AS value_for_money_review, 
        count(r) AS review_count LIMIT 1"""
        return conn.execute_query(query, {'hotel_name': hotel_name})
    
    @staticmethod
    def template_D2_describe_specific_aspects(conn: Neo4jConnection, hotel_name: str, aspects: List[str]):
        aspect_mapping = {'cleanliness': ('cleanliness_base', 'score_cleanliness'), 'comfort': ('comfort_base', 'score_comfort'),
                         'facilities': ('facilities_base', 'score_facilities'), 'location': ('location_base', 'score_location'),
                         'staff': ('staff_base', 'score_staff'), 'value_for_money': ('value_for_money_base', 'score_value_for_money')}
        
        valid_aspects = [a for a in aspects if a in aspect_mapping]
        if not valid_aspects:
            return QueryLibrary.template_D1_describe_all_aspects(conn, hotel_name)
        
        aspect_fields = []
        for aspect in valid_aspects:
            base_field, review_field = aspect_mapping[aspect]
            aspect_fields.append(f"h.{base_field} AS {aspect}_base")
            aspect_fields.append(f"avg(r.{review_field}) AS {aspect}_review")
        
        aspect_select = ", ".join(aspect_fields)
        query = f"""MATCH (h:Hotel)-[:LOCATED_IN]->(city:City)-[:LOCATED_IN]->(country:Country)
        WHERE toLower(h.name) = toLower($hotel_name) OPTIONAL MATCH (h)<-[:REVIEWED]-(r:Review)
        RETURN h.name AS hotel_name, city.name AS city_name, country.name AS country_name, {aspect_select}, count(r) AS review_count LIMIT 1"""
        return conn.execute_query(query, {'hotel_name': hotel_name})
    
    @staticmethod
    def template_C1_compare_all_aspects(conn: Neo4jConnection, hotel1: str, hotel2: str, aspects: List[str] = None):
        aspect_mapping = {'cleanliness': 'cleanliness_base', 'comfort': 'comfort_base', 'facilities': 'facilities_base',
                         'location': 'location_base', 'staff': 'staff_base', 'value_for_money': 'value_for_money_base'}
        
        if aspects:
            valid_aspects = [a for a in aspects if a in aspect_mapping]
            if not valid_aspects:
                return []
        else:
            valid_aspects = list(aspect_mapping.keys())
        
        aspect_fields = []
        for aspect in valid_aspects:
            base_field = aspect_mapping[aspect]
            aspect_fields.append(f"h1.{base_field} AS hotel1_{aspect}_base")
            aspect_fields.append(f"h2.{base_field} AS hotel2_{aspect}_base")
        
        aspect_select = ", ".join(aspect_fields)
        
        query = f"""MATCH (h1:Hotel)-[:LOCATED_IN]->(city1:City)-[:LOCATED_IN]->(country1:Country),
        (h2:Hotel)-[:LOCATED_IN]->(city2:City)-[:LOCATED_IN]->(country2:Country)
        WHERE toLower(h1.name) = toLower($hotel1) AND toLower(h2.name) = toLower($hotel2)
        RETURN h1.name AS hotel1_name, city1.name AS hotel1_city, country1.name AS hotel1_country,
        h2.name AS hotel2_name, city2.name AS hotel2_city, country2.name AS hotel2_country,
        {aspect_select} LIMIT 1"""
        return conn.execute_query(query, {'hotel1': hotel1, 'hotel2': hotel2})
    
    @staticmethod
    def template_C2_compare_with_traveller_type(conn: Neo4jConnection, hotel1: str, hotel2: str, 
                                               traveller_type: str, aspects: List[str] = None):
        aspect_mapping = {'cleanliness': 'cleanliness_base', 'comfort': 'comfort_base', 'facilities': 'facilities_base',
                         'location': 'location_base', 'staff': 'staff_base', 'value_for_money': 'value_for_money_base'}
        
        if aspects:
            valid_aspects = [a for a in aspects if a in aspect_mapping]
            if not valid_aspects:
                return QueryLibrary.template_C1_compare_all_aspects(conn, hotel1, hotel2)
        else:
            valid_aspects = list(aspect_mapping.keys())
        
        aspect_fields = []
        for aspect in valid_aspects:
            base_field = aspect_mapping[aspect]
            aspect_fields.append(f"h1.{base_field} AS hotel1_{aspect}_base")
            aspect_fields.append(f"h2.{base_field} AS hotel2_{aspect}_base")
        
        aspect_select = ", ".join(aspect_fields)
        
        query = f"""MATCH (h1:Hotel)-[:LOCATED_IN]->(city1:City)-[:LOCATED_IN]->(country1:Country),
        (h2:Hotel)-[:LOCATED_IN]->(city2:City)-[:LOCATED_IN]->(country2:Country)
        WHERE toLower(h1.name) = toLower($hotel1) AND toLower(h2.name) = toLower($hotel2)
        RETURN h1.name AS hotel1_name, city1.name AS hotel1_city, country1.name AS hotel1_country,
        h2.name AS hotel2_name, city2.name AS hotel2_city, country2.name AS hotel2_country,
        {aspect_select} LIMIT 1"""
        
        results = conn.execute_query(query, {'hotel1': hotel1, 'hotel2': hotel2, 'traveller_type': traveller_type})
        if not results:
            results = QueryLibrary.template_C1_compare_all_aspects(conn, hotel1, hotel2, aspects)
        return results
    
    @staticmethod
    def template_V1_check_visa_requirement(conn: Neo4jConnection, from_country: str, to_country: str):
        query = """MATCH (from:Country {name: $from_country}), (to:Country {name: $to_country})
        OPTIONAL MATCH (from)-[v:NEEDS_VISA]->(to)
        RETURN from.name AS from_country, to.name AS to_country, v.visa_type AS visa_type, 
        CASE WHEN v IS NOT NULL THEN true ELSE false END AS visa_required LIMIT 1"""
        return conn.execute_query(query, {'from_country': from_country, 'to_country': to_country})

print("QueryLibrary defined (14 templates)")