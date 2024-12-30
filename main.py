from menu import menu_screen
from game import game_screen
from editor import map_editor
from setting_page import settings_screen

def main():
    current_page = "menu"
    while True:
        if current_page == "menu":
            current_page = menu_screen()
        elif current_page == "game":
            current_page = game_screen()
        elif current_page == "editor":
            current_page = map_editor()
        elif current_page == "settings":
            current_page, _ = settings_screen()
        elif current_page == "exit":
            break

if __name__ == "__main__":
    main()
