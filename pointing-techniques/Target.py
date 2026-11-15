from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt

class Target :

    def __init__(self, x, y, size):
        self.defaultCol = QColor("#213448")
        self.highlightCol = QColor("#32CD32")
        self.toSelectCol  = QColor("#FF0000")
        self.x = x
        self.y = y 
        self.size = size 
        self.toSelect =  False
        self.highlighted = False 


    def paint(self, painter) :
        
        painter.setRenderHint(QPainter.Antialiasing)

        if self.toSelect :
            painter.setBrush(QBrush(self.toSelectCol))
        elif self.highlighted :
            painter.setBrush(QBrush(self.highlightCol))
        else : 
            painter.setBrush(QBrush(self.defaultCol))

            
        painter.setPen(Qt.NoPen)

        radius = self.size//2

        painter.drawEllipse(self.x - radius, self.y - radius, self.size, self.size)
        
