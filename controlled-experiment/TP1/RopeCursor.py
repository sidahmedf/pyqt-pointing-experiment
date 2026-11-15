from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt
from .BubbleCursor import BubbleCursor


class RopeCursor(BubbleCursor):

    def __init__(self, targets):
        super().__init__(targets)
        self.ropeColor = QColor("#4169E1")

    def paint(self, painter):

        painter.setRenderHint(QPainter.Antialiasing)

        if self.closest:

            pen = QPen(self.ropeColor)
            pen.setWidth(3)
            pen.setStyle(Qt.SolidLine)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)

            painter.drawLine(int(self.x), int(self.y),
                             int(self.closest.x), int(self.closest.y))


            painter.setBrush(QBrush(self.ropeColor))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(int(self.x) - 4, int(self.y) - 4, 8, 8)