from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from api.groq_api import GroqApi
from util.translation_format import TranslationFormat
import json

class GroqModel:

    def __init__(self, language: str):
        self.groq_api = GroqApi()
        self.client = self.groq_api.client
        self.prompt = [
            {
                "role": "system",
                "content": 
                        f"You are a helpful {language} language translator."
                        f"You will be given a Korean sentence and 3 part of speech lists containing Korean nouns, verbs, and adjectives each respectively."
                        f"Your role is to translate that sentence and each word in the parts of speech lists appearing in the Korean sentence in that context."
                        f"Before processing the Korean sentence, remove all unnecessary white space and line breaks from it."
                        f"You will only reply in the form of JSON."
                        f"""The JSON object must use the schema: {json.dumps(TranslationFormat.model_json_schema(), indent=2)}. 
                        For text field, put the sentence. 
                        For translation field, put the English translation of the text.
                        For the nouns field, put dictionary key value pairs where key is the original Korean noun in the Korean nouns list and value is the translated meaning in its context.
                        For the verbs field, put dictionary key value pairs where key is the original Korean verb in the Korean nouns list and value is the translated meaning in its context.
                        For the adjectives field, put dictionary key value pairs where key is the original Korean adjective in the Korean nouns list and value is the translated meaning in its context.
                        """
            }
        ]

    def groq_translate(self, message: str):
        
        translation_request = self.client.chat.completions.create(
            messages = message,
            model="openai/gpt-oss-120b",
            temperature=0.2,
            max_tokens=3000,
            stream=False,
            response_format={"type": "json_object"},
        )

        response = TranslationFormat.model_validate(json.loads(translation_request.choices[0].message.content)).model_dump()

        return response
    
    def send_message(self, message: str):
        
        self.parse_user_msg(message)

        response = self.groq_translate(self.prompt)

        self.parse_bot_msg(response['text'])

        return response
    
    # Modifies self.prompt in place
    def parse_user_msg(self, user_msg: str):

        user_msg_dict = {
            "role": "user",
            "content": f"{user_msg}"
        }

        self.prompt.append(user_msg_dict)

        return user_msg_dict
    
    def parse_bot_msg(self, bot_msg: str):
        
        bot_msg_dict = {
            "role": "system",
            "content": f"{bot_msg}"
        }

        self.prompt.append(bot_msg_dict)

        return bot_msg_dict
    
if __name__ == "__main__":
    translator = GroqModel("Korean")
    nouns = ['곶감', '뭐', '게']
    verbs = ['크다']
    adjectives = ['무섭다', '분명하다']

    user_msg = f"""
    sentence: 곶감이 뭐지? 크고 무서운 게 분명해.’
    nouns: {nouns}
    verbs: {verbs}
    adjectives: {adjectives}
    """

    translator = GroqModel("Korean")

    response = translator.send_message(user_msg)

    print(response)