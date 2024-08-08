from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from views.base_view import BaseView


class MainView(BaseView):
    def __init__(self):
        """
        Initialise la vue principale en appelant le constructeur de la classe BaseView.
        """
        super().__init__()

    def display_main_menu(self):
        """
        Affiche le menu principal et capture le choix de l'utilisateur.
        """
        # Calcul de la longueur du choix le plus long pour ajuster la taille du Separator
        longest_choice_length = max(
            len("📋 Gestion des joueurs"),
            len("🏆 Gestion des tournois"),
            len("📁 Gestion des rapports"),
            len("🚪 Quitter le programme"),
        )

        # Définition des options du menu principal
        menu_options = [
            Choice("player_management", name="📋 Gestion des joueurs"),
            Choice("tournament_management", name="🏆 Gestion des tournois"),
            Choice("report_management", name="📁 Gestion des rapports"),
            Separator(line="-" * (longest_choice_length + 1)),
            Choice("quit", name="🚪 Quitter le programme"),
        ]

        # Affichage du menu principal en utilisant inquirer
        self.choice = inquirer.select(
            message="Menu Principal\n",
            long_instruction="\nDans le menu principal, vous avez accès à ces quatre fonctionnalités :\
            \n\n- Gestion des joueurs (ce menu vous permet de gérer l'intégralité des joueurs du programme)\
            \n- Gestion des tournois (ce menu vous permet de gérer l'intégralité des tournois du programme)\
            \n- Gestion des rapports (ce menu vous permet de générer des rapports sur les joueurs et les tournois)\
            \n- Quitter le programme (vous pourrez quitter le programme facilement)\
            \n\n-----------------------------------------------------------------------------------------------------------------\
            \n\nCe programme a été conçu avec 🤍 et développé par Thomas Dupré\
            \n\n💻 https://github.com/ThomasDpr\
            \n📸 https://tdupre.fr",
            choices=menu_options,
            pointer="❯",
            qmark="",
            style=self.custom_style,
            show_cursor=False,
        ).execute()

    def get_user_choice(self):
        """
        Retourne le choix de l'utilisateur capturé par display_main_menu.
        """

        return self.choice

    def show_message(self, message):
        """
        Affiche un message à l'utilisateur.

        Args:
            message (str): Le message à afficher.
        """

        print(message)
