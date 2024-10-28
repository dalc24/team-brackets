import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout, QFrame, QListWidget, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class BracketWindow(QWidget):
    def __init__(self, leftSide, rightSide):
        super().__init__()
        self.leftTeams = leftSide
        self.rightTeams = rightSide
        
        self.leftWinners = []
        self.rightWinners = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tournament Bracket')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2b2b2b; color: white;")

        # main layout
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        # left and right side
        self.leftMatchLayout = QVBoxLayout()
        self.rightMatchLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.leftMatchLayout, 0, 0)
        self.mainLayout.addLayout(self.rightMatchLayout, 0, 1)

        # initial matches
        self.displayMatches(self.leftTeams, self.leftMatchLayout, "Left Matches")
        self.displayMatches(self.rightTeams, self.rightMatchLayout, "Right Matches")

        #  winners display
        self.winnersList = QListWidget()
        self.winnersList.setStyleSheet("background-color: #1e1e1e; color: white;")
        self.mainLayout.addWidget(self.winnersList, 1, 0, 1, 2)

        # next round matchups
        self.nextRoundButton = QPushButton("Next Round")
        self.nextRoundButton.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.nextRoundButton.clicked.connect(self.startNextRound)
        self.mainLayout.addWidget(self.nextRoundButton, 2, 0, 1, 2)

        # for final champ
        self.championLabel = QLabel("")
        self.championLabel.setAlignment(Qt.AlignCenter)
        self.championLabel.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFD700;")  # Gold color for the champion label
        self.mainLayout.addWidget(self.championLabel, 3, 0, 1, 2)

        self.show()

    def displayMatches(self, teams, layout, title):

        titleLabel = QLabel(title)
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        layout.addWidget(titleLabel)

        # clear previous matches
        for i in reversed(range(layout.count())): 
            widget = layout.itemAt(i).widget()
            if widget and widget != titleLabel:
                widget.deleteLater()

        # add matches in pairs
        for i in range(0, len(teams), 2):
            team1 = teams[i]
            team2 = teams[i + 1] if i + 1 < len(teams) else "Bye"
            matchBox = self.createMatchBox(team1, team2)
            layout.addWidget(matchBox)

    def createMatchBox(self, team1, team2):
        matchWidget = QFrame()
        matchWidget.setFrameShape(QFrame.Box)
        matchWidget.setLineWidth(2)
        matchWidget.setStyleSheet("background-color: #1e1e1e; border: 2px solid #444; color: white;")

        matchLayout = QVBoxLayout()

        # team labels
        team1Label = QLabel(team1)
        team1Label.setAlignment(Qt.AlignCenter)
        team1Label.setStyleSheet("background-color: #3b3b3b; padding: 8px; color: white; border-radius: 4px;")
        team1Label.mousePressEvent = lambda event, lbl=team1Label: self.selectWinner(lbl, side="left" if team1 in self.leftTeams else "right")

        team2Label = QLabel(team2)
        team2Label.setAlignment(Qt.AlignCenter)
        team2Label.setStyleSheet("background-color: #3b3b3b; padding: 8px; color: white; border-radius: 4px;")
        team2Label.mousePressEvent = lambda event, lbl=team2Label: self.selectWinner(lbl, side="left" if team2 in self.leftTeams else "right")

        # separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #555;") 


        matchLayout.addWidget(team1Label)
        matchLayout.addWidget(line)
        matchLayout.addWidget(team2Label)
        matchWidget.setLayout(matchLayout)

        return matchWidget


    def selectWinner(self, label, side):
        label.setStyleSheet("background-color: #4CAF50; padding: 8px; color: white; border-radius: 4px;") 

        # update winners based on side
        if side == "left" and label.text() not in self.leftWinners:
            self.leftWinners.append(label.text())
        elif side == "right" and label.text() not in self.rightWinners:
            self.rightWinners.append(label.text())

        self.updateWinnersList()

    def updateWinnersList(self):
        self.winnersList.clear()
        self.winnersList.addItems(self.leftWinners + self.rightWinners)

    def startNextRound(self):
        if len(self.leftWinners) == 1 and len(self.rightWinners) == 1:
            self.displayFinalMatch()
            return
        
        # uneven winners
        if len(self.leftWinners) % 2 != 0 or len(self.rightWinners) % 2 != 0:
            QMessageBox.warning(self, "Cannot Proceed", "Uneven winners. Cannot create matches.")
            return

        # next round
        random.shuffle(self.leftWinners)
        random.shuffle(self.rightWinners)
        self.leftTeams = self.leftWinners
        self.rightTeams = self.rightWinners
        self.leftWinners = []
        self.rightWinners = []

        # reset
        self.displayMatches(self.leftTeams, self.leftMatchLayout, "Left Matches")
        self.displayMatches(self.rightTeams, self.rightMatchLayout, "Right Matches")
        self.updateWinnersList()

    #Need to fix
    """
    def displayFinalMatch(self):
        while self.mainLayout.count():
            item = self.mainLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                sublayout = item.layout()
                if sublayout:
                    while sublayout.count():
                        subitem = sublayout.takeAt(0)
                        subwidget = subitem.widget()
                        if subwidget:
                            subwidget.deleteLater()

        finalTeam1 = self.leftWinners[0] if self.leftTeams else "No Team"
        finalTeam2 = self.rightWinners[0] if self.rightTeams else "No Team"

        finalMatchBox = self.createMatchBox(finalTeam1, finalTeam2)

        finalLayout = QVBoxLayout()
        finalLayout.addWidget(finalMatchBox)
        finalLayout.setAlignment(Qt.AlignCenter)

        self.mainLayout.addLayout(finalLayout, 0, 0, 1, 2)

        self.update()
        self.repaint()
    """


def main():
    app = QApplication(sys.argv)
    leftSide = ['Team A', 'Team B', 'Team C', 'Team D']
    rightSide = ['Team E', 'Team F', 'Team G', 'Team H']
    
    window = BracketWindow(leftSide, rightSide)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
