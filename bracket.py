import random 

class Bracket:
    def __init__(self):
        self.teams = []
        self.winners = []

    def setTeams(self, numTeams):
        if numTeams < 4 or numTeams > 32 or (numTeams & (numTeams-1) != 0):
            raise ValueError("Invalid number of teams.")
        self.teams = [None] * numTeams
        self.winners = []
    
    def setTeamNames(self, index, name):
        if 0 <= index < len(self.teams):
            self.teams[index] = name
        else:
            raise IndexError("invalid team index")
    
    def getTeams(self):
        return self.teams
    
    def createBracket(self):
            random.shuffle(self.teams)
            bracket = []
            for i in range(0, len(self.teams), 2):
                bracket.append((self.teams[i], self.teams[i + 1]))
            return bracket
        
    def displayBracket(self):
        bracket = self.createBracket() 
        print("Tournament Bracket:")
        for i, match in enumerate(bracket):
            print(f"Match {i + 1}: {match[0]} vs {match[1]}")