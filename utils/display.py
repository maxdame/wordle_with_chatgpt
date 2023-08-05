import os
import time
import sys


def clear_screen(sec):
    time.sleep(sec)
    os.system("cls") if os.name == "nt" else os.system("clear")


def display_title():
    print(COMPLETION)
    title = """::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: ##::::::##: ######:: ##::: ##: ########::::::: #######:: ##::: ##: ##:::::::##: ########:::
::. ##::::##: ##... ##: ##::: ##: ##.... ##:::::: ##... ##: ##::: ##: ###:::::###: ##.... ##::
:::. ##::##:: ##::: ##: ##::: ##: ##:::: ##:::::: ##::: ##: ##::: ##: ####:::####: ##:::: ##::
::::. ####::: ##::: ##: ##::: ##: ########::::::: ##::: ##: ##::: ##: ## ##:## ##: ########:::
:::::. ##:::: ##::: ##: ##::: ##: ##... ##::::::: ##::: ##: ##::: ##: ##: #### ##: ##.... ##::
:::::: ##:::: ##::: ##: ##::: ##: ##:::: ##:::::: ##::: ##: ##::: ##: ##:: ##: ##: ##:::: ##::
:::::: ##:::: #######::. ######:: ##::::: ##::::: #######::. ######:: ##::..:: ##: ########:::
::::::..:::::.......::::......:::..::::::..::::::.......::::......:::..:::::::..::........::::"""
    print(title.replace("#", f"{Colors.GREEN}#{Colors.BASE}"))


def show_homepage(authorized_user, player_points, games_played, loss_rate, first_game):
    clear_screen(2)
    display_title()
    # print("FIRST GAME:", first_game)
    print_homepage(authorized_user, player_points,
                   games_played, loss_rate, first_game)
    return handle_user_input(authorized_user)


def print_homepage(authorized_user, player_points, games_played, loss_rate, first_game):
    print(
        f"========================================== {Colors.CYAN}HOMEPAGE{Colors.BASE} ==========================================")
    if authorized_user == False:
        print(f"{Colors.MAGENTA}USER:{Colors.BASE}")
    else:
        print(f"{Colors.MAGENTA}USER:{Colors.BASE} {authorized_user}")
    print(f"{Colors.MAGENTA}POINTS AVAILABLE:{Colors.BASE} {player_points}")
    print(f"{Colors.MAGENTA}GAMES PLAYED:{Colors.BASE} {games_played}")
    print(f"{Colors.MAGENTA}DUMMY METER:{Colors.BASE}")
    draw_progress_bar(authorized_user, first_game, loss_rate)
    print("+------------------------------+------------------------------+------------------------------+")
    print("|         1. LOGIN             |         2. REGISTER          |         3. PLAY              |")
    print("+------------------------------+------------------------------+------------------------------+")
    print("|         4. GAME RULES        |         5. DUMMYBOARD        |         6. EXIT              |")
    print("+------------------------------+------------------------------+------------------------------+")


def handle_user_input(authorized_user):
    while True:
        option = input(
            f"{Colors.YELLOW}Please make a selection >> {Colors.BASE}").lower()
        if option in ("1", "login"):
            if authorized_user:
                red_text("Already logged in.")
                option = None
            else:
                green_text("Loading login page...")
        elif option in ("2", "register"):
            if authorized_user:
                red_text("Already registered.")
                option = None
            else:
                green_text("Loading registration page...")
        elif option in ("3", "play"):
            if authorized_user:
                green_text("Loading game...")
            else:
                red_text("Please login or register to play.")
                option = None
        elif option in ("4", "game rules", "rules"):
            green_text("Loading game rules...")
        elif option in ("5", "dummyboard"):
            green_text("Laoding dummyboard...")
        elif option in ("6", "exit"):
            green_text("Logging out...")
        elif option == "liar!":
            pass
        else:
            red_text("Please make a valid selection.")
        return option, authorized_user


def display_register_header():
    print(
        f"======================================== {Colors.CYAN}REGISTRATION{Colors.BASE} ========================================")
    print(f"{Colors.YELLOW}                                Input # to return to the homepage.{Colors.BASE}")
    print(DIVIDER)
    print(f"{Colors.BOLD_START}                                         Register Now!{Colors.BOLD_END}")
    print(DIVIDER)


def display_login_header():
    print(
        f"============================================ {Colors.CYAN}LOGIN{Colors.BASE} ===========================================")
    print(f"{Colors.YELLOW}                                Input # to return to the homepage.{Colors.BASE}")
    print(DIVIDER)
    print(f"{Colors.BOLD_START}                                       Login to play now!{Colors.BOLD_END}")
    print(DIVIDER)


def display_game_header():
    display_title()
    print(COMPLETION)
    print(f"{Colors.YELLOW}                                Input # to return to the homepage.{Colors.BASE}")
    print(DIVIDER)
    print(f'        {Colors.CYAN}POWER UPS:{Colors.BASE}  "HELP" 0pts  {Colors.CYAN}|{Colors.BASE}  "HINT" 25pts  {Colors.CYAN}|{Colors.BASE}  "REWIND" 50pts  {Colors.CYAN}|{Colors.BASE}  "RIDDLE" 100pts  ')


def yellow_text(str):  # System messages
    print(f"{Colors.YELLOW}{str}{Colors.BASE}")


def green_text(str):  # Completions
    print(COMPLETION)
    print(f"{Colors.GREEN}{str}{Colors.BASE}")
    print(COMPLETION)


def red_text(str):  # Errors
    print(ERROR)
    print(f"{Colors.RED}{str}{Colors.BASE}")
    print(ERROR)


# Login/registration success message
def print_success_message(username, Colors, str):
    print(COMPLETION)
    print(
        f"{Colors.GREEN}{username} has successfully {str}.{Colors.BASE}")
    green_text("Loading homepage...")


def magenta_text(str):  # User info
    print(f"{Colors.MAGENTA}{str}{Colors.BASE}")


def cyan_text(str):  # Header text
    print(f"{Colors.CYAN}{str}{Colors.BASE}")


def draw_progress_bar(authorized_user, first_game, stop_at):
    if not authorized_user:
        print("You look pretty smart to me!... or am I lying?")
    else:
        # The width of the progress bar (in characters)
        width = 42
        disses = ["Perhaps you're actually smart. Let's see how long that lasts...",
                  "Seems like you're a sandwich short of a picnic, buddy.",
                  "You're as sharp as a marble...",
                  "Your wheel's spinning but the hamster's long gone.",
                  "You'd struggle to pour water out of a boot with instructions on the heel.",
                  "You're about as useful as a one-legged man in an ass kicking contest.",
                  "You couldn't think your way out of a paper bag if the bottom was already torn.",
                  "You're denser than a black hole and half as interesting.",
                  "If stupidity was a crime, you'd be serving a life sentence.",
                  "Your brain is so damn slow, even snails roll their eyes passing by you",
                  "Just being honest, you're dumb ass fuck."]
        # Find the index of a diss based on the stop_at percentage
        diss_index = int(stop_at // 10)
        for i in range(101):
            # Calculate the number of characters to fill
            fill = int(width * i / 100)
            # Create the progress bar string
            progress_bar = '[' + '#' * fill + '-' * (width - fill) + ']'
            # Print the progress bar (\r carriage return, %s expects a string and %d expects an interger)
            sys.stdout.write('\r%s %d%%' % (progress_bar, i))
            sys.stdout.flush()
            time.sleep(0.01)
            if first_game:
                stop_at = 100
            # Stop updating the progress bar once MAXIMUM DUMMY RANGE is reached
            if i >= stop_at:
                if first_game:
                    print("\nI know this is your first time playing...")
                    print(
                        "but let's make some assumptions and crank that meter all the way up!")
                else:
                    print("\n" + disses[diss_index])
                break


DIVIDER = "+--------------------------------------------------------------------------------------------+"
COMPLETION = "=============================================================================================="
ERROR = "**********************************************************************************************"


class Colors:
    BOLD_START = "\033[1m"
    BOLD_END = "\033[0m"
    BASE = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    PERSISTENT_COLORS = [RED, GREEN, CYAN]
