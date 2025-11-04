import psycopg2
import os
import ast
from dotenv import load_dotenv

load_dotenv()

class Db:

    connection = psycopg2.connect(**ast.literal_eval(os.getenv("DB_CONNECT")))
    cursor = connection.cursor()

    def deck_not_exist(self, user_id: int, deck_name: str) -> bool:
        self.cursor.execute(f"""
                            SELECT EXISTS(
                            SELECT 1
                            FROM flashcards.user_decks
                            WHERE user_id = {user_id}
                            AND deck_name = '{deck_name}');
                            """)
        
        if (not self.cursor.fetchone()[0]):
            raise ValueError(f"Deck '{deck_name}' does not exist")
        
    def vocab_not_exist(self, user_id: int, deck_name: str, vocab: str):
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

    def deck_exist(self, user_id: int, deck_name: str) -> bool:
        self.cursor.execute(f"""
                            SELECT EXISTS(
                            SELECT 1
                            FROM flashcards.user_decks
                            WHERE user_id = {user_id}
                            AND deck_name = '{deck_name}');
                            """)
        
        if (self.cursor.fetchone()[0]):
            raise ValueError(f"Deck '{deck_name}' already exist")
        
    def vocab_exist(self, user_id: int, deck_name: str, vocab: str):
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
            return e
        
    def delete_deck(self, user_id: int, deck_name: str):

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
            return e

    def update_deck_name(self, user_id: int, deck_name: str, new_deck_name: str):
        
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
            return e

    def add_vocab(self, user_id: int, deck_name: str, vocab: str, definition: str):
        
        try:
            self.deck_not_exist(user_id, deck_name)
            self.vocab_exist(user_id, deck_name, vocab)

            self.cursor.execute(f"""
                                INSERT into flashcards.flashcards(user_id, deck_name, front_page, back_page) 
                                VALUES({user_id}, '{deck_name}', '{vocab}', '{definition}');
                                """)
            
            self.connection.commit()
        except ValueError as e:
            return e
        
    def delete_vocab(self, user_id: int, deck_name: str, vocab: str):

        try:
            self.deck_not_exist(user_id, deck_name)
            self.vocab_not_exist(user_id, deck_name, vocab)

            self.cursor.execute(f"""
                                DELETE FROM flashcards.flashcards 
                                WHERE user_id = {user_id}
                                AND front_page = '{vocab}'
                                AND deck_name = '{deck_name}';
                                """)
            
            self.connection.commit()
        except ValueError as e:
            return e
        
    def update_word(self, user_id: int, deck_name: str, vocab: str, new_vocab: str, new_definition: str):

        try:
            self.deck_not_exist(user_id, deck_name)
            self.vocab_not_exist(user_id, deck_name, vocab)

            self.cursor.execute(f"""
                                UPDATE flashcards.flashcards
                                SET front_page = '{new_vocab}', back_page = '{new_definition}'
                                WHERE deck_name = '{deck_name}'
                                AND user_id = {user_id}
                                AND front_page = '{vocab}';
                                """)
        except ValueError as e:
            return e

    def fetch_vocabs(self, user_id: int, deck_name: str):
        
        try:
            self.deck_not_exist(user_id, deck_name)

            self.cursor.execute(f"""
                                SELECT front_page, back_page
                                FROM flashcards.flashcards
                                WHERE user_id = {user_id}
                                AND deck_name = '{deck_name}';
                                """)
            
            vocabs = self.cursor.fetchall()

            return vocabs
        except ValueError as e:
            return e

    def fetch_decks(self, user_id: int):
        
        self.cursor.execute(f"""
                            SELECT deck_name
                            FROM flashcards.user_decks
                            WHERE user_id = {user_id};
                            """)
        
        all_decks = self.cursor.fetchall()

        return all_decks
    
    def get_deck_length(self, user_id: int, deck_name: str):

        try:
            self.deck_not_exist(user_id, deck_name)

            self.cursor.execute(f"""
                                SELECT COUNT(*)
                                FROM flashcards.flashcards
                                WHERE user_id = {user_id}
                                AND deck_name = '{deck_name}';
                                """)
            
            deck_len = self.cursor.fetchone()[0]

            return deck_len
        except ValueError as e:
            return e