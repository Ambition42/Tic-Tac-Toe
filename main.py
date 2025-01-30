def check_for_losers(plateau):
    for row in plateau:
        if all(cell != "" for cell in row):
            if all(cell == "O" for cell in row):
                return "O wins !"
            if all(cell == "X" for cell in row):
                return "X wins !"

    for col in range(3):
        if all(plateau[row][col] != "" for row in range(3)):
            if all(plateau[row][col] == "O" for row in range(3)):
                return "O wins !"
            if all(plateau[row][col] == "X" for row in range(3)):
                return "X wins !"
        # Check main diagonal
    if all(plateau[i][i] != "" for i in range(3)):
        if all(plateau[i][i] == "O" for i in range(3)):
            return "O wins !"
        if all(plateau[i][i] == "X" for i in range(3)):
            return "X wins !"
        # Check anti-diagonal
    if all(plateau[i][2 - i] != "" for i in range(3)):
        if all(plateau[i][2 - i] == "O" for i in range(3)):
            return "O wins !"
        if all(plateau[i][2 - i] == "X" for i in range(3)):
            return "X wins !"

    if all(cell != "" for row in plateau for cell in row):
        return "Égalité"

    return "No winner"


def print_board(plateau):
    print("  |  ".join(plateau[0]))
    print("-" * 12)
    print("  |  ".join(plateau[1]))
    print("-" * 12)
    print("  |  ".join(plateau[2]))

def play(sign, plateau):
    correct_choice = False
    while not correct_choice:
        choice_line = input("Enter line number : ")
        if choice_line == "1" or choice_line == "2" or choice_line == "3":
            line = int(choice_line)
            line -= 1
            choice_column = input("Enter column number : ")
            if choice_column == "1" or choice_column == "2" or choice_column == "3":
                column = int(choice_column)
                column -= 1

                box = plateau[line][column]
                if box == "":
                    plateau[line][column] = sign
                    return plateau

                else:
                    print("This box has already a sign in it !")


while True:
    choice = input("Begin a new game ?")
    if choice == "Yes":
        board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        print("Player 1 : X")
        print("Player 2 : O")
        print_board(board)
        while True:
            board = play("X", board)
            print_board(board)
            result = check_for_losers(board)
            if result != "No winner":
                print(result)
                break
            board = play("O", board)
            print_board(board)
            result = check_for_losers(board)
            if result != "No winner":
                print(result)
                break
    if choice == "No":
        exit()









