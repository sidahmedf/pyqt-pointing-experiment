import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from ExpSetup import ExpSetup


class MainExp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expérience Contrôlée")
        self.resize(800, 600)

        self.dialog = ExpSetup()

        if self.dialog.exec_():
            user = self.dialog.user_id.value()
            tech = self.dialog.technique.currentText()
            dens = self.dialog.density.currentText()
            size = self.dialog.size.currentText()
            reps = self.dialog.repetitions.value()

            print(f"User: {user}, Tech: {tech}, Dens: {dens}, Size: {size}, Reps: {reps}")

            self.setCentralWidget(QLabel(f"Ready to launch: {tech}"))

        else:
            sys.exit()


def main():
    app = QApplication(sys.argv)
    window = MainExp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()