from api_manager import MerriamAPIManager, PapagoAPIManager

class Translator():

    merriam_API = MerriamAPIManager()
    papago_API = PapagoAPIManager()

    def __init__(self):
        pass

    def get_word(self, word):
        merriam_response = self.merriam_API.request_json(word)
        word_info = {}

        word_info["word_name"] = word
        word_info["stem_set"] = set(map(lambda stem: stem.split(" ")[0], merriam_response[0]["meta"]["stems"]))
        word_info["definitions"] = merriam_response[0]["shortdef"] 
        word_info["part_of_speech"] = merriam_response[0]["fl"]

        return word_info
    
    def translate_word(self, word):
        return self.papago_API.translate_word(word)

if __name__ == '__main__':
    translator = Translator()

    translator.get_word('voluminous')
    print(translator.translate_word('hello'))