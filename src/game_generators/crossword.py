from src.api_manager import RandomAPIManager, MerriamAPIManager

generate_random = RandomAPIManager().request_json
generate_merriam = MerriamAPIManager().request_json

if __name__ == '__main__':
    generate_random(3, 5)


