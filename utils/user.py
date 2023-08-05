import os
import csv
from utils.display import *


class User:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.player_points = ""
        self.games_played = ""
        self.games_won = ""
        self.words_played = []
        self.loss_rate = 0
        self.first_game = None
        self.extra_points = 250
        self.extra_points_given = False

    def give_extra_points(self, authorized_user):
        if self.extra_points_given:
            red_text("Nice try but you only get this handout once!")
            return False
        if not authorized_user:
            red_text("Not logged in or registered!")
            return False
        if self.first_game != True:
            red_text("Sorry you missed your chance!")
            return False
        self.increase_player_points(self.extra_points)
        self.extra_points_given = True
        print(COMPLETION)
        cyan_text(
            "Okay, you caught me... I'm just messing around with you!")
        print(COMPLETION)
        cyan_text(
            "Here are some extra points. Don't go spending them all at once...")
        print(COMPLETION)
        self.first_game = False
        return self.first_game

    def increase_player_points(self, points):
        try:
            with open("users.csv", "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                found_user = False
                # Iterate over the rows (skipping the header row with index 0)
                for i in range(1, len(rows)):
                    # If the username in the row matches the current username
                    if rows[i][0].lower() == self.username:
                        # Add points to the user's player_points columns
                        rows[i][2] = int(rows[i][2]) + points
                        found_user = True  # Update user found flag
                        break
                if not found_user:
                    red_text(f"Did not find user {self.username}")
            # Open users file for writing updated value
            with open("users.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
        except Exception as e:
            red_text(f"An error occurred: {str(e)}")

    def register(self):
        display_title()
        display_register_header()
        # USERNAME CHECK
        while True:
            self.username = input(
                f"{Colors.MAGENTA}Create your username: {Colors.BASE}")
            if self.username == "#":
                break
            if self.is_username_registered():
                red_text("Username already registered.")
            elif len(self.username) > 10 or len(self.username) == 0 or " " in self.username:
                red_text("Username must be 1 - 10 characters, no spaces.")
            else:
                break
        # PASSWORD CHECK
        while True:
            print(DIVIDER)
            if self.username == "#":
                break
            self.password = input(
                f"{Colors.MAGENTA}Create your password: {Colors.BASE}")
            if self.password == "#":
                break
            if len(self.password) < 5 or " " in self.password:
                red_text("Password must be at least 5 characters, no spaces.")
            else:
                file_exists = os.path.isfile("users.csv")
                with open("users.csv", "a", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    if not file_exists:
                        writer.writerow(
                            ["username", "password", "player_points", "games_played", "games_won", "words_played"])
                    writer.writerow(
                        [self.username, self.password, 0, 0, 0, ""])
                break
        if self.username == "#" or self.password == "#":
            green_text("Loading homepage...")
            return False
        else:
            print_success_message(self.username, Colors, "registered")
            authorized_user = self.username
            return authorized_user

    def is_username_registered(self):
        if not os.path.isfile("users.csv"):
            return False
        with open("users.csv", "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0].lower() == self.username:
                    return True
        return False

    def login(self):
        display_title()
        display_login_header()
        # USERNAME CHECK
        while True:
            self.username = input(
                f"{Colors.MAGENTA}Enter your username: {Colors.BASE}").lower()
            if self.username == "#":
                break
            # Check if username is already in "users.csv"
            if not self.is_username_registered():
                red_text("Username not registered.")
            else:
                break
        # PASSWORD CHECK
        while True:
            print(DIVIDER)
            if self.username == "#":
                break
            self.password = input(
                f"{Colors.MAGENTA}Enter your password: {Colors.BASE}")
            if self.password == "#":
                break
            # Check if password matches with the username in "users.csv"
            if not self.is_password_correct():
                red_text("Incorrect password.")
            else:
                break
        if self.username == "#" or self.password == "#":
            green_text("Loading homepage...")
            return False
        else:
            print_success_message(self.username, Colors, "logged in")
            authorized_user = self.username
            return authorized_user

    def is_password_correct(self):
        # Open the "users.csv" file for reading
        with open("users.csv", "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0].lower() == self.username.lower() and row[1] == self.password:
                    return True  # Username and password match
        return False  # Password does not match for the given username

    def retreive_user_info(self, authorized_user):
        if authorized_user:
            with open("users.csv", "r") as file:
                reader = csv.reader(file)
                rows = list(reader)
            for i in range(1, len(rows)):
                if rows[i][0].lower() == authorized_user:
                    # Assign class attributes to approriate column values
                    self.player_points = int(rows[i][2])
                    self.games_played = int(rows[i][3])
                    self.games_won = int(rows[i][4])
                    self.words_played = rows[i][5]
                    if self.games_played > 0:
                        self.first_game = False
                        # Assign win rate as formatted percent
                        self.loss_rate = int(
                            ((self.games_played - self.games_won)/self.games_played)*100)
                    elif self.extra_points_given:
                        self.loss_rate = 0
                        self.first_game = False
                    elif self.games_played == 0:  # Handle divide by 0 error
                        self.loss_rate = 0
                        self.first_game = True
        return self.player_points, self.games_played, self.loss_rate, self.first_game, self.words_played

    def prompt_user(self, counter, authorized_user):
        self.player_points, self.games_played, self.loss_rate, self.first_game, self.words_played = self.retreive_user_info(
            authorized_user)
        print(DIVIDER)
        print(f"{Colors.MAGENTA}Points Available:{Colors.BASE} {self.player_points}")
        return input(f"                                         [{Colors.BLUE}{counter}{Colors.BASE}]>").lower()
