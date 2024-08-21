from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich.console import Console
from rich.table import Table, box

from utils.utils import clear_console
from views.base_view import BaseView


class TournamentView(BaseView):
    def __init__(self):
        """
        Initialise la vue du tournoi en appelant le constructeur de la classe parente.
        """

        super().__init__()
        self.name = ""
        self.location = ""
        self.start_date = ""
        self.end_date = ""
        self.description = ""
        self.rounds_count = 4  # Valeur par défaut
        self.current_step = 0

    def reset_info(self):
        """
        Réinitialise les informations du tournoi.
        """
        self.name = ""
        self.location = ""
        self.start_date = ""
        self.end_date = ""
        self.description = ""
        self.rounds_count = 4  # Valeur par défaut
        self.current_step = 0

    def show_message(self, message):
        """
        Affiche un message à l'utilisateur.

        Args:
            message (str): Le message à afficher.
        """
        self.console.print(message)

    def display_tournament_menu(self):
        """
        Affiche le menu principal de gestion des tournois.
        """
        longest_choice_length = max(
            len("Liste de tous les tournois"),
            len("Ajouter un tournoi"),
            len("Démarrer un tournoi"),
            len("Reprendre un tournoi"),
            len("Retour au menu principal"),
        )

        menu_options = [
            Choice("add_tournament", name="Ajouter un tournoi"),
            Choice("start_tournament", name="Démarrer un tournoi"),
            Choice("resume_tournament", name="Reprendre un tournoi"),
            Choice("tournament_list", name="Afficher tous les tournois"),
            Separator(line="-" * longest_choice_length),
            Choice("back_to_main_menu", name="Retour au menu principal"),
        ]
        self.choice = inquirer.select(
            message="Gestion des tournois \n",
            long_instruction="\nDans le menu Gestion des tournois, vous avez accès à ces cinq fonctionnalités :"
            "\n\n- Ajouter un tournoi (celui-ci sera créé puis enregistré en base de données)"
            "\n- Démarrer un tournoi (vous serez invité à sélectionner un tournoi existant)"
            "\n- Reprendre un tournoi (vous pourrez reprendre un tournoi en cours)"
            "\n- Liste de tous les tournois (vous pourrez visualiser les informations complète de tous les tournois)"
            "\n- Retour au menu principal (vous pourrez revenir au menu principal pour les autres fonctionnalités)\n"
            "\n\n❗️ Attention : Tout ajout, ou démarrage d'un tournoi entraînera"
            "la modification immédiate et automatique du fichier 'datas/tournaments.json'",
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
        Capture les informations du tournoi en interrogeant l'utilisateur étape par étape.
        Gère l'édition des informations et la confirmation de la création du tournoi.
        """
        self.reset_info()

        steps = [
            (
                "name",
                "Nom du tournoi :",
                "Veuillez entrer le Nom du tournoi.\n"
                "Si vous appuyez sur la touche 'Entrée' sans rien saisir,"
                "vous aurez la possibilité d'annuler l'opération.\n"
                "\n❗️ Attention : Ce champ est obligatoire.",
            ),
            (
                "location",
                "Localisation :",
                "Veuillez entrer la Localisation du tournoi.\n"
                "Si vous appuyez sur la touche 'Entrée' sans rien saisir,"
                "vous aurez la possibilité d'annuler l'opération.\n"
                "\n❗️ Attention : Ce champ est obligatoire.",
            ),
            (
                "start_date",
                "Date de début (YYYY-MM-DD) :",
                "Veuillez entrer la Date de début du tournoi.\n"
                "Si vous appuyez sur la touche 'Entrée' sans rien saisir, "
                "vous aurez la possibilité d'annuler l'opération.\n"
                "\n❗️ Attention : Ce champ est obligatoire.",
            ),
            (
                "end_date",
                "Date de fin (YYYY-MM-DD) :",
                "Veuillez entrer la Date de fin du tournoi.\n"
                "Si vous appuyez sur la touche 'Entrée' sans rien saisir, "
                "vous aurez la possibilité d'annuler l'opération.\n"
                "\n❗️ Attention : Ce champ est obligatoire.",
            ),
            (
                "description",
                "Description :",
                "Veuillez entrer une Description pour le tournoi.\n"
                "Si vous appuyez sur la touche 'Entrée' sans rien saisir, "
                "vous aurez la possibilité d'annuler l'opération.\n"
                "\n❗️ Attention : Ce champ est obligatoire.",
            ),
            (
                "rounds_count",
                "Nombre de rounds (laisser vide pour 4 par défaut) :",
                "Veuillez entrer le nombre de rounds pour le tournoi.\n"
                "Si vous appuyez sur la touche 'Entrée' sans rien saisir, "
                "vous aurez la possibilité d'annuler l'opération.\n"
                "\n❗️ Attention : Ce champ est obligatoire.",
            ),
        ]

        while self.current_step < len(steps):
            attr, message, instruction = steps[self.current_step]

            if attr == "rounds_count":
                value = self.get_rounds_count_with_default(message)
            else:
                value = self.text_with_cancel(message, instruction)

            if value == "edit":
                self.edit_info()
                continue
            elif value is None:
                return None

            setattr(self, attr, value)
            self.current_step += 1

        return self.confirm_tournament_creation()

    def text_with_cancel(self, message, long_instruction):
        """
        Capture un texte avec la possibilité d'annuler ou d'éditer une étape précédente.
        """
        while True:
            text_input = inquirer.text(
                message=f"{message}",
                long_instruction=f"{long_instruction}\n\n{self.get_formatted_info_table()}",
                style=self.custom_style,
                qmark="",
                amark="",
            ).execute()
            clear_console()

            if text_input == "":

                longest_choice_length = max(
                    len("Continuer la création"),
                    len("Éditer une information"),
                    len("Annuler la création du tournoi")
                    )

                choice = inquirer.select(
                    message="\nLe champ ne peut pas être vide. Que souhaitez-vous faire ?\n",
                    long_instruction="Vous pouvez soit continuer à créer le tournoi, "
                    "soit éditer une information déjà saisie, "
                    "soit annuler l'opération.",
                    choices=[
                        Choice(value="continue", name="Continuer la création"),
                        Choice(value="edit", name="Éditer une information"),
                        Separator(line="-" * longest_choice_length),
                        Choice(value="cancel", name="Annuler la création du tournoi"),
                    ],
                    style=self.custom_style,
                    pointer="❯",
                    qmark="",
                    show_cursor=False,
                ).execute()
                clear_console()

                if choice == "cancel":
                    clear_console()
                    return None
                elif choice == "edit":
                    return "edit"
                elif choice == "continue":
                    clear_console()
                    continue
            else:
                return text_input

    def get_formatted_info_table(self):
        """
        Retourne une table formatée contenant les informations saisies pour le tournoi.
        """
        plain_console = Console(force_terminal=False)
        table = Table(show_header=True, box=box.SQUARE, show_lines=True)
        table.add_column("Informations du tournoi", justify="left")
        table.add_column("Valeur saisie", justify="left")
        table.add_row("Nom du tournoi", self.name or "")
        table.add_row("Localisation", self.location or "")
        table.add_row("Date de début", self.start_date or "")
        table.add_row("Date de fin", self.end_date or "")
        table.add_row("Description", self.description or "")
        table.add_row("Nombre de rounds", str(self.rounds_count) or "")

        with plain_console.capture() as capture:
            plain_console.print(table)

        return capture.get()

    def confirm_tournament_creation(self):
        """
        Confirme la création du tournoi après avoir vérifié les informations saisies.
        """
        while True:
            confirmation = inquirer.select(
                message=f"\nConfirmez-vous la création du tournoi {self.name} ?\n",
                long_instruction="Nous vous invitons à vérifier les informations saisies :\n"
                f"\n{self.get_formatted_info_table()}\n"
                "Puis à confirmer si vous souhaitez créer ce tournoi, éditer une information ou annuler l'opération.",
                choices=[
                    Choice(value="yes", name="Créer le tournoi"),
                    Choice(value="edit", name="Éditer une information"),
                    Choice(value="no", name="Annuler"),
                ],
                style=self.custom_style,
                pointer="❯",
                qmark="",
                show_cursor=False,
            ).execute()

            if confirmation == "yes":
                return self.name, self.location, self.start_date, self.end_date, self.description, self.rounds_count
            elif confirmation == "edit":
                edit_choice = self.edit_info()
                if edit_choice == "cancel":
                    continue
            elif confirmation == "no":
                clear_console()
                return None

    def edit_info(self):
        """
        Permet à l'utilisateur d'éditer les informations saisies pour le tournoi.
        """
        choices = []
        if self.name:
            choices.append(Choice(value="name", name="Nom du tournoi"))
        if self.location:
            choices.append(Choice(value="location", name="Localisation"))
        if self.start_date:
            choices.append(Choice(value="start_date", name="Date de début"))
        if self.end_date:
            choices.append(Choice(value="end_date", name="Date de fin"))
        if self.description:
            choices.append(Choice(value="description", name="Description"))
        if self.rounds_count:
            choices.append(Choice(value="rounds_count", name="Nombre de rounds"))

        choices.append(Separator(line="-" * 30))
        choices.append(Choice(value="cancel", name="Sortir du mode édition"))

        choice = inquirer.select(
            message="Quelle information souhaitez-vous éditer ?",
            choices=choices,
            style=self.custom_style,
            pointer="❯",
            qmark="",
            show_cursor=False,
            long_instruction="Veuillez choisir l'information que vous souhaitez éditer ou "
            "sortez de l'édition pour continuer la création du tournoi.\n"
            f"\n{self.get_formatted_info_table()}",
        ).execute()

        if choice == "cancel":
            clear_console()
            return None

        if choice == "name":
            self.name = self.text_with_cancel(
                "Nom du tournoi :",
                "Veuillez entrer le Nom du tournoi."
            )
        elif choice == "location":
            self.location = self.text_with_cancel(
                "Localisation :",
                "Veuillez entrer la Localisation du tournoi."
            )
        elif choice == "start_date":
            self.start_date = self.text_with_cancel(
                "Date de début (YYYY-MM-DD) :",
                "Veuillez entrer la Date de début du tournoi."
            )
        elif choice == "end_date":
            self.end_date = self.text_with_cancel(
                "Date de fin (YYYY-MM-DD) :",
                "Veuillez entrer la Date de fin du tournoi."
            )
        elif choice == "description":
            self.description = self.text_with_cancel(
                "Description :",
                "Veuillez entrer une Description pour le tournoi."
            )
        elif choice == "rounds_count":
            self.rounds_count = int(self.text_with_cancel(
                "Nombre de rounds (laisser vide pour 4 par défaut) :",
                "Veuillez entrer le nombre de rounds pour le tournoi.") or 4
            )

        return choice

    def get_rounds_count_with_default(self, message):
        """
        Capture le nombre de rounds avec une valeur par défaut.
        """
        while True:
            rounds_input = inquirer.text(
                message=f"{message}",
                long_instruction=(
                    "Appuyez sur 'Entrée' sans saisir de valeur pour utiliser la valeur par défaut de 4."
                    f"\n\n{self.get_formatted_info_table()}"
                ),
                style=self.custom_style,
                qmark="",
                amark="",
            ).execute().strip()

            if rounds_input == "":
                # Applique la valeur par défaut si aucune saisie n'est faite
                return 4
            else:
                try:
                    rounds_count = int(rounds_input)
                    return rounds_count
                except ValueError:
                    self.show_message("Veuillez entrer un nombre valide pour les rounds.")
                    continue

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

    def select_tournament(self, action, tournaments):
        """
        Affiche une liste de tournois à sélectionner et capture le choix de l'utilisateur.

        Args:
            tournaments (list): La liste des tournois.

        Returns:
            str: Le choix de l'utilisateur.
        """

        longest_choice_length = max(
            max(len(f"🏆 {tournament['name']}") for tournament in tournaments),
            len("Retour au menu précédent")
        )

        choices = [
            Choice(value=i, name=f"🏆 {tournament['name']}") for i, tournament in enumerate(tournaments)] + [
            Separator(line="-" * (longest_choice_length + 1)),
            Choice(value="main_menu", name="Retour au menu précédent"),
        ]

        choice = inquirer.select(
            message=f"\nVeuillez sélectionner le tournoi à {action} :\n",
            long_instruction="\nVeuillez choisir parmis la liste des tournois disponibles, "
            f"celui que vous voulez {action}",
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
        longest_choice_length = max(
            len("Ajouter des joueurs au tournoi"),
            len("Retirer des joueurs au tournoi"),
            len("Commencer le tournoi"),
            len("Retour au menu précédent"),
        )

        actions = [
            Choice(value="add", name="Ajouter des joueurs au tournoi"),
            Choice(value="remove", name="Retirer des joueurs du tournoi"),
            Choice(value="start", name="Commencer le tournoi"),
            Separator(line="-" * longest_choice_length),
            Choice(value="cancel", name="Retour au menu précédent"),
        ]

        action = inquirer.select(
            message="\nQue souhaitez-vous faire ?\n",
            long_instruction="Dans ce menu, vous avez accès à ces quatre fonctionnalités :"
            "\n\n- Ajouter des joueurs au tournoi (vous pourrez même créer un nouveau joueur)"
            "\n- Retirer des joueurs du tournoi (vous pourrez retirer un joueur du tournoi)"
            "\n- Commencer le tournoi (c'est ici que tout commence !)"
            "\n- Retour au menu précédent (vous pourrez revenir au menu précédent pour les autres fonctionnalités)\n"
            "\n❗️ Attention : Tout ajout, suppression ou démarrage d'un tournoi entraînera"
            "la modification immédiate et automatique des fichiers 'datas/players.json' et 'datas/tournaments.json'",
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
            Choice(value="add", name="Ajouter des joueurs"),
            Separator(line=27 * "-"),
            Choice(value="back", name="Retour au menu précédent"),
            Choice(value="main_menu", name="Retour au menu principal"),
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
        choices.append(Choice("back", name="Retour au menu précédent"))
        choices.append(Choice("main_menu", name="Retour au menu principal"))

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
