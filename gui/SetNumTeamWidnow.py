# main_window.py

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from gui.TeamNamesWindow import TeamNamesWindow 
from bracket import Bracket 

class BracketApp(QWidget):
    def __init__(self):
        super().__init__()
        self.bracket = Bracket()
        self.initUI()

    def initUI(self):
        # window size and title
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('Tournament Setup')
        self.setStyleSheet('background-color: #2b2b2b;')

        # layout 
        self.layout = QVBoxLayout()

        # lavbel for input
        self.label = QLabel('Enter number of teams:')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px; color: white;")
        self.layout.addWidget(self.label)

        # textbox for user input 
        self.teamInput = QLineEdit()
        self.teamInput.setFixedWidth(200)
        self.teamInput.setAlignment(Qt.AlignCenter)
        self.teamInput.setStyleSheet("font-size: 14px; padding: 5px; color: white")
        self.layout.addWidget(self.teamInput, alignment=Qt.AlignCenter)

        # next button
        self.nextButton = QPushButton('Next')
        self.nextButton.setFixedWidth(100)
        self.nextButton.setStyleSheet("font-size: 14px; padding: 5px; background-color: #4CAF50; color: white;")
        self.nextButton.clicked.connect(self.goToNextStep)
        self.layout.addWidget(self.nextButton, alignment=Qt.AlignCenter)

        # layout
        self.setLayout(self.layout)
        self.show()

    def goToNextStep(self):
        # gets users input 
        num_teams = self.teamInput.text()
        
        #ensures input satisfies coniditnos
        try:
            num_teams = int(num_teams)
            if num_teams < 4 or num_teams > 32 or (num_teams & (num_teams - 1) != 0):
                raise ValueError

            #calls bracket object to set number of teams 
            self.bracket.setNumberTeams(num_teams)
            
            # goes to next window
            self.close() 
            self.openTeamNamesWindow(num_teams)

        except ValueError:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Invalid Input')
            msg_box.setText('Please enter a valid number of teams (4, 8, 16, 32).')
            msg_box.setStyleSheet("color: white; background-color: #2b2b2b;")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

    def openTeamNamesWindow(self, num_teams):
        self.teamNamesWindow = TeamNamesWindow(num_teams, self.bracket)
        self.teamNamesWindow.show()


