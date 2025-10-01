from decouple import config
from groq import Groq

class ConvoApiManager:

    def __init__(self):
        self.client = Groq(api_key = config('GROQ_API'))
