from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
import pytest
from unittest.mock import patch, MagicMock
import sys

# Mock the database connection before importing db module
mock_connect = MagicMock()
mock_conn = MagicMock()
mock_cursor = MagicMock()
mock_connect.return_value = mock_conn
mock_conn.cursor.return_value = mock_cursor

with patch('psycopg2.connect', mock_connect):
    from database.db import Db


@pytest.fixture
def db_instance():
    """Fixture to create a Db instance with mocked cursor."""
    db = Db()
    db.cursor = MagicMock()
    db.connection = MagicMock()
    return db


class TestDeckNotExist:
    def test_deck_exists_no_error(self, db_instance):
        """Test that no error is raised when deck exists."""
        db_instance.cursor.fetchone.return_value = (True,)
        
        # Should not raise an error
        db_instance.deck_not_exist(1, "test_deck")
        
    def test_deck_does_not_exist_raises_error(self, db_instance):
        """Test that ValueError is raised when deck doesn't exist."""
        db_instance.cursor.fetchone.return_value = (False,)
        
        with pytest.raises(ValueError, match="Deck 'test_deck' does not exist"):
            db_instance.deck_not_exist(1, "test_deck")


class TestFlashcardNotExist:
    def test_flashcard_exists_no_error(self, db_instance):
        """Test that no error is raised when flashcard exists."""
        db_instance.cursor.fetchone.return_value = (True,)
        
        # Should not raise an error
        db_instance.flashcard_not_exist(1, "test_deck", "test_flashcard")
        
    def test_flashcard_does_not_exist_raises_error(self, db_instance):
        """Test that ValueError is raised when flashcard doesn't exist."""
        db_instance.cursor.fetchone.return_value = (False,)
        
        with pytest.raises(ValueError, match="flashcard 'test_flashcard' does not exist"):
            db_instance.flashcard_not_exist(1, "test_deck", "test_flashcard")


class TestDeckExist:
    def test_deck_does_not_exist_no_error(self, db_instance):
        """Test that no error is raised when deck doesn't exist."""
        db_instance.cursor.fetchone.return_value = (False,)
        
        # Should not raise an error
        db_instance.deck_exist(1, "test_deck")
        
    def test_deck_exists_raises_error(self, db_instance):
        """Test that ValueError is raised when deck already exists."""
        db_instance.cursor.fetchone.return_value = (True,)
        
        with pytest.raises(ValueError, match="Deck 'test_deck' already exist"):
            db_instance.deck_exist(1, "test_deck")


class TestFlashcardExist:
    def test_flashcard_does_not_exist_no_error(self, db_instance):
        """Test that no error is raised when flashcard doesn't exist."""
        db_instance.cursor.fetchone.return_value = (False,)
        
        # Should not raise an error
        db_instance.flashcard_exist(1, "test_deck", "test_flashcard")
        
    def test_flashcard_exists_raises_error(self, db_instance):
        """Test that ValueError is raised when flashcard already exists."""
        db_instance.cursor.fetchone.return_value = (True,)
        
        with pytest.raises(ValueError, match="flashcard 'test_flashcard' already exist"):
            db_instance.flashcard_exist(1, "test_deck", "test_flashcard")


class TestCreateDeck:
    def test_create_deck_success(self, db_instance):
        """Test successful deck creation."""
        db_instance.cursor.fetchone.return_value = (False,)
        
        db_instance.create_deck(1, "new_deck")
        
        assert db_instance.cursor.execute.call_count == 2
        db_instance.connection.commit.assert_called_once()
        
    def test_create_deck_already_exists(self, db_instance):
        """Test that creating an existing deck raises ValueError."""
        db_instance.cursor.fetchone.return_value = (True,)
        
        with pytest.raises(ValueError, match="Deck 'existing_deck' already exist"):
            db_instance.create_deck(1, "existing_deck")


class TestDeleteDeck:
    def test_delete_deck_success(self, db_instance):
        """Test successful deck deletion."""
        db_instance.cursor.fetchone.return_value = (True,)
        
        db_instance.delete_deck(1, "test_deck")
        
        assert db_instance.cursor.execute.call_count == 3
        db_instance.connection.commit.assert_called_once()
        
    def test_delete_deck_not_exists(self, db_instance):
        """Test that deleting non-existent deck raises ValueError."""
        db_instance.cursor.fetchone.return_value = (False,)
        
        with pytest.raises(ValueError, match="Deck 'nonexistent_deck' does not exist"):
            db_instance.delete_deck(1, "nonexistent_deck")


class TestUpdateDeckName:
    def test_update_deck_name_success(self, db_instance):
        """Test successful deck name update."""
        db_instance.cursor.fetchone.return_value = (True,)
        
        db_instance.update_deck_name(1, "old_deck", "new_deck")
        
        assert db_instance.cursor.execute.call_count == 3
        db_instance.connection.commit.assert_called_once()
        
    def test_update_deck_name_not_exists(self, db_instance):
        """Test that updating non-existent deck raises ValueError."""
        db_instance.cursor.fetchone.return_value = (False,)
        
        with pytest.raises(ValueError, match="Deck 'nonexistent_deck' does not exist"):
            db_instance.update_deck_name(1, "nonexistent_deck", "new_deck")


class TestAddFlashcard:
    def test_add_flashcard_success(self, db_instance):
        """Test successful flashcard addition."""
        db_instance.cursor.fetchone.side_effect = [(True,), (False,)]
        
        db_instance.add_flashcard(1, "test_deck", "front", "back")
        
        assert db_instance.cursor.execute.call_count == 3
        db_instance.connection.commit.assert_called_once()
        
    def test_add_flashcard_deck_not_exists(self, db_instance):
        """Test that adding flashcard to non-existent deck raises ValueError."""
        db_instance.cursor.fetchone.return_value = (False,)
        
        with pytest.raises(ValueError, match="Deck 'nonexistent_deck' does not exist"):
            db_instance.add_flashcard(1, "nonexistent_deck", "front", "back")
            
    def test_add_flashcard_already_exists(self, db_instance):
        """Test that adding duplicate flashcard raises ValueError."""
        db_instance.cursor.fetchone.side_effect = [(True,), (True,)]
        
        with pytest.raises(ValueError, match="flashcard 'front' already exist"):
            db_instance.add_flashcard(1, "test_deck", "front", "back")


class TestFetchFlashcardBack:
    def test_fetch_flashcard_back_success(self, db_instance):
        """Test successful flashcard back retrieval."""
        db_instance.cursor.fetchone.side_effect = [(True,), ("back content",)]
        
        result = db_instance.fetch_flashcard_back(1, "test_deck", "front")
        
        assert result == "back content"
        
    def test_fetch_flashcard_back_not_exists(self, db_instance):
        """Test that fetching non-existent flashcard raises ValueError."""
        db_instance.cursor.fetchone.return_value = (False,)
        
        with pytest.raises(ValueError, match="flashcard 'nonexistent' does not exist"):
            db_instance.fetch_flashcard_back(1, "test_deck", "nonexistent")


class TestDeleteFlashcard:
    def test_delete_flashcard_success(self, db_instance):
        """Test successful flashcard deletion."""
        db_instance.cursor.fetchone.side_effect = [(True,), (True,)]
        
        db_instance.delete_flashcard(1, "test_deck", "flashcard")
        
        assert db_instance.cursor.execute.call_count == 3
        db_instance.connection.commit.assert_called_once()
        
    def test_delete_flashcard_deck_not_exists(self, db_instance):
        """Test that deleting flashcard from non-existent deck raises ValueError."""
        db_instance.cursor.fetchone.return_value = (False,)
        
        with pytest.raises(ValueError, match="Deck 'nonexistent_deck' does not exist"):
            db_instance.delete_flashcard(1, "nonexistent_deck", "flashcard")
            
    def test_delete_flashcard_not_exists(self, db_instance):
        """Test that deleting non-existent flashcard raises ValueError."""
        db_instance.cursor.fetchone.side_effect = [(True,), (False,)]
        
        with pytest.raises(ValueError, match="flashcard 'nonexistent' does not exist"):
            db_instance.delete_flashcard(1, "test_deck", "nonexistent")


class TestUpdateFlashcard:
    def test_update_flashcard_success(self, db_instance):
        """Test successful flashcard update."""
        db_instance.cursor.fetchone.side_effect = [(True,), (True,)]
        
        db_instance.update_flashcard(1, "test_deck", "old_front", "new_front", "new_back")
        
        assert db_instance.cursor.execute.call_count == 3
        
    def test_update_flashcard_deck_not_exists(self, db_instance):
        """Test that updating flashcard in non-existent deck raises ValueError."""
        db_instance.cursor.fetchone.return_value = (False,)
        
        with pytest.raises(ValueError, match="Deck 'nonexistent_deck' does not exist"):
            db_instance.update_flashcard(1, "nonexistent_deck", "old", "new_front", "new_back")
            
    def test_update_flashcard_not_exists(self, db_instance):
        """Test that updating non-existent flashcard raises ValueError."""
        db_instance.cursor.fetchone.side_effect = [(True,), (False,)]
        
        with pytest.raises(ValueError, match="flashcard 'nonexistent' does not exist"):
            db_instance.update_flashcard(1, "test_deck", "nonexistent", "new_front", "new_back")


class TestFetchFlashcards:
    def test_fetch_flashcards_success(self, db_instance):
        """Test successful flashcards retrieval."""
        db_instance.cursor.fetchone.return_value = (True,)
        db_instance.cursor.fetchall.return_value = [
            ("front1", "back1"),
            ("front2", "back2")
        ]
        
        result = db_instance.fetch_flashcards(1, "test_deck")
        
        assert len(result) == 2
        assert result[0] == ("front1", "back1")
        assert result[1] == ("front2", "back2")
        
    def test_fetch_flashcards_deck_not_exists(self, db_instance):
        """Test that fetching flashcards from non-existent deck raises ValueError."""
        db_instance.cursor.fetchone.return_value = (False,)
        
        with pytest.raises(ValueError, match="Deck 'nonexistent_deck' does not exist"):
            db_instance.fetch_flashcards(1, "nonexistent_deck")


class TestFetchDecks:
    def test_fetch_decks_success(self, db_instance):
        """Test successful decks retrieval."""
        db_instance.cursor.fetchall.return_value = [
            ("deck1",),
            ("deck2",),
            ("deck3",)
        ]
        
        result = db_instance.fetch_decks(1)
        
        assert len(result) == 3
        assert result[0] == ("deck1",)
        assert result[1] == ("deck2",)
        
    def test_fetch_decks_empty(self, db_instance):
        """Test fetching decks when user has no decks."""
        db_instance.cursor.fetchall.return_value = []
        
        result = db_instance.fetch_decks(1)
        
        assert result == []


class TestGetDeckLength:
    def test_get_deck_length_success(self, db_instance):
        """Test successful deck length retrieval."""
        db_instance.cursor.fetchone.side_effect = [(True,), (5,)]
        
        result = db_instance.get_deck_length(1, "test_deck")
        
        assert result == 5
        
    def test_get_deck_length_deck_not_exists(self, db_instance):
        """Test that getting length of non-existent deck raises ValueError."""
        db_instance.cursor.fetchone.return_value = (False,)
        
        with pytest.raises(ValueError, match="Deck 'nonexistent_deck' does not exist"):
            db_instance.get_deck_length(1, "nonexistent_deck")
            
    def test_get_deck_length_empty_deck(self, db_instance):
        """Test getting length of empty deck."""
        db_instance.cursor.fetchone.side_effect = [(True,), (0,)]
        
        result = db_instance.get_deck_length(1, "test_deck")
        
        assert result == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])