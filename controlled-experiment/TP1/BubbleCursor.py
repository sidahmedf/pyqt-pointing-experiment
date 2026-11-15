from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt


import math

class BubbleCursor () :

    def __init__(self,targets):
        self.defaultCol = QColor("#F0F0DB80")
        self.x = 0 
        self.y = 0 
        self.size = 10 
        self.targets = targets 
        self.closest = None 


    def paint(self, painter) :
        
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.defaultCol))
        painter.setPen(QColor("#000000"))
        #painter.setPen(Qt.NoPen)

        radius = int(self.size)
        diameter = int(self.size * 2)

        painter.drawEllipse(self.x - radius, self.y - radius, diameter, diameter) 


    def move(self, x, y ) :
        self.x = x
        self.y = y

        if self.closest:
            self.closest.highlighted = False

        # délégation
        self.closest = self._calculate_closest_target()

        if self.closest:
            self.closest.highlighted = True


    def _calculate_closest_target(self) :
        if not self.targets:
            return None

        nearest_target = None
        min_distance = 1000

        for target in self.targets:
            # Formule pour la distance (au centre): sqrt((x2-x1)^2 + (y2-y1)^2)
            dist_to_center = math.sqrt((self.x - target.x)**2 + (self.y - target.y)**2)
            
            dist_to_edge = dist_to_center - (target.size / 2)

            if dist_to_edge < min_distance:
                min_distance = dist_to_edge
                nearest_target = target

        if nearest_target:
            self.size = min_distance

        return nearest_target

