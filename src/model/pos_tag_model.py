from konlpy.tag import Okt
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.translator_model import TranslatorModel

class PosTagModel:

    translator = TranslatorModel()
    translate_from = 'ko'
    translate_to = 'en'

    def extract_pos(self, phrase):
        okt = Okt()
        pos_map = {'Noun': [], 'Verb': [], 'Adjective': []}

        processed_phrase = okt.pos(phrase, norm = True, stem = True)

        for word_tup in processed_phrase:
            POS_i = 1
            WORD_i = 0

            if (word_tup[POS_i] in pos_map):
                pos_map[word_tup[POS_i]].append(word_tup[WORD_i])

        return pos_map # Always a dict of POS with key pair values
    
    def map_pos_meaning(self, phrase_map):
        word_meaning_map = {'Noun': [], 'Verb': [], 'Adjective': []}

        for pos, words in phrase_map.items():
            for word in words:
                word_meaning_map[pos].append(self.map_word_meaning(word))

        return word_meaning_map

    def map_word_meaning(self, word):

        meaning = self.translator.translate_word(word, self.translate_from, self.translate_to).text

        return {word: meaning}
    
if __name__ == '__main__':

    tag_model = PosTagModel()

    print(tag_model.map_pos_meaning(tag_model.extract_pos("‘곶감이 뭐지? 크고 무서운 게 분명해.’ 호랑이는 생각했다. ‘곶감을 피해야 해. 그렇지 않으면 나는 죽을 지 몰라.’")))