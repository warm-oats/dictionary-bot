from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from api_manager.dict_api import DictAPIManager

class DictModel():

    api_manager = DictAPIManager()

    def get_word_info(self, word):
        api_response = DictModel.api_manager.request_json(word)
        word_infos = [] # List of all possible definition contexts

        for word_info in api_response:
            word_infos.append(self.process_word_info(word_info))

        return word_infos # Always be a dict with word property key pair values
    
    def process_word_info(self, unprocessed_word):
        word_info = {}

        word_info["word_name"] = ''.join([letter for letter in unprocessed_word['meta']['id'] if letter.isalpha()])
        word_info["stem_set"] = set(map(lambda stem: stem.split(" ")[0], unprocessed_word["meta"]["stems"]))
        word_info["definitions"] = unprocessed_word["shortdef"] 
        word_info["part_of_speech"] = unprocessed_word["fl"]

        return word_info
    
if __name__ == '__main__':
    dict_model = DictModel()

    print(dict_model.get_word_info('what'))
