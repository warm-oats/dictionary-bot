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
        
    def flashcard_not_exist(self, user_id: int, deck_name: str, flashcard: str):
        self.cursor.execute(f"""
                            SELECT EXISTS(
                            SELECT 1
                            FROM flashcards.flashcards
                            WHERE user_id = {user_id}
                            AND deck_name = '{deck_name}'
                            AND flashcard_front = '{flashcard}');
                            """)
        
        if (not self.cursor.fetchone()[0]):
            raise ValueError(f"flashcard '{flashcard}' does not exist")

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
        
    def flashcard_exist(self, user_id: int, deck_name: str, flashcard: str):
        self.cursor.execute(f"""
                            SELECT EXISTS(
                            SELECT 1
                            FROM flashcards.flashcards
                            WHERE user_id = {user_id}
                            AND deck_name = '{deck_name}'
                            AND flashcard_front = '{flashcard}');
                            """)
        
        if (self.cursor.fetchone()[0]):
            raise ValueError(f"flashcard '{flashcard}' already exist")

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

    def add_flashcard(self, user_id: int, deck_name: str, flashcard_front: str, flashcard_back: str):
        
        try:
            self.deck_not_exist(user_id, deck_name)
            self.flashcard_exist(user_id, deck_name, flashcard_front)

            self.cursor.execute(f"""
                                INSERT into flashcards.flashcards(user_id, deck_name, flashcard_front, flashcard_back) 
                                VALUES({user_id}, '{deck_name}', '{flashcard_front}', '{flashcard_back}');
                                """)
            
            self.connection.commit()
        except ValueError as e:
            return e
        
    def get_flashcard_back(self, user_id: int, deck_name: str, flashcard_front: str):
        
        try:
            self.flashcard_not_exist(user_id, deck_name, flashcard_front)

            self.cursor.execute(f"""
                                SELECT flashcard_back 
                                FROM flashcards.flashcards
                                WHERE user_id = {user_id}
                                AND deck_name = '{deck_name}'
                                AND flashcard_front = '{flashcard_front}';
                                """)
            
            flashcard_back = self.cursor.fetchone()[0]

            return flashcard_back
        except ValueError as e:
            return e
        
    def delete_flashcard(self, user_id: int, deck_name: str, flashcard: str):

        try:
            self.deck_not_exist(user_id, deck_name)
            self.flashcard_not_exist(user_id, deck_name, flashcard)

            self.cursor.execute(f"""
                                DELETE FROM flashcards.flashcards 
                                WHERE user_id = {user_id}
                                AND flashcard_front = '{flashcard}'
                                AND deck_name = '{deck_name}';
                                """)
            
            self.connection.commit()
        except ValueError as e:
            return e
        
    def update_flashcard(self, user_id: int, deck_name: str, flashcard: str, new_flashcard_front: str, new_flashcard_back: str):

        try:
            self.deck_not_exist(user_id, deck_name)
            self.flashcard_not_exist(user_id, deck_name, flashcard)

            self.cursor.execute(f"""
                                UPDATE flashcards.flashcards
                                SET flashcard_front = '{new_flashcard_front}', flashcard_back = '{new_flashcard_back}'
                                WHERE deck_name = '{deck_name}'
                                AND user_id = {user_id}
                                AND flashcard_front = '{flashcard}';
                                """)
        except ValueError as e:
            return e

    def fetch_flashcards(self, user_id: int, deck_name: str):
        
        try:
            self.deck_not_exist(user_id, deck_name)

            self.cursor.execute(f"""
                                SELECT flashcard_front, flashcard_back
                                FROM flashcards.flashcards
                                WHERE user_id = {user_id}
                                AND deck_name = '{deck_name}';
                                """)
            
            flashcards = self.cursor.fetchall()

            return flashcards
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