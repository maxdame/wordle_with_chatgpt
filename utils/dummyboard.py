from utils.display import Colors, display_title, red_text, green_text, COMPLETION


def show_dummyboard():
    display_title()
    print(
        f"========================================= {Colors.CYAN}DUMMYBOARD{Colors.BASE} =========================================")
    print("")
    red_text("DUMMYBOARD IMPLEMENTATION STILL IN PROGRESS. Rest assured, you'd be at the top of the list...")
    print("")
    print(COMPLETION)
    input(f"{Colors.YELLOW}Press ENTER to return to the homepage.{Colors.BASE}")
    green_text("Loading homepage...")
