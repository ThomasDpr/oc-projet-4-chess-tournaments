from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich.table import Table, box

from utils.utils import clear_console
from views.base_view import BaseView


class TournamentView(BaseView):
    def __init__(self):
        """
        Initialise la vue du tournoi en appelant le constructeur de la classe parente.
        """

        super().__init__()

    def show_message(self, message):
        """
        Affiche un message à l'utilisateur.

        Args:
            message (str): Le message à afficher.
        """
        self.console.print(message)

    def show_menu(self):
        """
        Affiche le menu principal de gestion des tournois.
        """
        menu_options = [
            Choice("1", name="📋 Liste de tous les tournois"),
            Choice("2", name="➕ Ajouter un tournoi"),
            Choice("3", name="🏁 Démarrer un tournoi"),
            Choice("4", name="🔄 Reprendre un tournoi"),
            Separator(),
            Choice("5", name="🔙 Retour au menu principal"),
        ]
        self.choice = inquirer.select(
            message="Gestion des tournois \n",
            choices=menu_options,
            pointer="❯",
            qmark="",
            style=self.custom_style,
            show_cursor=False,
        ).execute()

    def get_user_select_choice(self):
        """
        Retourne le choix de l'utilisateur dans le menu de sélection.

        Returns:
            str: Le choix de l'utilisateur.
        """
        return self.choice

    def get_tournament_info(self):
        """
        Récupère les informations du tournoi auprès de l'utilisateur.

        Returns:
            tuple: Les informations du tournoi (nom, location, start_date, end_date, description, rounds_count).
        """
        name = self.text_with_cancel("Nom du tournoi :")
        if name is None:
            return None

        location = self.text_with_cancel("Localisation :")
        if location is None:
            return None

        start_date = self.text_with_cancel("Date de début (YYYY-MM-DD) :")
        if start_date is None:
            return None

        end_date = self.text_with_cancel("Date de fin (YYYY-MM-DD) :")
        if end_date is None:
            return None

        description = self.text_with_cancel("Description :")
        if description is None:
            return None

        rounds_count = self.get_rounds_count_with_default("Nombre de rounds (laisser vide pour 4 par défaut) :")
        if rounds_count is None:
            return None

        return name, location, start_date, end_date, description, rounds_count

    def text_with_cancel(self, message):
        """
        Affiche un input permettant à l'utilisateur de saisir une valeur ou d'annuler l'opération.

        Args:
            message (str): Le message à afficher.

        Returns:
            str or None: La valeur saisie par l'utilisateur ou None si l'opération est annulée.
        """
        while True:
            text_input = inquirer.text(message=f"{message}", style=self.custom_style, qmark="", amark="").execute()

            if text_input == "":
                choice = inquirer.select(
                    message="Le champ ne peut pas être vide. Que souhaitez-vous faire ?",
                    choices=[
                        Choice(value=None, name="Continuer la création du tournoi"),
                        Choice(value="cancel", name="Annuler"),
                    ],
                    style=self.custom_style,
                    pointer="❯",
                    qmark="",
                    show_cursor=False,
                ).execute()
                clear_console()
                print("Appuyez sur Entrée pour annuler\n")

                if choice == "cancel":
                    clear_console()
                    return None
            else:
                return text_input

    def get_rounds_count_with_default(self, message):
        """
        Affiche une invite permettant à l'utilisateur de saisir le nombre de rounds ou d'utiliser la valeur par défaut.

        Args:
            message (str): Le message à afficher.

        Returns:
            str: Le nombre de rounds saisi par l'utilisateur ou la valeur par défaut.
        """
        while True:
            rounds_input = inquirer.text(message=f"{message}", style=self.custom_style, qmark="", amark="").execute()

            if rounds_input == "":
                choice = inquirer.select(
                    message="Que souhaitez-vous faire ?",
                    choices=[
                        Choice(value="default", name="Appliquer 4 rounds (par défaut)"),
                        Choice(value="cancel", name="Annuler"),
                    ],
                    style=self.custom_style,
                    pointer="❯",
                    qmark="",
                    show_cursor=False,
                ).execute()

                if choice == "default":
                    return "4"
                elif choice == "cancel":
                    clear_console()
                    return None
            else:
                return rounds_input

    def list_tournaments(self, tournaments_df):
        """
        Affiche la liste des tournois.

        Args:
            tournaments_df (pd.DataFrame): Le DataFrame contenant les informations des tournois.
        """

        table = Table(title="Liste des tournois", box=box.SQUARE, show_lines=True)
        table.add_column("Nom", header_style="bold cyan")
        table.add_column("Lieu", header_style="bold cyan")
        table.add_column("Date de début", header_style="bold cyan")
        table.add_column("Date de fin", header_style="bold cyan")
        table.add_column("Description", header_style="bold cyan")
        table.add_column("Rounds", header_style="bold cyan")
        table.add_column("Joueurs", header_style="bold cyan")

        for _, tournament in tournaments_df.iterrows():
            description = (
                tournament["description"][:30] + "..."
                if len(tournament["description"]) > 30
                else tournament["description"]
            )
            table.add_row(
                tournament["name"],
                tournament["location"],
                tournament["start_date"],
                tournament["end_date"],
                description,
                f"{len(tournament['rounds'])} rounds",
                f"{len(tournament['players'])} joueurs",
            )

        self.console.print(table)

    def select_tournament(self, tournaments):
        """
        Affiche une liste de tournois à sélectionner.

        Args:
            tournaments (list): La liste des tournois.

        Returns:
            str: Le choix de l'utilisateur.
        """
        choices = [Choice(value=i, name=f"🏆 {tournament['name']}") for i, tournament in enumerate(tournaments)] + [
            Separator(),
            Choice(value="main_menu", name="🔙 Retour au menu principal"),
        ]

        choice = inquirer.select(
            message="Choisissez un tournoi",
            choices=choices,
            pointer="❯",
            qmark="",
            style=self.custom_style,
            show_cursor=False,
        ).execute()
        return choice

    def list_players_in_tournament(self, tournament_players_df, players_df):
        """
        Affiche la liste des joueurs inscrits dans un tournoi.

        Args:
            tournament_players_df (pd.DataFrame): Le DataFrame contenant les joueurs du tournoi.
            players_df (pd.DataFrame): Le DataFrame contenant tous les joueurs.
        """
        if tournament_players_df is not None:
            table_tournament_players = Table(title="Joueurs du tournoi", box=box.SQUARE, show_lines=True)
            table_tournament_players.add_column("Nom", header_style="bold cyan")
            table_tournament_players.add_column("Prénom", header_style="bold cyan")
            table_tournament_players.add_column("Date de naissance", header_style="bold cyan")
            table_tournament_players.add_column("ID national", header_style="bold cyan")
            table_tournament_players.add_column("Score de carrière", header_style="bold cyan")

            for player in tournament_players_df:
                player_data = players_df.loc[players_df["national_id"] == player["national_id"]].iloc[0]
                table_tournament_players.add_row(
                    player_data["last_name"],
                    player_data["first_name"],
                    player_data["birth_date"],
                    player["national_id"],
                    str(player["career_score"]),
                )

            self.console.print(table_tournament_players)

    def show_tournament_actions(self):
        """
        Affiche les actions disponibles pour un tournoi en cours.

        Returns:
            str: Le choix de l'utilisateur.
        """

        actions = [
            Choice(value="add", name="➕ Ajouter des joueurs"),
            Choice(value="remove", name="➖ Retirer des joueurs"),
            Choice(value="start", name="🏁 Commencer le tournoi"),
            Separator(),
            Choice(value="cancel", name="🔙 Retour au menu précédent"),
        ]

        action = inquirer.select(
            message="\nQue souhaitez-vous faire ?\n",
            choices=actions,
            pointer="❯",
            qmark="",
            style=self.custom_style,
            show_cursor=False,
        ).execute()
        return action

    def show_no_player_actions(self):
        """
        Affiche les actions disponibles lorsqu'aucun joueur n'est inscrit dans le tournoi.

        Returns:
            str: Le choix de l'utilisateur.
        """

        actions = [
            Choice(value="add", name="➕ Ajouter des joueurs"),
            Separator(line=27 * "-"),
            Choice(value="back", name="🔙 Retour au menu précédent"),
            Choice(value="main_menu", name="🏠 Retour au menu principal"),
        ]
        action = inquirer.select(
            message="\nQue souhaitez-vous faire ?\n",
            choices=actions,
            pointer="❯",
            qmark="",
            style=self.custom_style,
            show_cursor=False,
        ).execute()
        return action

    def select_player_to_remove(self, tournament_players):
        """
        Affiche la liste des joueurs du tournoi pour en sélectionner un à retirer.

        Args:
            tournament_players (list): La liste des joueurs du tournoi.

        Returns:
            str: Le choix de l'utilisateur.
        """

        choices = [
            Choice(
                player["national_id"], name=f"{player['first_name']} {player['last_name']} ({player['national_id']})"
            )
            for player in tournament_players
        ]
        choices.append(Separator(line=50 * "-"))
        choices.append(Choice("back", name="🔙 Retour au menu précédent"))
        choices.append(Choice("main_menu", name="🏠 Retour au menu principal"))

        choice = inquirer.select(
            message="Sélectionnez le joueur à retirer :\n",
            choices=choices,
            style=self.custom_style,
            pointer="❯",
            qmark="",
            show_cursor=False,
        ).execute()
        return choice

    def get_player_add_choice(self):
        """
        Affiche une invite permettant à l'utilisateur de saisir l'identifiant national d'un joueur à ajouter.

        Returns:
            str: L'identifiant national saisi par l'utilisateur.
        """

        choice = inquirer.text(
            message="\nVeuillez saisir l'Identifiant National du joueur à ajouter "
            "ou 'new' pour créer un nouveau joueur (entrez 'done' pour terminer) :",
            style=self.custom_style,
            qmark="",
            amark="",
        ).execute()
        return choice.lower()

    def create_tournament_tables(self, tournament, pairs, round_name, match_number, player1_info, player2_info):
        """
        Crée les tableaux d'informations pour un tournoi, y compris les joueurs, rounds et matches.

        Args:
            tournament (Tournament): L'objet tournoi.
            pairs (list): La liste des paires de joueurs.
            round_name (str): Le nom du round actuel.
            match_number (int): Le numéro du match actuel.
            player1_info (str): Les informations du joueur 1.
            player2_info (str): Les informations du joueur 2.

        Returns:
            Table: Le tableau principal contenant toutes les informations alignées correctement.
        """

        # Tableau pour les informations générales du tournoi
        tournament_table = Table(title=f"Tournoi : {tournament.name}", title_style="bold magenta", box=box.SQUARE)
        tournament_table.add_column("Nombre de rounds", justify="center", style="bold cyan")
        tournament_table.add_column("Nombre de matchs", justify="center", style="bold cyan")
        tournament_table.add_column("Nombre de joueurs", justify="center", style="bold cyan")
        tournament_table.add_row(str(tournament.rounds_count), str(len(pairs)), str(len(tournament.players)))

        # Tableau pour les informations sur le round et le match actuel
        round_table = Table(box=box.SQUARE, title="Round et match actuel", title_style="bold magenta")
        round_table.add_column("Round n°", justify="center", style="bold cyan")
        round_table.add_column("Match n°", justify="center", style="bold cyan")
        round_table.add_row(str(tournament.current_round), str(match_number))

        # Tableau pour les informations des joueurs
        players_table = Table(title="Match", title_style="bold magenta", box=box.SQUARE)
        players_table.add_column("👨 Joueur 1", header_style="bold yellow", justify="center")
        players_table.add_column("🧑 Joueur 2", header_style="bold yellow", justify="center")
        players_table.add_row(player1_info, player2_info)

        # Tableau pour le barème de match
        scale_table = Table(title="Barème de match", title_style="bold magenta", box=box.SQUARE)
        scale_table.add_column("🥇 Gagnant", header_style="bold green", justify="center")
        scale_table.add_column("🥈 Perdant", header_style="bold red", justify="center")
        scale_table.add_column("🤝 Égalité", header_style="bold blue", justify="center")
        scale_table.add_row("1 point", "0 point", "0.5 point")

        # Table principale pour tout aligner correctement
        main_table = Table(show_edge=False, show_header=False, box=box.SIMPLE, show_lines=False)
        main_table.add_row(tournament_table, round_table)
        main_table.add_row(players_table, scale_table)

        self.console.print(main_table)

        return main_table

    def get_match_result(self, player1, player2):
        """
        Affiche une invite pour que l'utilisateur sélectionne le résultat d'un match.

        Args:
            player1 (dict): Informations du joueur 1.
            player2 (dict): Informations du joueur 2.

        Returns:
            tuple: Les scores des joueurs (score_player1, score_player2).
        """
        choice = inquirer.select(
            message="\nQui gagne ?\n",
            choices=[
                Choice(value="1", name=f"{player1['first_name']} {player1['last_name']}"),
                Choice(value="2", name=f"{player2['first_name']} {player2['last_name']}"),
                Choice(value="3", name="Égalité"),
                Separator(),
                Choice(value="4", name="🔙 Retour au menu principal"),
            ],
            pointer="❯",
            qmark="",
            style=self.custom_style,
            show_cursor=False,
        ).execute()

        if choice == "1":
            return (1.0, 0.0)
        elif choice == "2":
            return (0.0, 1.0)
        elif choice == "3":
            return (0.5, 0.5)
        elif choice == "4":
            raise InterruptedError("Retour au menu principal demandé.")
        else:
            self.show_message("Choix invalide, veuillez réessayer.")
            return self.get_match_result(player1, player2)
