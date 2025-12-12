# Knowledge Graph for Milestone 3

## Overview
This directory contains the improved knowledge graph schema for the Graph-RAG hotel assistant system.

## Changes from Milestone 2

### Added
- **Hotel base scores** for all 6 aspects:
  - `location_base`
  - `staff_base`
  - `value_for_money_base`

### Removed
- **STAYED_AT relationship** (Traveller -> Hotel)
  - Redundant: can be derived from `Traveller -> WROTE -> Review -> REVIEWED -> Hotel`

## Updated Schema

### Nodes

**Hotel**
```
- hotel_id
- name
- star_rating
- cleanliness_base, comfort_base, facilities_base
- location_base, staff_base, value_for_money_base (NEW)
- average_reviews_score
```

**Traveller**
```
- user_id
- age (age_group)
- type (traveller_type)
- gender
```

**Review**
```
- review_id
- text
- date
- score_overall
- score_cleanliness, score_comfort, score_facilities
- score_location, score_staff, score_value_for_money
```

**City**
```
- name
```

**Country**
```
- name
```

### Relationships

```
Traveller -[:WROTE]-> Review
Review -[:REVIEWED]-> Hotel
Hotel -[:LOCATED_IN]-> City
City -[:LOCATED_IN]-> Country
Traveller -[:FROM_COUNTRY]-> Country
Country -[:NEEDS_VISA {visa_type}]-> Country
```

## Benefits

### 1. Complete Aspect Coverage
All 6 aspects now have both base and review scores:
- cleanliness
- comfort
- facilities
- location
- staff
- value_for_money

### 2. Base vs Review Comparison
Can compare hotel's advertised quality vs actual guest experiences:
```cypher
MATCH (h:Hotel {name: 'Hilton Cairo'})
OPTIONAL MATCH (h)<-[:REVIEWED]-(r:Review)
RETURN
  h.location_base AS advertised,
  avg(r.score_location) AS actual
```

### 3. Demographic Filtering
Filter reviews by traveler demographics for personalized recommendations:
```cypher
MATCH (t:Traveller {type: 'Family'})-[:WROTE]->(r:Review)-[:REVIEWED]->(h:Hotel)
WHERE h.name = 'Marriott Dubai'
RETURN avg(r.score_cleanliness) AS family_cleanliness_rating
```

## Usage

### 1. Configure Neo4j
Edit `config.txt` with your Neo4j credentials:
```
URI=neo4j://localhost:7687
USERNAME=neo4j
PASSWORD=your_password
```

### 2. Run Script
```bash
cd "Milestone 3/KnowledgeGraph"
python Create_kg.py
```

### 3. Verify
The script will output:
- Number of nodes created for each type
- Number of relationships created
- Confirmation of all 6 base aspect scores

## Files

- `Create_kg.py` - Updated graph creation script
- `config.txt` - Neo4j connection configuration
- `Dataset/` - CSV files (hotels, users, reviews, visa)
- `README.md` - This file
