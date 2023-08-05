from utils.user import User
from utils.display import clear_screen, show_homepage, display_game_header, green_text
from utils.game_loop import GameLoop
from utils.game_rules import show_game_rules
from utils.dummyboard import show_dummyboard

if __name__ == "__main__":
    clear_screen(0)
    print("Let's see how dumb you really are...")
    authorized_user = ""
    user_instance = User()
    while True:
        player_points, games_played, loss_rate, first_game, words_played = user_instance.retreive_user_info(
            authorized_user)
        option, authorized_user = show_homepage(
            authorized_user, player_points, games_played, loss_rate, first_game)
        if option in ("1", "login"):
            clear_screen(2)
            authorized_user = user_instance.login()
        elif option in ("2", "register"):
            clear_screen(2)
            authorized_user = user_instance.register()
        elif option in ("3", "play"):
            clear_screen(2)
            display_game_header()
            with open("cheat.txt", "w") as txtfile:
                txtfile.write(GameLoop.CHOSEN_WORD)
            GameLoop.add_words_played(user_instance)
            while True:
                guess = user_instance.prompt_user(
                    GameLoop.GUESS_COUNTER, authorized_user)
                game_on = GameLoop(user_instance, guess)
                if guess == "#":
                    game_on.reset_game()
                    green_text("Loading homepage...")
                    break
                if game_on.game_logic():
                    game_on.reset_game()
                    break
        elif option in ("4", "game rules", "rules"):
            clear_screen(2)
            show_game_rules()
        elif option in ("5", "dummyboard"):
            clear_screen(2)
            show_dummyboard()
        elif option in ("liar!",):
            user_instance.give_extra_points(authorized_user)
        elif option in ("6", "exit"):
            clear_screen(2)
            break
