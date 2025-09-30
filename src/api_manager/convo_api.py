# groq_translation.py
import json
from typing import Optional

from decouple import config
from groq import Groq
from pydantic import BaseModel

# Set up the Groq client
client = Groq(api_key = config('GROQ_API'))

# Model for conversations
class Conversation(BaseModel):
    text: str
    translation: str
    verb_vocabularies: list[dict]
    noun_vocabularies: list[dict]

class ConvoAPIManager():
    # Generate convo text using the Groq API

    def __init__(self):
        self.conversation = [
            {
                "role": "system",
                "content": 
                        f"You are a helpful Korean language teacher."
                        f"Only use beginner level conversations."
                        f"Keep replies simple. Maximum 2 sentences and no more than 50 words."
                        f"Don't attach any phonetic or romanized Korean spelling or pronunciation on the side when replying."
                        f"Minimize talking in English unless directed otherwise."
                        f"You will play your role and given context."
                        f"Use complete sentences."
                        f"Correct any grammatical or spelling errors."
                        f"You will only reply in the form of JSON."
                        f"""When having a conversation, the JSON object must use the schema: {json.dumps(Conversation.model_json_schema(), indent=2)}. 
                        For text field, put the Hangul. 
                        For translation field, put the English translation of the Hangul.
                        For the verb_vocabulary field, put all Korean verbs in the list as key pair values of key as the Korean verb in its base form and value as translation of that vocabulary.
                        For the noun_vocabulary field, put all Korean nouns in the list as key pair values of key as the Korean verb in its base form and value as translation of that vocabulary."""
            }
        ]

    def groq_translate(self, message):
        
        conversation = client.chat.completions.create(
            messages = message,
            model="openai/gpt-oss-20b",
            temperature=0.2,
            max_tokens=1024,
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
    conversationalist = ConvoAPIManager()

    while True:
        user_msg = input("Enter: ")

        response = conversationalist.send_message(user_msg)

        print(response)
