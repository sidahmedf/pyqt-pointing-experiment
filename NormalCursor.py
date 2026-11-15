from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt
import math


class NormalCursor:
    def __init__(self, targets):
        self.x = 0
        self.y = 0
        self.targets = targets
        self.hovered_target = None  #au lieu de closest

        self.cursorColor = QColor("black")

    def paint(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.cursorColor))
        painter.setPen(Qt.NoPen)

        radius = 4
        painter.drawEllipse(self.x - radius, self.y - radius, radius * 2, radius * 2)

    def move(self, x, y):
        self.x = x
        self.y = y

        if self.hovered_target:
            self.hovered_target.highlighted = False
            self.hovered_target = None

        for target in self.targets:

            dist = math.sqrt((self.x - target.x) ** 2 + (self.y - target.y) ** 2)

            if dist <= (target.size / 2):
                self.hovered_target = target
                target.highlighted = True
                break