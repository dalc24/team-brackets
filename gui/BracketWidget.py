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
        self.finalWinner = []

        

        self.finalMatchLabel = None 

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
        self.mainLayout.addLayout(self.leftMatchLayout, 1, 0)  # Adjusted row to 1
        self.mainLayout.addLayout(self.rightMatchLayout, 1, 1)

        # initial matches
        self.displayMatches(self.leftTeams, self.leftMatchLayout, "Left Matches")
        self.displayMatches(self.rightTeams, self.rightMatchLayout, "Right Matches")

        # winners display
        self.winnersList = QListWidget()
        self.winnersList.setStyleSheet("background-color: #1e1e1e; color: white;")
        self.mainLayout.addWidget(self.winnersList, 2, 0, 1, 2)  # Adjusted row to 2

        # next round matchups
        self.nextRoundButton = QPushButton("Next Round")
        self.nextRoundButton.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.nextRoundButton.clicked.connect(self.startNextRound)
        self.mainLayout.addWidget(self.nextRoundButton, 3, 0, 1, 2)  # Adjusted row to 3

        # for final champ
        self.championLabel = QLabel("")
        self.championLabel.setAlignment(Qt.AlignCenter)
        self.championLabel.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFD700;")  # Gold color
        self.mainLayout.addWidget(self.championLabel, 4, 0, 1, 2)  # Adjusted row to 4

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
        selected_team = label.text()

        # opponent's team label 
        opponent_label = label.parent().findChildren(QLabel)
        opponent_label.remove(label)  
        opponent_team = opponent_label[0].text()

        # reset style
        if opponent_label[0].styleSheet() == "background-color: #4CAF50; padding: 8px; color: white; border-radius: 4px;":
            opponent_label[0].setStyleSheet("background-color: #3b3b3b; padding: 8px; color: white; border-radius: 4px;")
        
        # style of selected label
        label.setStyleSheet("background-color: #4CAF50; padding: 8px; color: white; border-radius: 4px;")

        # remove the opponent from the winners list if already theree
        if side == "left" and opponent_team in self.leftWinners:
            self.leftWinners.remove(opponent_team)
        elif side == "right" and opponent_team in self.rightWinners:
            self.rightWinners.remove(opponent_team)

        # add to winners list
        if side == "left" and selected_team not in self.leftWinners:
            self.leftWinners.append(selected_team)
        elif side == "right" and selected_team not in self.rightWinners:
            self.rightWinners.append(selected_team)

        print(f"Winner selected: {selected_team}")
        self.updateWinnersList()

    def updateWinnersList(self):
        self.winnersList.clear()
        self.winnersList.addItems(self.leftWinners + self.rightWinners)

    def startNextRound(self):
        if len(self.leftWinners) == 1 and len(self.rightWinners) == 1:
            self.displayFinalMatch()
            return

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

    def displayFinalMatch(self):
        # clear layout except for specific widgets
        self.clearLayoutExcept(self.mainLayout, [self.winnersList, self.championLabel])

        # remove final match label 
        if self.finalMatchLabel:
            self.finalMatchLabel.deleteLater()

        # create and style the final match label
        self.finalMatchLabel = QLabel('<span style="color: #FFD700;">Final</span> <span style="color: white;">Match</span>')
        self.finalMatchLabel.setAlignment(Qt.AlignCenter)
        self.finalMatchLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.mainLayout.addWidget(self.finalMatchLabel, 0, 0, 1, 2)  # Add it at the top

        # clear winners list and prepare final teams
        self.winnersList.clear()
        finalTeam1 = self.leftWinners[0] if self.leftWinners else "No Team"
        finalTeam2 = self.rightWinners[0] if self.rightWinners else "No Team"

        # create final match box
        finalMatchBox = self.createMatchBox(finalTeam1, finalTeam2)

        # assign mousePressEvent to the team labels
        labels = finalMatchBox.findChildren(QLabel)
        for label in labels:
            label.mousePressEvent = lambda event, lbl=label: self.selectFinalWinnerFromLabel(lbl)

        # add final match box to the layout
        finalLayout = QVBoxLayout()
        finalLayout.addWidget(finalMatchBox)
        finalLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.addLayout(finalLayout, 1, 0, 1, 2)

    def selectFinalWinnerFromLabel(self, label):
        parentBox = label.parent()

        labels = parentBox.findChildren(QLabel)
        for lbl in labels:
            lbl.setStyleSheet("background-color: #3b3b3b; padding: 8px; color: white; border-radius: 4px;")
        label.setStyleSheet("background-color: #4CAF50; padding: 8px; color: white; border-radius: 4px;")

        # update the final winner
        self.finalWinner = [label.text()]
        self.winnersList.clear()
        self.winnersList.addItems(self.finalWinner)
        self.displayWinner(label.text())

    def displayWinner(self, teamName):

        if self.championLabel:
            self.championLabel.setText(f"WINNER: {teamName}")
        
        # create the new button
        nextButton = QPushButton("New Bracket")
        nextButton.setStyleSheet("background-color: #4CAF50; padding: 8px; color: white; border-radius: 4px;")
        nextButton.setMaximumSize(100, 50)  # Minimum width and height
        nextButton.clicked.connect(self.goToSetNums)

        self.mainLayout.addWidget(nextButton, 4, 1)
        
    def clearLayoutExcept(self, layout, keepWidgets):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget and widget not in keepWidgets:
                widget.deleteLater()

    def goToSetNums(self):
        from gui.SetNumTeamWidnow import BracketApp  
        self.setNumTeamNumber = BracketApp()
        self.setNumTeamNumber.show()
        self.close()



def main():
    app = QApplication(sys.argv)
    leftSide = ['Team A', 'Team B', 'Team C', 'Team D']
    rightSide = ['Team E', 'Team F', 'Team G', 'Team H']
    
    window = BracketWindow(leftSide, rightSide)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
