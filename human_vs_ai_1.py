import random
import pickle
import time


def save_ai(saved_ai):
    ai_file = open('ai_data.dat', 'wb')
    pickle.dump(saved_ai, ai_file)
    ai_file.close()


def open_ai():
    ai_file = open('ai_data.dat', 'rb')
    ai = pickle.load(ai_file)
    ai_file.close()
    return ai


def convert_list_to_tuple(grid):
    return tuple(tuple(row) for row in grid)


class Situation:
    def __init__(self, grid, options, chosen_option):
        self.grid = grid
        self.options = options
        self.chosen_option = chosen_option


class Option:
    def __init__(self, line, column, grade):
        self.line = line
        self.column = column
        self.grade = grade


def check_for_losers(plateau):
    for row in plateau:
        if all(cell != " " for cell in row):
            if all(cell == "O" for cell in row):
                return "O wins !"
            if all(cell == "X" for cell in row):
                return "X wins !"

    for col in range(3):
        if all(plateau[row][col] != " " for row in range(3)):
            if all(plateau[row][col] == "O" for row in range(3)):
                return "O wins !"
            if all(plateau[row][col] == "X" for row in range(3)):
                return "X wins !"
        # Check main diagonal
    if all(plateau[i][i] != " " for i in range(3)):
        if all(plateau[i][i] == "O" for i in range(3)):
            return "O wins !"
        if all(plateau[i][i] == "X" for i in range(3)):
            return "X wins !"
        # Check anti-diagonal
    if all(plateau[i][2 - i] != " " for i in range(3)):
        if all(plateau[i][2 - i] == "O" for i in range(3)):
            return "O wins !"
        if all(plateau[i][2 - i] == "X" for i in range(3)):
            return "X wins !"

    if all(cell != " " for row in plateau for cell in row):
        return "Equality !"

    return "No winner"


def print_board(plateau):
    print("  |  ".join(plateau[0]))
    print("-" * 14)
    print("  |  ".join(plateau[1]))
    print("-" * 14)
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
                if box == " ":
                    plateau[line][column] = sign
                    return plateau

                else:
                    print("This box has already a sign in it !")


class AI:
    def __init__(self, situations_list, history):
        self.situations_list = situations_list
        self.history = history

    def start_turn(self, grid, sign):
        tuple_grid = convert_list_to_tuple(grid)
        for selected_situation in self.situations_list:
            if (selected_situation.grid == tuple_grid and selected_situation.grid[0] == tuple_grid[0]
                    and selected_situation.grid[1] == tuple_grid[1] and selected_situation.grid[2] == tuple_grid[2]):
                # Ranking the best option
                if selected_situation.options:
                    sorted_options = sorted(selected_situation.options, key=lambda selected_option: selected_option.grade, reverse=True)
                    selected_situation.chosen_option = sorted_options[0]
                    modified_grid = self.play(selected_situation, grid, sign)
                    return modified_grid
                else:
                    return "Game conceded"
        # Unknown situation
        new_situation = Situation(grid, [], None)
        new_situation.grid = convert_list_to_tuple(new_situation.grid)
        line = 0
        for Line in grid:
            column = 0
            for Column in Line:
                if Column == " ":
                    new_option = Option(line, column, 0)
                    new_situation.options.append(new_option)
                column += 1
            line += 1
        random.shuffle(new_situation.options)
        new_situation.chosen_option = new_situation.options[0]
        self.situations_list.append(new_situation)
        modified_grid = self.play(new_situation, grid, sign)
        return modified_grid

    def play(self, new_situation, grid, sign):
        self.history.append(new_situation)
        grid[new_situation.chosen_option.line][new_situation.chosen_option.column] = sign
        return grid


ai = open_ai()

while True:
    # choice = input("Begin a new game ?")
    choice = input("Start a new game ?")
    if choice == "No":
        print("Data recording...")
        save_ai(ai)
        time.sleep(2)
        print("Data successfully recorded !")
        print("Goodbye !")
        exit()
    if choice == "Yes":
        # Reset the game
        board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]
        ai.history = []
        ai_lost = False

        print("Player 1 : X")
        print("Player 2 : O")
        print_board(board)
        while True:
            board = play("X", board)
            result = check_for_losers(board)
            if result != "No winner":
                print_board(board)
                print(result)
                if result == "X wins !":
                    ai_lost = True
                break
            board = ai.start_turn(board, "O")
            if board == "Game conceded":
                print("The AI concedes the game ! You won !")
                ai_lost = True
                break
            print_board(board)
            if board is list:
                result = check_for_losers(board)
            if result != "No winner":
                print(result)
                if result == "X wins !":
                    ai_lost = True
                break

        if ai_lost:
            last_situation = ai.history[-1]
            last_situation.options.remove(last_situation.chosen_option)
        else:
            for situation in ai.history:
                for option in situation.options:
                    if option == situation.chosen_option:
                        option.grade += 1
