# main.py
from bracket import Bracket

def main():
    bracket = Bracket()
    
    while True:
        try:
            num_teams = int(input("Enter the number of teams. Pick [4, 8, 16, 32]: "))
            bracket.setTeams(num_teams)
            break  
        except ValueError as e:
            print(e) 

    for i in range(num_teams):
        team_name = input(f"Enter the name for Team {i + 1}: ")
        bracket.setTeamNames(i, team_name)

    # Display the bracket
    bracket.displayBracket()

if __name__ == "__main__":
    main()
