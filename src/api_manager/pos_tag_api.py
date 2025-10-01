from konlpy.tag import Okt

class PosTagApiManager:

    def extract_pos(self, phrase):
        okt = Okt()
        pos_map = {'Noun': [], 'Verb': [], 'Adjective': []}

        processed_phrase = okt.pos(phrase, norm = True, stem = True)

        for word_tup in processed_phrase:
            POS_i = 1
            WORD_i = 0

            if (word_tup[POS_i] in pos_map):
                pos_map[word_tup[POS_i]] = word_tup[WORD_i]

        return pos_map
    
if __name__ == '__main__':

    okt = PosTagApiManager()