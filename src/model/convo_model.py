from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from api_manager.convo_api import ConvoApiManager
import json
from pydantic import BaseModel

class Conversation(BaseModel):
    text: str
    translation: str
    verb_vocabulary: list[dict[str, str]]
    noun_vocabulary: list[dict[str, str]]
    adjective_vocabulary: list[dict[str, str]]

class ConvoModel():

    def __init__(self, language):
        self.api_manager = ConvoApiManager()
        self.client = self.api_manager.client
        self.conversation = [
            {
                "role": "system",
                "content": 
                        f"You are a helpful {language} language teacher."
                        f"Only use beginner level conversations."
                        f"Keep replies short and simple, with a maximum of 2 sentences per reply and each reply should take no more than 35 words."
                        f"Don't attach any phonetic or romanized spelling or pronunciation on the side when replying."
                        f"Minimize talking in English unless directed otherwise."
                        f"Use complete sentences with correct grammar."
                        f"You will only reply in the form of JSON."
                        f"""When having a conversation, the JSON object must use the schema: {json.dumps(Conversation.model_json_schema(), indent=2)}. 
                        For text field, put the sentence. 
                        For translation field, put the English translation of the text."""
            }
        ]

    def groq_translate(self, message):
        
        conversation = self.client.chat.completions.create(
            messages = message,
            model="openai/gpt-oss-120b",
            temperature=0.2,
            max_tokens=1500,
            stream=False,
            response_format={"type": "json_object"},
        )

        response = Conversation.model_validate(json.loads(conversation.choices[0].message.content)).model_dump()

        return response
    
    def send_message(self, message):

        self.parse_user_msg(message)

        response = self.groq_translate(self.conversation)

        self.parse_bot_msg(response['text'])

        return response
    
    # Modifies self.conversation in place
    def parse_user_msg(self, user_msg):

        user_msg_dict = {
            "role": "user",
            "content": f"{user_msg}"
        }

        self.conversation.append(user_msg_dict)

        return user_msg_dict
    
    def parse_bot_msg(self, bot_msg):
        
        bot_msg_dict = {
            "role": "system",
            "content": f"bot_msg"
        }

        self.conversation.append(bot_msg_dict)

        return bot_msg_dict
    
if __name__ == "__main__":
    conversationalist = ConvoModel("Korean")

    while True:
        user_msg = input("Enter: ")

        response = conversationalist.send_message(user_msg)

        print(response)