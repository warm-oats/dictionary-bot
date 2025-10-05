from pydantic import BaseModel

class TranslationFormat(BaseModel):
    text: str
    translation: str
    nouns: list[dict[str, str]]
    verbs: list[dict[str, str]]
    adjectives: list[dict[str, str]]