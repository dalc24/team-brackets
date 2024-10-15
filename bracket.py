import random

"""

Class that handles Bracket functions including teams and bracket logic 

"""
class Bracket:
    def __init__(self):
        self.teams = []
        self.winners = []

    def setNumberTeams(self, numTeams):
        """
        Sets number of teams in bracket 
        
        numTeams is the integer amount of teams wanted. must be within constraints
        """
        # checks if valid number 
        if numTeams < 4 or numTeams > 32 or (numTeams & (numTeams - 1) != 0):
            raise ValueError("Invalid number of teams.")
        self.teams = [None] * numTeams
        self.winners = []

    def setTeamNames(self, index, teamName):
        """
        Sets names of teams in bracket

        index to indicate team number. teamName for user input name.
        """
        if 0 <= index < len(self.teams):
            self.teams[index] = teamName
        else:
            raise IndexError("index not available")
    
    def getTeamNames(self):
        """
        Gets names of all teams in bracket
        """
        return self.teams

    def createBracket(self):
        """
        Creates initial bracket separating teams for left side and right side
        """
        # cuts the team in half for left side and right side
        middle = len(self.teams) // 2
        leftSide = self.teams[:middle]
        rightSide = self.teams[middle:]

        #randomizes teams
        random.shuffle(leftSide)
        random.shuffle(rightSide)

        return leftSide, rightSide

    def displayBracket(self, leftSide, rightSide):
        """
        Displays full bracket including leftSide and rightSide 

        leftSide holds the teams in the left side of bracket
        rightSide holds the teams in the right side of the bracket
        """
        print("\n** Tournament Bracket **")

        print("\nLeft Side:")
        for i in range(0, len(leftSide), 2):
            print(f"Match {i // 2 + 1}: {leftSide[i]} vs {leftSide[i+1]}")


        print("\nRight Side:")
        for i in range(0, len(rightSide), 2):
            print(f"Match {i // 2 + 1}: {rightSide[i]} vs {rightSide[i+1]}")
    
    def displayLeftBracket(self, leftSide):
        """
        Displays only leftSide of bracket

        leftSide holds the teams in the left side of bracket
        """
        print("\n*Left Side Bracket*\n")
        for i in range(0, len(leftSide), 2):
            print(f"Match {i // 2 + 1}: {leftSide[i]} vs {leftSide[i+1]}")


    def displayRightBracket(self, rightSide):
        """
        Displays only leftSide of bracket

        rightSide holds the teams in the right side of the bracket
        """
        print("\n*Right Side Bracket*\n")
        for i in range(0, len(rightSide), 2):
            print(f"Match {i // 2 + 1}: {rightSide[i]} vs {rightSide[i+1]}")
    
    def chooseWinners(self, teams):
        """
        Takes input to choose winner in match 

        teams is the teams and their matches
        """
        winners = []

        for i in range(0, len(teams), 2):
            # sets up teams in match
            match = (teams[i], teams[i+1])
            while True:
                winner = input(f"\nChoose the winner for {match[0]} vs {match[1]}: ")
                if winner in match:
                    winners.append(winner)
                    break
                else:
                    print("Invalid winner. Please choose a valid team form the match")
        
        return winners
        
    def displayWinners(self, teams):
        """
        Displays the winners of a bracket

        teams is the winners of specified side 
        """
        print("\nWinners of this bracket:", teams)

    def playTournament(self):
        """
        Starts and plays the whole tournament by first creating the fill game bracket.
        Then proceeds to advance to next rounds.
        """
        # create the brackets
        leftSide, rightSide = self.createBracket()
        roundNum = 1
    
        self.displayBracket(leftSide, rightSide)

        #continue to run bracket
        while len(leftSide) > 1 or len(rightSide) > 1:
            print(f"\n-- Round {roundNum} -- ")

            # does left side first
            if len(leftSide) > 1:
                self.displayLeftBracket(leftSide)
                leftSide = self.chooseWinners(leftSide)
                self.displayWinners(leftSide)
                self.winners.append(leftSide)
            
            # does right side next
            if len(rightSide) > 1:
                self.displayRightBracket(rightSide)
                rightSide = self.chooseWinners(rightSide)
                self.displayWinners(rightSide)
                self.winners.append(rightSide)

            roundNum += 1

        
        #final match ot determine winner
        finalMatch = (leftSide[0], rightSide[0])
        print(f"\n-- Final Match --")
        print(f"Final: {finalMatch[0]} vs {finalMatch[1]}")
        while True: 
            finalWinner = input(f"Choose the final winner for {finalMatch[0]} vs {finalMatch[1]}: ")
            if finalWinner in finalMatch:
                print(f"\nFinal Winner: {finalWinner}")
                break
            else:
                print("Invalid team. Please choose a valid team from the match.")



        

    

        