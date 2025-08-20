import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from api_manager import MerriamAPIManager, RandomAPIManager

generate_random = RandomAPIManager().request_json
generate_merriam = MerriamAPIManager().request_json

if __name__ == '__main__':
    print(generate_random())


