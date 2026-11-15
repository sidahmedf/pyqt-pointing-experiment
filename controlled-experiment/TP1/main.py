import sys 
from PyQt5.QtWidgets import QApplication, QMainWindow
from BubbleWidget import BubbleWidget
from NormalWidget import NormalWidget


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bonjour")
        self.resize(1024, 800)
        
        self.display = BubbleWidget()
        #self.display = NormalWidget()

        self.setCentralWidget(self.display)




def main() :

    app = QApplication(sys.argv)

    window = MyWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__" :
    main()
