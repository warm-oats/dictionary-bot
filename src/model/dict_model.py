from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from api_manager.dict_api import DictAPIManager

class DictModel():

    api_manager = DictAPIManager()

    def get_word_info(self, word):
        api_response = DictModel.api_manager.request_json(word)
        def_contexts = [] # List of all possible definition contexts

        for word_info in api_response:
            def_contexts.append(self.process_word_info(word_info, word))

        return list(filter(lambda def_context: def_context, def_contexts)) # Always be a list with dicts containing all definition contexts
    
    def process_word_info(self, unprocessed_word, word_name):
        word_info = {}

        word_info["word_name"] = ''.join([letter for letter in unprocessed_word['meta']['id'] if letter.isalpha()])
        word_info["stem_set"] = set(filter(lambda stem: len(stem) == 1, unprocessed_word["meta"]["stems"]))
        word_info["definitions"] = unprocessed_word["shortdef"] 
        word_info["part_of_speech"] = unprocessed_word["fl"]
        
        if self.is_valid_word(word_info, word_name):
            return word_info # Always be a dict with word property key pair values
    
    def is_valid_word(self, word_info, word_name):
        return word_info["word_name"] == word_name
    
if __name__ == '__main__':
    dict_model = DictModel()

    print(dict_model.get_word_info('fish'))
