"""Neo4j Database Connection"""
import os
from neo4j import GraphDatabase

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