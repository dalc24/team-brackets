import sys
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QApplication
)
from PyQt5.QtCore import Qt
from gui.SetNumTeamWindow import BracketApp 

class IntroWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # window size and title
        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle('Welcome to Brackets')
        self.setStyleSheet('background-color: #2b2b2b;')

        # main layout
        self.layout = QVBoxLayout()

        # label for welcome
        self.label = QLabel("Welcome to Brackets!")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 32px; font-weight: bold; color: white;") 
        self.layout.addWidget(self.label)

        # button for start
        self.startButton = QPushButton("Start")
        self.startButton.setFixedSize(150, 40)
        self.startButton.setStyleSheet("font-size: 14px; background-color: #4CAF50; color: white;")
        self.startButton.clicked.connect(self.goToSetNums)
        self.layout.addWidget(self.startButton, alignment=Qt.AlignCenter)

        # Set the layout
        self.setLayout(self.layout)
        self.show() 
    
    def goToSetNums(self):
        self.setNumTeamNumber = BracketApp()  
        self.setNumTeamNumber.show() 
        self.close()


