from konlpy.tag import Mecab

class POSTagAPIManager():

    def extract_pos(self, phrase):
        return Mecab().pos(phrase)
    
if __name__ == '__main__':

    mecab = POSTagAPIManager()

    print(mecab.extract_pos("안녕하세요"))