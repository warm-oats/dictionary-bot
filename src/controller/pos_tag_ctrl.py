from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.pos_tag_model import PosTagModel
from view.pos_tag_view import PosTagView

class PosTagController:

    def __init__(self):
        self.pos_tag_model = PosTagModel()
        self.pos_tag_view = PosTagView()