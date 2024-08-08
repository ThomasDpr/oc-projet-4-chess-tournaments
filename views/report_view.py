from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich.table import Table

from controllers.player_controller import PlayerController
from utils.utils import clear_console
from views.base_view import BaseView

from .player_view import PlayerView
from .tournament_view import TournamentView


class ReportView(BaseView):
    def __init__(self):
        """
        Initialise la vue des rapports avec les vues des tournois et des joueurs ainsi que le contrôleur des joueurs.
        """

        self.tournament_view = TournamentView()
        self.player_view = PlayerView()
        self.player_controller = PlayerController()
        super().__init__()

    def show_menu(self):
        """
        Affiche le menu des rapports avec différentes options de rapports et permet à l'utilisateur de faire un choix.
        """
        # Calcul de la longueur du choix le plus long pour ajuster la taille du Separator
        longest_choice_length = max(
            len("📋 Liste de tous les joueurs (A-Z)"),
            len("📋 Liste de tous les tournois"),
            len("📋 Nom et dates d’un tournoi donné"),
            len("📋 Liste des joueurs d'un tournoi (A-Z)"),
            len("📋 Liste de tous les tours du tournoi et de tous les matchs du tour"),
            len("🔙 Retour au menu principal"),
        )
        menu_options = [
            Choice(value="1", name="📋 Liste de tous les joueurs (A-Z)"),
            Choice(value="2", name="📋 Liste de tous les tournois"),
            Choice(value="3", name="📋 Nom et dates d’un tournoi donné"),
            Choice(value="4", name="📋 Liste des joueurs d'un tournoi (A-Z)"),
            Choice(value="5", name="📋 Liste de tous les tours du tournoi et de tous les matchs du tour"),
            Separator(line="-" * (longest_choice_length + 1)),
            Choice(value="6", name="🔙 Retour au menu principal"),
        ]
        self.choice = inquirer.select(
            message="Gestion des rapports\n",
            choices=menu_options,
            pointer="❯",
            qmark="",
            style=self.custom_style,
            show_cursor=False,
            long_instruction="Dans le menu des rapports, vous avez accès à ces six fonctionnalités :"
            "\n\n- Liste de tous les joueurs (triés par ordre alphabétique)"
            "\n- Liste de tous les tournois (stockés dans le fichier 'data/tournaments.json')"
            "\n- Nom et dates d’un tournoi donné (informations détaillées d'un tournoi donné)"
            "\n- Liste des joueurs d'un tournoi (triés par ordre alphabétique)"
            "\n- Liste de tous les rounds d'un tournoi et de tous les matchs d'un round"
            "\n- Retour au menu principal (vous pouvez revenir au menu principal pour les autres fonctionnalités)\n"
            "\nPour chaque fonctionnalité, vous pouvez exporter les données dans différents formats."
        ).execute()

    def get_user_choice(self):
        """
        Retourne le choix de l'utilisateur dans le menu des rapports.
        """

        return self.choice

    def show_message(self, message):
        """
        Affiche un message à l'utilisateur.
        """

        print(message)

    def list_players(self, players_df):
        """
        Affiche la liste des joueurs en utilisant player_view.list_players.
        """
        self.player_view.list_players(players_df)

    def list_tournaments(self, tournaments_df):
        """
        Affiche la liste des tournois en utilisant tournament_view.list_tournaments.
        """
        self.tournament_view.list_tournaments(tournaments_df)

    def show_tournament_details(self, tournament_data):
        """
        Affiche les détails d'un tournoi avec la table RichTable.
        """
        clear_console()
        table = Table(title="Détails du tournoi", show_header=True, header_style="bold magenta")
        table.add_column("Nom")
        table.add_column("Lieu")
        table.add_column("Date de début")
        table.add_column("Date de fin")
        table.add_column("Description")

        table.add_row(
            tournament_data["name"],
            tournament_data["location"],
            tournament_data["start_date"],
            tournament_data["end_date"],
            tournament_data["description"],
        )

        self.console.print(table)

    def select_tournament(self, tournament_choices):
        """
        Permet à l'utilisateur de sélectionner un tournoi existant dans la liste des tournois.
        """

        choices = [Choice(value=index, name=name) for name, index in tournament_choices]
        choices.append(Separator(line=50 * "-"))
        choices.append(Choice(value=None, name="🔙 Annuler"))
        choice = inquirer.select(
            message="Choisissez un tournoi \n",
            choices=choices,
            pointer="❯",
            qmark="",
            style=self.custom_style,
            show_cursor=False,
        ).execute()
        clear_console()
        return choice

    def display_rounds_and_matches(self, tournament_data, rounds):
        """
        Affiche les rounds et les matchs d'un tournoi donné.
        """

        self.console.print(f"[bold magenta]Tournoi : {tournament_data['name']}[/bold magenta]")
        for round_ in rounds:
            table = Table(title=round_.name, show_header=True, header_style="bold magenta")
            table.add_column("Joueur 1", style="cyan")
            table.add_column("Joueur 2", style="cyan")
            table.add_column("Score", justify="center")

            for match in round_.matches:
                player1 = self.player_controller.get_player_by_national_id(match.player1_id)
                player2 = self.player_controller.get_player_by_national_id(match.player2_id)
                match_info = f"{match.score_player1} - {match.score_player2}"
                table.add_row(
                    f"{player1.first_name} {player1.last_name}",
                    f"{player2.first_name} {player2.last_name}",
                    match_info,
                )

            self.console.print(table)

    def ask_export_choice(self):
        """
        Demande à l'utilisateur s'il souhaite exporter les données ou revenir au menu précédent.
        """

        # choices = ["Exporter", "Retour au menu précédent"]
        # Calcul de la longueur du choix le plus long pour ajuster la taille du Separator
        longest_choice_length = max(len("📁 Exporter les données"), len("🔙 Retour au menu précédent"))
        choices = [
            Choice(value="Exporter", name="📁 Exporter les données"),
            Separator(line="-" * (longest_choice_length + 1)),
            Choice(value="Retour au menu précédent", name="🔙 Retour au menu précédent"),
        ]
        choice = inquirer.select(
            message="\nQue souhaitez-vous faire ?\n",
            choices=choices,
            style=self.custom_style,
            pointer="❯",
            amark="",
            qmark="",
            show_cursor=False,
        ).execute()
        clear_console()
        return choice

    def ask_export_format(self):
        """
        Demande à l'utilisateur de choisir le format d'exportation des données.
        """
        # Calcul de la longueur du choix le plus long pour ajuster la taille du Separator
        longest_choice_length = max(len("HTML"), len("TXT"), len("CSV"), len("Annuler"))
        choices = [
            Choice(value="HTML", name="HTML"),
            Choice(value="TXT", name="TXT"),
            Choice(value="CSV", name="CSV"),
            Separator(line="-" * longest_choice_length),
            Choice(value="Annuler", name="Annuler"),
        ]
        choice = inquirer.select(
            message="\nDans quel format ?\n",
            choices=choices,
            style=self.custom_style,
            pointer="❯",
            amark="",
            qmark="",
            show_cursor=False,
        ).execute()
        clear_console()
        return choice
