from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt
from BubbleCursor import BubbleCursor


class RopeCursor(BubbleCursor):

    def __init__(self, targets):
        super().__init__(targets)
        self.ropeColor = QColor("black")

    def paint(self, painter):

        painter.setRenderHint(QPainter.Antialiasing)

        if self.closest:

            pen = QPen(self.ropeColor)
            pen.setWidth(2)
            pen.setStyle(Qt.SolidLine)
            painter.setPen(pen)

            painter.drawLine(int(self.x), int(self.y),
                             int(self.closest.x), int(self.closest.y))


            painter.setBrush(QBrush(self.ropeColor))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(int(self.x) - 3, int(self.y) - 3, 6, 6)