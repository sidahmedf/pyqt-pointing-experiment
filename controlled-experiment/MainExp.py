import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from ExpSetup import ExpSetup
from XPManager import XPManager

import os

sys.path.append(os.path.abspath("/TP1"))

from TP1.BubbleWidget import BubbleWidget
from TP1.RopeWidget import RopeWidget
from TP1.NormalWidget import NormalWidget


class MainExpWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expérience Contrôlée")
        self.resize(1024, 800)
        self.dialog = ExpSetup()
        if self.dialog.exec_() :

            data = {
                'user_id': self.dialog.get_user_id(),
                'technique': self.dialog.get_technique(),
                'repetitions': self.dialog.get_repetitions(),

            }

            print(f"Lancement: User {data['user_id']}, Technique: {data['technique']}")
                

            if data['technique'] == "Bubble":
                self.display = BubbleWidget()
            elif data['technique'] == "Rope":
                self.display = RopeWidget()
            else:
                self.display = NormalWidget()
                
            self.setCentralWidget(self.display)
                
            self.manager = XPManager(data, self.display, self)
                
            self.display.manager = self.manager
        else :
            sys.exit()            
               
    
def main():
    app = QApplication(sys.argv)
    window = MainExpWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()