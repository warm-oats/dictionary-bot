from konlpy.tag import Okt

class PosTagModel:

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
    
if __name__ == '__main__':

    okt = PosTagModel()

    print(okt.extract_pos("수학적으로 n차 다항식이 n + 1개 점으로 일대일 대응됨을 증명하라"))