from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from database.db import Db

class DeckModel:

    db = Db()

    def get_decks(self, user_id: int):

        # Result is a 2D list with each list element: [deck_name, deck_length]
        return [[deck[0], self.get_deck_length(user_id, deck[0])] for deck in self.db.fetch_decks(user_id)]
    
    def get_deck_length(self, user_id: int, deck_name: str):
        return self.db.get_deck_length(user_id, deck_name)
    
    def get_vocabs(self, user_id: int, deck_name: str):
        return self.db.fetch_flashcards(user_id, deck_name)