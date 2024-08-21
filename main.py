from controllers.main_controller import MainController
from utils.utils import capitalize_name, clear_console, get_username

if __name__ == "__main__":
    clear_console()
    print(
        f"Bonjour {capitalize_name(get_username())} ! Bienvenue dans l'application de gestion de tournois d'échecs !"
    )
    print(
        "Ce programme vous permet de gérer des joueurs, des tournois et de générer des rapports hors lignes "
        "de façon simple et efficace.\n"
    )

    main_controller = MainController()
    main_controller.run()
