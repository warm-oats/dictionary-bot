import requests

class RandomAPIManager():
    
    def request_json(self, amount=1, word_length=4):
        response = requests.get(f"https://random-word-api.herokuapp.com/word?number={amount}&length={word_length}")
        
        return response.json() # Output is a list of words