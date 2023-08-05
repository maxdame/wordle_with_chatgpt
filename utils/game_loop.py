from utils.user import User
from utils.valid_words import valid_words
from utils.display import Colors, red_text, green_text, ERROR, COMPLETION
from utils.chatgpt import gpt_validation, provide_real_word, gpt_riddle
import csv
import random


class GameLoop(User):
    '''CLASS/STATIC VARIABLES'''
    # CHOSEN_WORD = random.choice(valid_words)
    CHOSEN_WORD = provide_real_word()
    GUESS_LIMIT = 6
    GUESS_COUNTER = 1
    GREEN_POINTS = 5
    YELLOW_POINTS = 2
    HINT_COST = 25
    REWIND_COST = 50
    RIDDLE_POINTS = 100
    NO_COLOR_GUESSED_WORDS = []
    COLORED_GUESSED_WORDS = []
    ALPHABET = {
        "a": "a",
        "b": "b",
        "c": "c",
        "d": "d",
        "e": "e",
        "f": "f",
        "g": "g",
        "h": "h",
        "i": "i",
        "j": "j",
        "k": "k",
        "l": "l",
        "m": "m",
        "n": "n",
        "o": "o",
        "p": "p",
        "q": "q",
        "r": "r",
        "s": "s",
        "t": "t",
        "u": "u",
        "v": "v",
        "w": "w",
        "x": "x",
        "y": "y",
        "z": "z",
    }

    def __init__(self, user: User, guess: str):
        '''INSTANCE VARIABLES'''
        self.guess = guess
        self.guess_chars = list(self.guess)
        self.colored_guess = ""
        self.username = user.username
        self.player_points = user.player_points
        self.games_played = 0
        self.games_won = 0
        self.win_rate = 0

    def game_logic(self):
        if self.guess in ["help", "hint", "rewind", "riddle"]:
            if self.guess == "help":
                self.print_alphabet()
            elif self.guess == "hint":
                self.apply_hint()
            elif self.guess == "rewind":
                self.rewind()
            elif self.guess == "riddle":
                self.riddle()
            return False
        elif self.is_valid():
            self.apply_colors()
            if self.check_win():
                return True
            elif self.next_guess():
                return False
            if self.check_game_over():
                return True
        return False

    def next_guess(self):
        GameLoop.GUESS_COUNTER += 1

    def is_valid(self):
        if self.guess in GameLoop.NO_COLOR_GUESSED_WORDS:
            red_text(
                "                          Nice try but you already guessed that word...")
            return False
        if len(self.guess) != 5:
            red_text(
                "                          Your guess must contain 5 letters, dumbo...")
            return False
        if not gpt_validation(self.guess):
            red_text(
                f"                        Really? {self.guess}? Even the AI thinks you're dumb.")
            return False
        return True

    def apply_green(self):
        for i, _ in enumerate(self.guess_chars):
            answer_char = GameLoop.CHOSEN_WORD[i]
            guess_char = self.guess_chars[i]
            if answer_char == guess_char:
                colored_char = f"{Colors.GREEN}{guess_char}{Colors.BASE}"
                self.guess_chars[i] = colored_char
                # Locate guessed character in dictionary and update its value to the colored character
                self.edit_alphabet(guess_char, colored_char)
                # Increase the user's points by the points assigned for a correct guess
                self.increase_player_points(GameLoop.GREEN_POINTS)

    # Method to color guessed characters that are correct but in the wrong position
    def apply_yellow(self):
        # Iterate over each character in the user submitted guess word
        for i, _ in enumerate(self.guess_chars):
            guess_char = self.guess_chars[i]
            # If guessed character exists in the actual answer word
            if guess_char in GameLoop.CHOSEN_WORD:
                colored_char = f"{Colors.YELLOW}{guess_char}{Colors.BASE}"
                self.guess_chars[i] = colored_char
                # Locate guessed character in dictionary and update its value to the colored character
                self.edit_alphabet(guess_char, colored_char)
                # Increase the user's points by the points assigned for a correct character in wrong place
                self.increase_player_points(GameLoop.YELLOW_POINTS)
            else:  # Else color the character red (not in word)
                colored_char = f"{Colors.RED}{guess_char}{Colors.BASE}"
                self.edit_alphabet(guess_char, colored_char)

    def edit_alphabet(self, key, value):
        if key not in GameLoop.ALPHABET.keys():
            return
        # Get the current color of the character
        previous_value = GameLoop.ALPHABET.get(key, "")
        update_color = True  # Assume the color needs to be updated
        # Iterate over the list of persistent colors (green, red or cyan)
        for color in Colors.PERSISTENT_COLORS:
            # Do not update key-value pairs that are already colored (green, red or cyan)
            if color in previous_value:
                update_color = False
        if update_color:  # If the color needs to be updated
            # Update the color in the alphabet dictionary
            GameLoop.ALPHABET[key] = value

    def apply_colors(self):
        previous_points = self.retreive_current_points()
        self.apply_green()
        self.apply_yellow()
        updated_points = self.retreive_current_points()
        self.colored_guess = "".join(self.guess_chars)
        GameLoop.COLORED_GUESSED_WORDS.append(self.colored_guess)
        GameLoop.NO_COLOR_GUESSED_WORDS.append(self.guess)
        print(
            f"                                             {self.colored_guess}")
        print(
            f"{Colors.YELLOW}POINTS AWARDED:{Colors.BASE} +{updated_points - previous_points}")

    def check_win(self):
        if self.guess == GameLoop.CHOSEN_WORD:
            self.player_points = self.retreive_current_points()
            print(COMPLETION)
            print(
                f"{Colors.MAGENTA}POINTS AVAILABLE:{Colors.BASE} {self.player_points}")
            print("")
            if GameLoop.GUESS_COUNTER <= 2:
                print(
                    "                       You won! We're all a little suprised, not gonna lie.")
            if GameLoop.GUESS_COUNTER >= 3 and GameLoop.GUESS_COUNTER <= 4:
                print(
                    "     Congrats! You actually won something. I hope this isn't the peak of your achievements.")
            if GameLoop.GUESS_COUNTER == 5:
                print(
                    "                         You almost lost there bud, don't get too cocky!")
            print("")
            self.print_guesses()
            print("")
            print(COMPLETION)
            self.increase_games_played()
            self.increase_games_won()
            input(
                f"{Colors.YELLOW}                             Press ENTER to return to the homepage.{Colors.BASE}")
            green_text("Loading homepage...")
            return True

    def increase_player_points(self, points):
        try:
            with open("users.csv", "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                found_user = False  # Assume user not found
                # Iterate over the rows (skipping the header row with index 0)
                for i in range(1, len(rows)):
                    if rows[i][0].lower() == self.username:
                        rows[i][2] = int(rows[i][2]) + points
                        found_user = True
                        break
                if not found_user:
                    red_text(f"Did not find user {self.username}")
            with open("users.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
        except Exception as e:
            red_text(f"An error occurred: {str(e)}")

    def decrease_player_points(self, points):
        try:
            with open("users.csv", "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                found_user = False
                for i in range(1, len(rows)):
                    if rows[i][0].lower() == self.username:
                        rows[i][2] = int(rows[i][2]) - points
                        found_user = True  # Update user found flag
                        break
                if not found_user:
                    red_text(f"Did not find user {self.username}")
            with open("users.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
            print(f"{Colors.YELLOW}POINTS USED:{Colors.BASE} -{points}")
        except Exception as e:
            red_text(f"An error occurred: {str(e)}")

    def add_words_played(self):
        try:
            with open("users.csv", "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                found_user = False
                for i in range(1, len(rows)):
                    if rows[i][0].lower() == self.username.lower():
                        found_user = True
                        words_to_add = []
                        # Convert the words_played string to a list
                        if rows[i][5]:  # Check if the field is not empty
                            words_played = rows[i][5].split(", ")
                            words_to_add.extend(words_played)
                        # Append the chosen word to the list
                        words_to_add.append(GameLoop.CHOSEN_WORD)
                        rows[i][5] = ", ".join(words_to_add)
                        break
                if not found_user:
                    red_text(f"Did not find user {self.username}")
            with open("users.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
        except Exception as e:
            red_text(f"An error occurred: {str(e)}")

    def increase_games_won(self):
        try:
            with open("users.csv", "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                found_user = False
                for i in range(1, len(rows)):
                    if rows[i][0].lower() == self.username:
                        rows[i][4] = int(rows[i][4]) + 1
                        found_user = True
                        break
                if not found_user:
                    red_text(f"Did not find user {self.username}")
            with open("users.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
        except Exception as e:
            red_text(f"An error occurred: {str(e)}")

    def increase_games_played(self):
        try:
            with open("users.csv", "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                found_user = False
                for i in range(1, len(rows)):
                    if rows[i][0].lower() == self.username:
                        # Add 1 to the user's games_played column
                        rows[i][3] = int(rows[i][3]) + 1
                        found_user = True
                        break
                if not found_user:
                    red_text(f"Did not find user {self.username}")
            with open("users.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
        except Exception as e:
            red_text(f"An error occurred: {str(e)}")

    def check_game_over(self):
        if GameLoop.GUESS_COUNTER == GameLoop.GUESS_LIMIT + 1:
            print(ERROR)
            print(
                f"                                   Oof... the word was {Colors.GREEN}{GameLoop.CHOSEN_WORD}{Colors.BASE}.")
            print(ERROR)
            self.increase_games_played()
            input(
                f"{Colors.YELLOW}                             Press ENTER to return to the homepage.{Colors.BASE}")
            green_text("Loading homepage...")
            return True

    def print_guesses(self):
        for guess in GameLoop.COLORED_GUESSED_WORDS:
            print("                                             " + guess)

    def print_alphabet(self):
        print("")
        self.print_guesses()
        list_letters = list(GameLoop.ALPHABET.values())
        first_iteration = True
        for letter in list_letters:
            if first_iteration:
                print("                      " + letter, end=" ")
                first_iteration = False
            else:
                print(letter, end=" " if list_letters[-1] != letter else "\n")
        print("")

    def apply_hint(self):
        if self.player_points < GameLoop.HINT_COST:
            red_text("                                       Not enough points")
            return
        if self.player_points >= GameLoop.HINT_COST:
            # Initialize flag and character placeholder
            hint_found = False
            hint_char = None
            # Generate a shuffled list of indices
            correct_indices = list(range(len(GameLoop.CHOSEN_WORD)))
            random.shuffle(correct_indices)
            # Iterate over the indices until an unhighlighted character is found
            for hint_index in correct_indices:
                # Get character at hint index in the chosen word
                hint_char = GameLoop.CHOSEN_WORD[hint_index]
                # If the character is not colored, exit the loop
                if not (Colors.CYAN in GameLoop.ALPHABET[hint_char] or Colors.GREEN in GameLoop.ALPHABET[hint_char] or Colors.YELLOW in GameLoop.ALPHABET[hint_char]):
                    hint_found = True
                    break
            if hint_found:
                # Apply the hint color to the character
                colored_hint_char = f"{Colors.CYAN}{hint_char}{Colors.BASE}"
                self.edit_alphabet(hint_char, colored_hint_char)
                self.print_alphabet()
                self.decrease_player_points(GameLoop.HINT_COST)
            else:
                red_text(
                    "                                 All characters are being shown.")

    def rewind(self):
        if self.player_points < GameLoop.REWIND_COST:
            red_text("                                       Not enough points")
            return
        if self.player_points >= GameLoop.REWIND_COST:
            if GameLoop.GUESS_COUNTER > 1:
                GameLoop.GUESS_COUNTER -= 1
                self.decrease_player_points(GameLoop.REWIND_COST)
            else:
                red_text(
                    "                                      Cannot rewind past 1")
        return GameLoop.GUESS_COUNTER

    def riddle(self):
        if self.player_points < GameLoop.RIDDLE_POINTS:
            red_text("                                       Not enough points")
            return
        if self.player_points >= GameLoop.RIDDLE_POINTS:
            riddle = gpt_riddle(GameLoop.CHOSEN_WORD)
            print("")
            print(riddle)
            print("")
            self.decrease_player_points(GameLoop.RIDDLE_POINTS)

    def retreive_current_points(self):
        try:
            with open("users.csv", "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                found_user = False
                for i in range(1, len(rows)):
                    if rows[i][0].lower() == self.username:
                        self.player_points = int(rows[i][2])
                        found_user = True
                        return self.player_points
                if not found_user:
                    red_text(f"Did not find user: {self.username}")
        except Exception as e:
            red_text(f"An error occurred: {str(e)}")

    def retreive_user_info(self):
        with open("users.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
        for i in range(1, len(rows)):
            if rows[i][0].lower() == self.username:
                # Assign class attributes to approriate column values
                self.player_points = int(rows[i][2])
                self.games_played = int(rows[i][3])
                self.games_won = int(rows[i][4])
                if self.games_played == 0:  # Handle divide by 0 error
                    self.win_rate = 0
                else:
                    # Assign win rate as formatted percent
                    self.win_rate = format(
                        (self.games_won/self.games_played)*100, '.0f')
        return self.player_points, self.games_played, self.win_rate

    def reset_game(self):
        # GameLoop.CHOSEN_WORD = random.choice(valid_words)
        GameLoop.CHOSEN_WORD = provide_real_word()
        GameLoop.GUESS_LIMIT = 6
        GameLoop.GUESS_COUNTER = 1
        GameLoop.COLORED_GUESSED_WORDS = []
        GameLoop.NO_COLOR_GUESSED_WORDS = []
        GameLoop.ALPHABET = {
            "a": "a",
            "b": "b",
            "c": "c",
            "d": "d",
            "e": "e",
            "f": "f",
            "g": "g",
            "h": "h",
            "i": "i",
            "j": "j",
            "k": "k",
            "l": "l",
            "m": "m",
            "n": "n",
            "o": "o",
            "p": "p",
            "q": "q",
            "r": "r",
            "s": "s",
            "t": "t",
            "u": "u",
            "v": "v",
            "w": "w",
            "x": "x",
            "y": "y",
            "z": "z",
        }
