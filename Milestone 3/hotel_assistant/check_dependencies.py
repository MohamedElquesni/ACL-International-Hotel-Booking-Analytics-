"""Dependency Checker - Ensures all required packages are installed"""

import sys
import os
import importlib.util

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REQUIRED_PACKAGES = {
    'streamlit': 'streamlit',
    'dotenv': 'python-dotenv',
    'openai': 'openai',
    'neo4j': 'neo4j',
    'sentence_transformers': 'sentence-transformers',
    'transformers': 'transformers',
    'torch': 'torch',
    'pandas': 'pandas',
    'numpy': 'numpy'
}

def check_package(package_name, install_name=None):
    if install_name is None:
        install_name = package_name

    spec = importlib.util.find_spec(package_name)
    if spec is None:
        return False, install_name
    return True, None

def check_all_dependencies():
    missing = []
    print("Checking dependencies...")
    print("=" * 50)

    for package, install_name in REQUIRED_PACKAGES.items():
        is_installed, missing_package = check_package(package, install_name)
        status = "OK" if is_installed else "MISSING"
        symbol = "+" if is_installed else "-"

        print(f"  [{symbol}] {package:25} {status}")

        if not is_installed:
            missing.append(missing_package)

    print("=" * 50)

    if missing:
        print(f"\nMissing {len(missing)} package(s):")
        for pkg in missing:
            print(f"  - {pkg}")

        print("\nInstall missing packages:")
        print(f"  pip install {' '.join(missing)}")
        return False
    else:
        print("\n[+] All dependencies installed!")
        return True

def verify_hotel_assistant_modules():
    print("\nVerifying hotel_assistant modules...")
    print("=" * 50)

    modules = [
        ('hotel_assistant.config', 'OPENAI_API_KEY'),
        ('hotel_assistant.database.neo4j_connection', 'Neo4jConnection'),
        ('hotel_assistant.database.query_library', 'QueryLibrary'),
        ('hotel_assistant.database.query_executor', 'select_and_execute_query'),
        ('hotel_assistant.nlp.intent_classifier', 'IntentClassifier'),
        ('hotel_assistant.nlp.entity_extractor', 'extract_entities'),
        ('hotel_assistant.nlp.embeddings', 'semantic_search_mpnet'),
        ('hotel_assistant.llm.prompt_engine', 'PromptEngine'),
        ('hotel_assistant.llm.context_builder', 'ContextBuilder'),
        ('hotel_assistant.llm.result_merger', 'merge_and_rank_results'),
        ('hotel_assistant.llm.llm_layer', 'llm_layer')
    ]

    all_ok = True
    for module_path, component in modules:
        try:
            module = importlib.import_module(module_path)
            if hasattr(module, component):
                print(f"  [+] {module_path:50} {component}")
            else:
                print(f"  [-] {module_path:50} Missing: {component}")
                all_ok = False
        except Exception as e:
            print(f"  [-] {module_path:50} Error: {str(e)[:30]}")
            all_ok = False

    print("=" * 50)

    if all_ok:
        print("\n+ All hotel_assistant modules verified!")
    else:
        print("\n- Some modules have issues")

    return all_ok

if __name__ == "__main__":
    deps_ok = check_all_dependencies()
    modules_ok = verify_hotel_assistant_modules()

    if deps_ok and modules_ok:
        print("\n" + "=" * 50)
        print("READY TO RUN!")
        print("=" * 50)
        print("\nNext steps:")
        print("  1. Create .env file with OPENAI_API_KEY")
        print("  2. Verify KnowledgeGraph/config.txt exists")
        print("  3. Run: streamlit run app.py")
        sys.exit(0)
    else:
        sys.exit(1)
