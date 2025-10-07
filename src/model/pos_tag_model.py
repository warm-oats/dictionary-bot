from konlpy.tag import Okt
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.translator_model import TranslatorModel
from model.groq_model import GroqModel

class PosTagModel:

    translator = GroqModel("Korean")
    translate_from = 'ko'
    translate_to = 'en'

    def extract_pos(self, phrase, norm = True, stem = True):
        okt = Okt()
        pos_map = {'nouns': [], 'verbs': [], 'adjectives': []}

        processed_phrase = okt.pos(phrase, norm = norm, stem = stem)

        for word_tup in processed_phrase:
            POS_i = 1
            WORD_i = 0

            # Convert library dict keys to new keys for processing
            convert_pos = {'Noun': 'nouns', 'Verb': 'verbs', 'Adjective': 'adjectives'}

            if (word_tup[POS_i] in convert_pos):
                pos_map[convert_pos[word_tup[POS_i]]].append(word_tup[WORD_i])

        # Remove duplicates from part of speech mapping
        for pos, word_list in pos_map.items():
            pos_map[pos] = list(set(word_list))

        #Always a dict of {'pos': [Korean words]}
        return pos_map
    
    def map_pos_meaning(self, phrase, phrase_map):

        user_msg = f"""
            sentence: {phrase.strip()}
            nouns: {phrase_map['nouns']}
            verbs: {phrase_map['verbs']}
            adjectives: {phrase_map['adjectives']}"""
        
        translation_map = self.translator.send_message(user_msg)

        return translation_map
    
if __name__ == '__main__':

    tag_model = PosTagModel()

    print(tag_model.extract_pos("‘곶감이 뭐지? 크고 무서운 게 분명해.’ 호랑이는 생각했다. ‘곶감을 피해야 해. 그렇지 않으면 나는 죽을 지 몰라.’", True, False))