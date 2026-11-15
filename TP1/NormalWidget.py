from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QElapsedTimer
from .Target import Target
from .NormalCursor import NormalCursor
import random
import csv
import os


class NormalWidget(QWidget):
    def __init__(self, manager=None):
        super().__init__()
        self.manager = manager
        self.targets = []
        self.cursor = NormalCursor(self.targets)
        self.setMouseTracking(True)
        self.timer = QElapsedTimer()
        self.target_to_click = None

        if self.manager is None:
            current_dir = os.path.dirname(__file__)
            csv_path = os.path.join(current_dir, "src_tp_bubble.csv")

            self.load_csv(csv_path)
            self.select_new_target()

    def load_csv(self, filename):
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    self.targets.append(Target(int(parts[0]), int(parts[1]), int(parts[2])))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for target in self.targets:
            target.paint(painter)

        self.cursor.paint(painter)

    def mouseMoveEvent(self, event):
        self.cursor.move(event.x(), event.y())
        self.update()

    def mousePressEvent(self, event):

        if self.cursor.hovered_target == self.target_to_click:
            if self.manager:
                self.manager.handle_success()
            else:
                print(f"Temps: {self.timer.elapsed()} ms")
                self.select_new_target()
        else:
            if self.manager:
                self.manager.handle_error()
            else:
                print("Missed! pls try again")

    def select_new_target(self):
        if self.target_to_click:
            self.target_to_click.toSelect = False

        self.target_to_click = random.choice(self.targets)
        self.target_to_click.toSelect = True

        self.timer.start()
        self.update()
        
        
        
    def load_scenario(self, csv_filename, target_size=20):
        self.targets = []
        try:
            with open(csv_filename, "r") as file:
                reader = csv.reader(file)
                for line in reader:
                    if len(line) >= 3:
                        t_id = int(line[0])
                        x = int(line[1])
                        y = int(line[2])
                        
                        t = Target(x, y, target_size) 
                        t.id = t_id          
                        self.targets.append(t)
                        
            self.cursor.targets = self.targets
            self.update()
        except Exception as e:
            print(f"Error loading {csv_filename}: {e}")

    def set_active_target(self, target_id):
        if self.target_to_click:
            self.target_to_click.toSelect = False
            
        for t in self.targets:
            if getattr(t, 'id', -1) == target_id:
                t.toSelect = True
                self.target_to_click = t
                break
                
        self.timer.start()
        self.update()