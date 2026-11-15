from .BubbleWidget import BubbleWidget
from .RopeCursor import RopeCursor

class RopeWidget(BubbleWidget):
    
    def __init__(self, manager=None):
        super().__init__(manager)
        
        self.cursor = RopeCursor(self.targets)