from controllers.player_controller import PlayerController
from controllers.report_controller import ReportController
from controllers.tournament_controller import TournamentController
from utils.utils import capitalize_name, clear_console, get_username
from views.main_view import MainView


class MainController:
    """
    Contrôleur principal qui gère l'interaction entre les vues et les autres contrôleurs.
    """
    def __init__(self):
        """
        Initialise le contrôleur principal avec les contrôleurs de joueur, tournoi et rapport.
        """
        self.main_view = MainView()

        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController(self.player_controller)
        self.report_controller = ReportController(
            self.player_controller.players_df, self.tournament_controller.tournaments_df, self.player_controller
        )

    def run(self):
        while True:
            self.main_view.display_main_menu()
            choice = self.main_view.get_user_choice()

            if choice == "player_management":
                clear_console()
                self.player_controller.run()
                # Après la gestion des joueurs, recharge players_df pour que tout soit à jour
                self.report_controller.players_df = self.player_controller.load_players()

            elif choice == "tournament_management":
                clear_console()
                result = self.tournament_controller.run()
                self.report_controller.tournaments_df = self.tournament_controller.tournaments_df
                self.report_controller.players_df = self.player_controller.players_df

                if result == "back":
                    continue

            elif choice == "report_management":
                clear_console()
                self.player_controller.load_players()
                self.tournament_controller.load_tournaments()
                self.report_controller.players_df = self.player_controller.players_df
                self.report_controller.tournaments_df = self.tournament_controller.tournaments_df
                self.report_controller.run()

            elif choice == "quit":
                clear_console()
                self.main_view.show_message(f"Au revoir {capitalize_name(get_username())}, à très vite ! 👋 \n")
                break
