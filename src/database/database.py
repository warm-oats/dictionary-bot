import psycopg2
import os
import ast
from dotenv import load_dotenv

load_dotenv()

class DataBase:

    def __init__(self):
        self.connection = psycopg2.connect(**ast.literal_eval(os.getenv("DB_CONNECT")))
        self.cursor = self.connection.cursor()

    def deck_not_exist(self, user_id, deck_name) -> bool:
        self.cursor.execute(f"""
                            SELECT EXISTS(
                            SELECT 1
                            FROM flashcards.user_decks
                            WHERE user_id = {user_id}
                            AND deck_name = '{deck_name}');
                            """)
        
        if (not self.cursor.fetchone()[0]):
            raise ValueError(f"Deck '{deck_name}' does not exist")
        
    def vocab_not_exist(self, user_id, deck_name, vocab):
        self.cursor.execute(f"""
                            SELECT EXISTS(
                            SELECT 1
                            FROM flashcards.flashcards
                            WHERE user_id = {user_id}
                            AND deck_name = '{deck_name}'
                            AND front_page = '{vocab}');
                            """)
        
        if (not self.cursor.fetchone()[0]):
            raise ValueError(f"Vocab '{vocab}' does not exist")

    def deck_exist(self, user_id, deck_name) -> bool:
        self.cursor.execute(f"""
                            SELECT EXISTS(
                            SELECT 1
                            FROM flashcards.user_decks
                            WHERE user_id = {user_id}
                            AND deck_name = '{deck_name}');
                            """)
        
        if (self.cursor.fetchone()[0]):
            raise ValueError(f"Deck '{deck_name}' already exist")
        
    def vocab_exist(self, user_id, deck_name, vocab):
        self.cursor.execute(f"""
                            SELECT EXISTS(
                            SELECT 1
                            FROM flashcards.flashcards
                            WHERE user_id = {user_id}
                            AND deck_name = '{deck_name}'
                            AND front_page = '{vocab}');
                            """)
        
        if (self.cursor.fetchone()[0]):
            raise ValueError(f"Vocab '{vocab}' already exist")

    def create_deck(self, user_id: int, deck_name: str):
        
        try:
            self.deck_exist(user_id, deck_name)

            self.cursor.execute(f"""
                    INSERT into flashcards.user_decks(user_id, deck_name)
                    VALUES({user_id}, '{deck_name}');
                    """)

            self.connection.commit()  
        except ValueError as e:
            print(e)
        
    def delete_deck(self, user_id, deck_name):

        try:
            self.deck_not_exist(user_id, deck_name)

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
        
            self.connection.commit()
        except ValueError as e:
            print(e)

    def update_deck_name(self, user_id, deck_name, new_deck_name):
        
        try:
            self.deck_not_exist(user_id, deck_name)

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
            
            self.connection.commit()
        except ValueError as e:
            print(e)

    def add_vocab(self, user_id, vocab, definition, deck_name):
        
        try:
            self.deck_not_exist(user_id, deck_name)
            self.vocab_exist(user_id, deck_name, vocab)

            self.cursor.execute(f"""
                                INSERT into flashcards.flashcards(user_id, deck_name, front_page, back_page) 
                                VALUES({user_id}, '{deck_name}', '{vocab}', '{definition}');
                                """)
        except ValueError as e:
            print(e)
        
    def delete_vocab(self, user_id, vocab, deck_name):

        try:
            self.deck_not_exist(user_id, deck_name)
            self.vocab_not_exist(user_id, deck_name, vocab)

            self.cursor.execute(f"""
                                DELETE FROM flashcards.flashcards 
                                WHERE user_id = {user_id}
                                AND front_page = '{vocab}'
                                AND deck_name = '{deck_name}';
                                """)
        except ValueError as e:
            print(e)
        
    def update_word(self, user_id, new_word, new_definition, deck_name):
        pass

    def fetch_vocab(self):
        
        self.cursor.execute("select * from flashcards.user_decks;")

        # Fetch all rows from database
        record = self.cursor.fetchall()

        print("Data from Decks:- ", record)

        self.cursor.execute("select * from flashcards.flashcards;")

        # Fetch all rows from database
        record = self.cursor.fetchall()

        print("Data from Flashcards:- ", record)

if __name__ == "__main__":
    db = DataBase()

    db.create_deck(123456, "Korean Stuff")
    db.fetch_vocab()
    db.update_deck_name(123456, "Korean Stuff", "Korean Stuff")
    print('---------------------')
    db.fetch_vocab()
    db.add_vocab(123456, "what", "Means hello", "Korean Stuff")
    print('---------------------')
    db.fetch_vocab()
    db.delete_vocab(123456, "whattttttttt", "Korean Stuff")
    print('---------------------')
    db.fetch_vocab()
    db.delete_deck(123456, "Korean Stuff")
    print('---------------------')
    db.fetch_vocab()