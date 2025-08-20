from api_manager import MerriamAPIManager, RandomAPIManager

class Translator():

    merriam_request = MerriamAPIManager().request_json

    def __init__(self):
        pass

    def get_word(self, word):
        merriam_response = self.merriam_request(word)

        word_name = word
        stem_set = set(map(lambda stem: stem.split(" ")[0], merriam_response[0]["meta"]["stems"]))
        short_def = merriam_response[0]["shortdef"] 
        part_of_speech = merriam_response[0]["fl"]

        print(word_name, stem_set, short_def, part_of_speech)

if __name__ == '__main__':
    translator = Translator()

    translator.get_word('voluminous')