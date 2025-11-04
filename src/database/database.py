import psycopg2
import os
import ast
from dotenv import load_dotenv

load_dotenv()

class DataBase:

    def __init__(self):
        self.connection = psycopg2.connect(**ast.literal_eval(os.getenv("DB_CONNECT")))
        self.cursor = self.connection.cursor()

    def deck_exists(self, user_id, deck_name) -> bool:
        self.cursor.execute(f"""
                            SELECT EXISTS(
                            SELECT 1
                            FROM flashcards.user_decks
                            WHERE user_id = {user_id}
                            AND deck_name = '{deck_name}'
                            );
                            """)
        
        return self.cursor.fetchone()[0]

    def create_deck(self, user_id: int, deck_name: str):
        if (not self.deck_exists(user_id, deck_name)):
            self.cursor.execute(f"""
                                INSERT into flashcards.user_decks(user_id, deck_name)
                                VALUES({user_id}, '{deck_name}');
                                """)

            self.connection.commit()
        else:
            raise ValueError(f"Deck '{deck_name}' already exists")
        
    def delete_deck(self, user_id, deck_name):

        if (not self.deck_exists(user_id, deck_name)):
            raise ValueError(name = f"Deck '{deck_name}' doesn't exist")

        self.cursor.execute(f""" 
            DELETE FROM flashcards.user_decks
            WHERE user_id = {user_id} 
            AND deck_name = '{deck_name}';
            """)
        
        self.cursor.execute(f"""
            DELETE FROM flashcards.flashcards
            WHERE user_id = {user_id}
            AND deck_name = '{deck_name}';
            """)

    def update_deck_name(self, user_id, deck_name, new_deck_name):
            
        if (not self.deck_exists):
            raise ValueError(name = f"Deck '{deck_name}' does not exist")

        self.cursor.execute(f"""
                            UPDATE flashcards.user_decks
                            SET deck_name = '{new_deck_name}'
                            WHERE user_id = {user_id}
                            AND deck_name = '{deck_name}';
                            """)
        
        self.cursor.execute(f"""
                            UPDATE flashcards.flashcards
                            SET deck_name = '{new_deck_name}'
                            WHERE user_id = {user_id}
                            AND deck_name = '{deck_name}';
                            """)

    def add_word(self, user_id, word, definition, deck_name):
        if (self.deck_exists(user_id, deck_name)):
            self.cursor.execute(f"""
                                INSERT into flashcards.flashcards(user_id, deck_name, front_page, back_page) 
                                VALUES({user_id}, '{deck_name}', '{word}', '{definition}');
                                """)
        else:
            raise ValueError(name = f"Invalid user id or deck name (does not exist)")
        
    def delete_word(self, user_id, word, deck_name):
        try:
            self.cursor.execute(f"""
                                DELETE FROM flashcards.flashcards 
                                WHERE user_id = {user_id}
                                AND front_page = '{word}'
                                AND deck_name = '{deck_name}';
                                """)
        except ValueError:
            return f"Invalid user id or deck name (does not exist)"
        
    def update_word(self, user_id, new_word, new_definition, deck_name):
        pass

    def fetch_word(self):
        
        self.cursor.execute("select * from flashcards.user_decks;")

        # Fetch all rows from database
        record = self.cursor.fetchall()

        print("Data from Database:- ", record)

        self.cursor.execute("select * from flashcards.flashcards;")

        # Fetch all rows from database
        record = self.cursor.fetchall()

        print("Data from Database:- ", record)

if __name__ == "__main__":
    db = DataBase()

    db.fetch_word()
    db.update_deck_name(123456, "kOREAN fwaefafe", "Korean Stuff")
    print('---------------------')
    db.fetch_word()
    db.add_word(123456, "hello", "Means hello", "Korean Stuff")
    print('---------------------')
    db.fetch_word()
    db.delete_word(123456, "hello", "Korean Stuff")
    print('---------------------')
    db.fetch_word()
    db.delete_deck(123456, "Korean Stuff")
    print('---------------------')
    db.fetch_word()