from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QComboBox, QSpinBox, QPushButton)

class ExpSetup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setup Expérience")
        self.resize(300, 250)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.user_id = QSpinBox()
        self.user_id.setRange(1, 999)
        self.add_option("User ID:", self.user_id)

        self.technique = QComboBox()
        self.technique.addItems(["Bubble", "Rope", "Normal"])
        self.add_option("Technique:", self.technique)

        self.density = QComboBox()
        self.density.addItems(["30","90"])
        self.add_option("Densité:", self.density)

        self.size = QComboBox()
        self.size.addItems(["8", "18"])
        self.add_option("Taille Cible:", self.size)

        self.repetitions = QSpinBox()
        self.repetitions.setRange(2, 50)
        self.repetitions.setValue(3)
        self.add_option("Répétitions:", self.repetitions)

        self.layout.addStretch()

        self.btn_start = QPushButton("Valider")
        self.btn_start.clicked.connect(self.accept)
        self.layout.addWidget(self.btn_start)

    def add_option(self, label_text, widget):

        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel(label_text))
        h_layout.addWidget(widget)
        self.layout.addLayout(h_layout)
        
    def get_user_id(self):
        return self.user_id.value()

    def get_technique(self):
        return self.technique.currentText()

    def get_density(self):
        return int(self.density.currentText())

    def get_size(self):
        return int(self.size.currentText())

    def get_repetitions(self):
        return self.repetitions.value()
