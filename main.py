from datetime import datetime
import csv
def addnew(pname):
    names = []
    with open("players.csv", mode="r+", newline="", encoding="utf-8") as playertable:
        for row in csv.reader(playertable): names.append(row[0])
        while pname in names: pname = input("Name already in Leaderboard\nEnter new name: ")
        csv.writer(playertable).writerow([pname, 0])
    return pname
def main():
    p, choice = [0, 0], input("""
               Tic-tac-toe Competition
------------------------------------------------------
A: Start game
B: Add player
C: View game history
D: Reset Leaderboard (Deletes all players and history)
Q: Quit
------------------------------------------------------
Please enter your choice: """)
    if choice.lower() == "a":
        leaderboard, num_rows = [[],[]], 0
        with open("players.csv", mode="r", newline="", encoding="utf-8") as playertable:
            header = next(csv.reader(playertable))
            print(f"{header[0]}\t{header[1]}")
            for row in csv.reader(playertable):
                leaderboard[0].append(row[0])
                leaderboard[1].append(int(row[1]))
                num_rows += 1
        if num_rows > 1: leaderboard[0], leaderboard[1] = zip(*sorted(list(zip(leaderboard[0],leaderboard[1])),key=lambda x: x[1], reverse=True))
        for n in range(2): leaderboard[n] = list(leaderboard[n]) 
        for l in range(len(leaderboard[0])): print(f"{leaderboard[0][l]}\t\t{leaderboard[1][l]}")
        if len(leaderboard[0]) == 0: print("-----------\t-----\n")
        for l,n in zip(("X","O"),(0,1)):
            while p[n] == 0:
                p[n] = input(f"Who will be {l}? ")
                if p[n] not in leaderboard[0]:
                    if input("Player not in Leaderboard.\nAdd new player? (y/n)") == "y":
                        leaderboard[0].append(addnew(p[n]))
                        leaderboard[1].append(0)
                    else: p[n] = 0
        players, again= {p[0]: 0, p[1]: 0}, "y"
        while again == "y":
            board, letter=[3*[" "] for i in range(3) ], "X"
            print("| 00 | 01 | 02 |\n| 10 | 11 | 12 |\n| 20 | 21 | 22 |")
            count=0
            while count <= 9:
                count +=1
                print(f"{p[0] if letter == 'X' else p[1]}'s Move")
                check, move, again= [], input("Location: "), "y"
                while move not in ("00", "01", "02", "10", "11", "12","20", "21", "22") or board[int(move[0:1])][int(move[1:])] in ("X","O"): move = input("Already full or Invalid input. New Location: ")
                board[int(move[:1])][int(move[1:])] = letter
                print(f"| {board[0][0]} | {board[0][1]} | {board[0][2]} |\n| {board[1][0]} | {board[1][1]} | {board[1][2]} |\n| {board[2][0]} | {board[2][1]} | {board[2][2]} |")
                letter = {"X":"O", "O":"X"}[letter]
                for n in range(3): check += board[n],[board[0][n],board[1][n],board[2][n]], [board[0][0],board[1][1],board[2][2]],[board[2][0],board[1][1],board[0][2]]
                for l,n in zip(("X","O"),(p[0],p[1])):
                    if [l,l,l] in check:
                        print(f"{n} Wins")
                        count = 10
                        players[n] += 1
                    if count == 9: print("Draw")
            again = input("Play again? (y/n) ").lower()
            while again not in ("y", "n"): again = input("Play again? (y/n) ").lower()
        print(f"{header[0]}\t{header[1]}")
        with open("players.csv", mode="w+", newline="", encoding="utf-8") as playertable:
            csv.writer(playertable).writerow(["Player Name","Score"])
            for key, value in players.items():
                print(f"{key}\t\t{value}")
                leaderboard[1][leaderboard[0].index(key)] += value
            for i in range(len(leaderboard[0])):csv.writer(playertable).writerow([leaderboard[0][i],leaderboard[1][i]])
        csv.writer(open("history.csv", mode="a", newline="", encoding="utf-8")).writerow([datetime.now().strftime("%d/%m/%Y %H:%M:%S"), p[0], players[p[0]], p[1], players[p[1]]])
    elif choice.lower() == "b": addnew(input("What is the player's name? "))
    elif choice.lower() == "c":
        for row in csv.reader(open("history.csv", newline="", encoding="utf-8"), delimiter=',', quotechar='|'): print(f"{row[0]}\t{row[1]} {row[2]}:{row[4]} {row[3]}")
    elif choice.lower() == "d":
        if input("Are you sure? (y/n) ").lower() == "y":
            csv.writer(open("players.csv", mode="w", newline="", encoding="utf-8")).writerow(["Player Name","Score"])
            csv.writer(open("history.csv", mode="w", newline="", encoding="utf-8")).writerow(["Date","\t\t","X"," ", "O"])
            print("\nLeaderboard RESET")
        else: print("\nLeaderboard NOT RESET")
    elif choice.lower() ==  "q": return 1
    else: print("You must only select either A,B,C,D, or Q.")
    return 0
if __name__ == '__main__':
    end = 0
    while end == 0: end = main()
