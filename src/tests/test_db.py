from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
import pytest
from unittest.mock import Mock, patch
from database.service import Db

@pytest.fixture
def mock_db_connection():
    """Fixture to mock database connection and cursor"""
    with patch('database.service.psycopg2.connect') as mock_connect:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        yield mock_conn, mock_cursor


@pytest.fixture
def db_instance(mock_db_connection):
    """Fixture to create a Db instance with mocked connection"""
    mock_conn, mock_cursor = mock_db_connection
    with patch('database.service.load_dotenv'), patch('database.service.os.getenv', return_value="{}"):
        db = Db()
        return db


class TestDeckValidation:
    """Test deck existence validation methods"""
    
    def test_deck_not_exist_raises_error_when_deck_missing(self, db_instance):
        """Test that deck_not_exist raises ValueError when deck doesn't exist"""
        db_instance.cursor.fetchone.return_value = [False]
        
        with pytest.raises(ValueError, match="Deck 'test_deck' does not exist"):
            db_instance.deck_not_exist(1, 'test_deck')
    
    def test_deck_not_exist_passes_when_deck_exists(self, db_instance):
        """Test that deck_not_exist doesn't raise error when deck exists"""
        db_instance.cursor.fetchone.return_value = [True]
        
        # Should not raise any exception
        db_instance.deck_not_exist(1, 'test_deck')
    
    def test_deck_exist_raises_error_when_deck_present(self, db_instance):
        """Test that deck_exist raises ValueError when deck already exists"""
        db_instance.cursor.fetchone.return_value = [True]
        
        with pytest.raises(ValueError, match="Deck 'test_deck' already exist"):
            db_instance.deck_exist(1, 'test_deck')
    
    def test_deck_exist_passes_when_deck_missing(self, db_instance):
        """Test that deck_exist doesn't raise error when deck doesn't exist"""
        db_instance.cursor.fetchone.return_value = [False]
        
        # Should not raise any exception
        db_instance.deck_exist(1, 'test_deck')


class TestVocabValidation:
    """Test vocabulary existence validation methods"""
    
    def test_vocab_not_exist_raises_error_when_vocab_missing(self, db_instance):
        """Test that vocab_not_exist raises ValueError when vocab doesn't exist"""
        db_instance.cursor.fetchone.return_value = [False]
        
        with pytest.raises(ValueError, match="Vocab 'hello' does not exist"):
            db_instance.vocab_not_exist(1, 'test_deck', 'hello')
    
    def test_vocab_not_exist_passes_when_vocab_exists(self, db_instance):
        """Test that vocab_not_exist doesn't raise error when vocab exists"""
        db_instance.cursor.fetchone.return_value = [True]
        
        # Should not raise any exception
        db_instance.vocab_not_exist(1, 'test_deck', 'hello')
    
    def test_vocab_exist_raises_error_when_vocab_present(self, db_instance):
        """Test that vocab_exist raises ValueError when vocab already exists"""
        db_instance.cursor.fetchone.return_value = [True]
        
        with pytest.raises(ValueError, match="Vocab 'hello' already exist"):
            db_instance.vocab_exist(1, 'test_deck', 'hello')
    
    def test_vocab_exist_passes_when_vocab_missing(self, db_instance):
        """Test that vocab_exist doesn't raise error when vocab doesn't exist"""
        db_instance.cursor.fetchone.return_value = [False]
        
        # Should not raise any exception
        db_instance.vocab_exist(1, 'test_deck', 'hello')


class TestCreateDeck:
    """Test deck creation functionality"""
    
    def test_create_deck_success(self, db_instance):
        """Test successful deck creation"""
        db_instance.cursor.fetchone.return_value = [False]
        
        result = db_instance.create_deck(1, 'new_deck')
        
        assert result is None
        db_instance.cursor.execute.assert_called()
        db_instance.connection.commit.assert_called_once()
    
    def test_create_deck_already_exists(self, db_instance):
        """Test creating a deck that already exists returns error"""
        db_instance.cursor.fetchone.return_value = [True]
        
        result = db_instance.create_deck(1, 'existing_deck')
        
        assert isinstance(result, ValueError)
        assert "already exist" in str(result)
        db_instance.connection.commit.assert_not_called()


class TestDeleteDeck:
    """Test deck deletion functionality"""
    
    def test_delete_deck_success(self, db_instance):
        """Test successful deck deletion"""
        db_instance.cursor.fetchone.return_value = [True]
        
        result = db_instance.delete_deck(1, 'test_deck')
        
        assert result is None
        assert db_instance.cursor.execute.call_count >= 2  # DELETE from both tables
        db_instance.connection.commit.assert_called_once()
    
    def test_delete_deck_not_exists(self, db_instance):
        """Test deleting a deck that doesn't exist returns error"""
        db_instance.cursor.fetchone.return_value = [False]
        
        result = db_instance.delete_deck(1, 'nonexistent_deck')
        
        assert isinstance(result, ValueError)
        assert "does not exist" in str(result)
        db_instance.connection.commit.assert_not_called()


class TestUpdateDeckName:
    """Test deck name update functionality"""
    
    def test_update_deck_name_success(self, db_instance):
        """Test successful deck name update"""
        db_instance.cursor.fetchone.return_value = [True]
        
        result = db_instance.update_deck_name(1, 'old_deck', 'new_deck')
        
        assert result is None
        assert db_instance.cursor.execute.call_count >= 2  # UPDATE both tables
        db_instance.connection.commit.assert_called_once()
    
    def test_update_deck_name_not_exists(self, db_instance):
        """Test updating a deck that doesn't exist returns error"""
        db_instance.cursor.fetchone.return_value = [False]
        
        result = db_instance.update_deck_name(1, 'nonexistent_deck', 'new_name')
        
        assert isinstance(result, ValueError)
        assert "does not exist" in str(result)
        db_instance.connection.commit.assert_not_called()


class TestAddVocab:
    """Test vocabulary addition functionality"""
    
    def test_add_vocab_success(self, db_instance):
        """Test successful vocabulary addition"""
        # First call checks deck exists, second call checks vocab doesn't exist
        db_instance.cursor.fetchone.side_effect = [[True], [False]]
        
        result = db_instance.add_vocab(1, 'hello', 'greeting', 'test_deck')
        
        assert result is None
        db_instance.cursor.execute.assert_called()
        db_instance.connection.commit.assert_called_once()
    
    def test_add_vocab_deck_not_exists(self, db_instance):
        """Test adding vocab to non-existent deck returns error"""
        db_instance.cursor.fetchone.return_value = [False]
        
        result = db_instance.add_vocab(1, 'hello', 'greeting', 'nonexistent_deck')
        
        assert isinstance(result, ValueError)
        assert "does not exist" in str(result)
        db_instance.connection.commit.assert_not_called()
    
    def test_add_vocab_already_exists(self, db_instance):
        """Test adding duplicate vocabulary returns error"""
        # Deck exists, vocab exists
        db_instance.cursor.fetchone.side_effect = [[True], [True]]
        
        result = db_instance.add_vocab(1, 'hello', 'greeting', 'test_deck')
        
        assert isinstance(result, ValueError)
        assert "already exist" in str(result)
        db_instance.connection.commit.assert_not_called()


class TestDeleteVocab:
    """Test vocabulary deletion functionality"""
    
    def test_delete_vocab_success(self, db_instance):
        """Test successful vocabulary deletion"""
        # Deck exists, vocab exists
        db_instance.cursor.fetchone.side_effect = [[True], [True]]
        
        result = db_instance.delete_vocab(1, 'hello', 'test_deck')
        
        assert result is None
        db_instance.cursor.execute.assert_called()
        db_instance.connection.commit.assert_called_once()
    
    def test_delete_vocab_not_exists(self, db_instance):
        """Test deleting non-existent vocab returns error"""
        # Deck exists, vocab doesn't exist
        db_instance.cursor.fetchone.side_effect = [[True], [False]]
        
        result = db_instance.delete_vocab(1, 'hello', 'test_deck')
        
        assert isinstance(result, ValueError)
        assert "does not exist" in str(result)
        db_instance.connection.commit.assert_not_called()


class TestUpdateWord:
    """Test vocabulary update functionality"""
    
    def test_update_word_success(self, db_instance):
        """Test successful vocabulary update"""
        # Deck exists, vocab exists
        db_instance.cursor.fetchone.side_effect = [[True], [True]]
        
        result = db_instance.update_word(1, 'test_deck', 'hello', 'hi', 'casual greeting')
        
        assert result is None
        db_instance.cursor.execute.assert_called()
    
    def test_update_word_deck_not_exists(self, db_instance):
        """Test updating word in non-existent deck returns error"""
        db_instance.cursor.fetchone.return_value = [False]
        
        result = db_instance.update_word(1, 'nonexistent_deck', 'hello', 'hi', 'greeting')
        
        assert isinstance(result, ValueError)
        assert "does not exist" in str(result)
    
    def test_update_word_vocab_not_exists(self, db_instance):
        """Test updating non-existent vocab returns error"""
        # Deck exists, vocab doesn't exist
        db_instance.cursor.fetchone.side_effect = [[True], [False]]
        
        result = db_instance.update_word(1, 'test_deck', 'nonexistent', 'new', 'def')
        
        assert isinstance(result, ValueError)
        assert "does not exist" in str(result)


class TestFetchVocab:
    """Test vocabulary fetching functionality"""
    
    def test_fetch_vocab_success(self, db_instance, capsys):
        """Test successful vocabulary fetching"""
        mock_deck_data = [(1, 'deck1'), (1, 'deck2')]
        mock_flashcard_data = [(1, 'deck1', 'hello', 'greeting')]
        
        db_instance.cursor.fetchall.side_effect = [mock_deck_data, mock_flashcard_data]
        
        db_instance.fetch_vocab()
        
        captured = capsys.readouterr()
        assert "Data from Decks:-" in captured.out
        assert "Data from Flashcards:-" in captured.out
        assert db_instance.cursor.execute.call_count == 2


class TestSQLInjectionProtection:
    """Test SQL injection vulnerability (current implementation is vulnerable)"""
    
    def test_sql_injection_in_deck_name(self, db_instance):
        """Test that SQL injection in deck name is a concern"""
        malicious_deck_name = "test'; DROP TABLE flashcards.user_decks; --"
        db_instance.cursor.fetchone.return_value = [False]
        
        # This test documents the vulnerability - the code should use parameterized queries
        db_instance.create_deck(1, malicious_deck_name)
        
        # Check that the malicious string was passed to execute
        call_args = db_instance.cursor.execute.call_args[0][0]
        assert malicious_deck_name in call_args


if __name__ == "__main__":
    pytest.main([__file__, "-v"])