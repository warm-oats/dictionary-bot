from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from api_manager.dict_api import DictAPIManager

class DictModel():
    
    def __init__(self):
        DictModel.api_manager = DictAPIManager()

    def get_word_info(self, word):
        api_response = DictModel.api_manager.request_json(word) 
        word_info = {}

        word_info["word_name"] = api_response[0]['meta']['id']
        word_info["stem_set"] = set(map(lambda stem: stem.split(" ")[0], api_response[0]["meta"]["stems"]))
        word_info["definitions"] = api_response[0]["shortdef"] 
        word_info["part_of_speech"] = api_response[0]["fl"]

        return word_info
    
if __name__ == '__main__':
    dict_model = DictModel()

    print(dict_model.get_word_info('hey'))
