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
    comments: Optional[str] = None


# Generate convo text using the Groq API
def groq_translate(query):
    # Create a chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful Korean language teacher."
                           f"Do not use phonetic spelling or romanization of Korean. Only use authentic Hangul."
                           f"Only use beginner level conversations, keep replies short and simple, and not too wordy."
                           f"Don't attach any phonetic or romanized Korean spelling or pronunciation on the side when replying."
                           f"Maintain the conversation and keep it going naturally unless directed otherwise by the user."
                           f"Minimize talking in English unless directed otherwise."
                           f"If no conversations have been started, suggest a conversation with a common Korean topic."
                           f"You will only reply in the form of JSON."
                           f"When having a conversation, the JSON object must use the schema: {json.dumps(Conversation.model_json_schema(), indent=2)}. For text field, put the Hangul. For comments field, put the English translation of the Hangul."
            },
            {
                "role": "user",
                "content": f"{query}"
            }
        ],
        model="openai/gpt-oss-20b",
        temperature=0.2,
        max_tokens=1024,
        stream=False,
        response_format={"type": "json_object"},
    )

    review = Conversation.model_validate(json.loads(chat_completion.choices[0].message.content))
    print(review.model_dump())

if __name__ == "__main__":
    groq_translate('Start a conversation using the word "fish"')
