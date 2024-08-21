from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich.console import Console
from rich.table import Table, box

from exceptions import InvalidDateFormatError, InvalidNationalIdError
from utils.utils import (
    capitalize_name,
    clear_console,
    normalize_national_id,
    parse_birth_date,
)
from views.base_view import BaseView


class PlayerView(BaseView):
    def __init__(self):
        """
        Initialise la vue des joueurs en appelant le constructeur de la classe de base.
        Initialise également les attributs pour stocker les informations du joueur.
        """

        super().__init__()
        self.first_name = ""
        self.last_name = ""
        self.birth_date = ""
        self.national_id = ""
        self.formatted_last_name = ""
        self.formatted_first_name = ""
        self.formatted_birth_date = ""
        self.formatted_national_id = ""
        self.current_step = 0

    def ask_to_add_player(self):
        """
        Propose à l'utilisateur d'ajouter un joueur ou de revenir au menu précédent
        lorsque la base de données des joueurs est vide.
        """
        longest_choice_length = max(len("🆕 Ajouter un joueur"), len("🔙 Revenir au menu précédent"))
        choices = [
            Choice(value="add_player", name="🆕 Ajouter un joueur"),
            Separator(line="-" * (longest_choice_length + 1)),
            Choice(value="back_to_menu", name="🔙 Revenir au menu précédent"),
        ]
        choice = inquirer.select(
            message="La base de données des joueurs est vide. Que souhaitez-vous faire ?\n",
            long_instruction="Vous pouvez ajouter un nouveau joueur à la base de données "
            "ou revenir au menu précédent.",
            choices=choices,
            style=self.custom_style,
            pointer="❯",
            qmark="",
            show_cursor=False,
        ).execute()

        return choice

    def reset_info(self):
        """
        Réinitialise les informations du joueur.
        """

        self.first_name = ""
        self.last_name = ""
        self.birth_date = ""
        self.national_id = ""
        self.formatted_last_name = ""
        self.formatted_first_name = ""
        self.formatted_birth_date = ""
        self.formatted_national_id = ""
        self.current_step = 0

    def display_player_menu(self):
        """
        Affiche le menu de gestion des joueurs et capture le choix de l'utilisateur.
        """
        # Calcul de la longueur du choix le plus long pour ajuster la taille du Separator
        longest_choice_length = max(
            len("Ajouter un joueur"),
            len("Supprimer un joueur"),
            len("Rechercher un joueur"),
            len("Afficher tous les joueurs"),
            len("Retour au menu principal"),
        )

        # Définition des options du menu de gestion des joueurs
        menu_options = [
            Choice(value="add_player", name="Ajouter un joueur"),
            Choice(value="remove_player", name="Supprimer un joueur"),
            Choice(value="search_player", name="Rechercher un joueur"),
            Choice(value="player_list", name="Afficher tous les joueurs"),
            Separator(line="-" * longest_choice_length),
            Choice(value="back_to_main_menu", name="Retour au menu principal"),
        ]

        # Affichage du menu de gestion des joueurs en utilisant InquirerPy
        self.choice = inquirer.select(
            message="Gestion des joueurs\n",
            long_instruction="\nDans le menu de Gestion des joueurs, vous avez accès à ces cinq fonctionnalités :\
            \n\n- Ajouter un joueur (celui-ci sera créé puis enregistré en base de données)\
            \n- Supprimer un joueur (celui-ci sera supprimé de la base de données après confirmation de votre part)\
            \n- Rechercher un joueur (vous pourrez visualiser les informations complète du joueur)\
            \n- Afficher tous les joueurs (vous pourrez visualiser les informations complète de tous les joueurs)\
            \n- Retour au menu principal (vous pourrez revenir au menu principal pour voir les autres fonctionnalités)\
            \n\n❗ Attention : Tout ajout ou suppression d'un joueur entraînera"
            "la modification immédiate et automatique du fichier 'datas/players.json'",
            choices=menu_options,
            pointer="❯",
            qmark="",
            style=self.custom_style,
            show_cursor=False,
        ).execute()

    def get_user_choice(self):
        """
        Retourne le choix de l'utilisateur capturé par display_player_menu.
        """

        return self.choice

    def update_formatted_info(self):
        """
        Met à jour les informations formatées du joueur en utilisant les fonctions dans utils/utils.py.
        Gère les exceptions liées au format de la date et à l'identifiant national d'un joueur.
        """

        try:
            self.formatted_last_name = capitalize_name(self.last_name)
            self.formatted_first_name = capitalize_name(self.first_name)
            self.formatted_birth_date = (
                parse_birth_date(self.birth_date).strftime("%d-%m-%Y") if self.birth_date else ""
            )
            self.formatted_national_id = normalize_national_id(self.national_id) if self.national_id else ""
        except InvalidDateFormatError as e:
            self.formatted_birth_date = ""
            self.show_message(str(e))
        except InvalidNationalIdError as e:
            self.formatted_national_id = ""
            self.show_message(str(e))

    def get_player_info(self):
        """
        Capture les informations du joueur en interrogeant l'utilisateur étape par étape.
        Gère l'édition des informations et la confirmation de la création du joueur.
        """

        self.reset_info()

        # Définition des étapes pour capturer les informations du joueur
        steps = [
            (
                "last_name",
                "Nom de famille :",
                "Veuillez entrer le Nom de famille du joueur\n"
                "Si vous appuyez sur la touche 'Entrée' sans rien saisir, "
                "vous aurez la possibilité d'annuler l'opération.\n"
                "\n❗️ Attention : Ce champ est obligatoire.",
            ),
            (
                "first_name",
                "Prénom :",
                "Veuillez entrer le Prénom du joueur\n"
                "Si vous appuyez sur la touche 'Entrée' sans rien saisir, "
                "vous aurez la possibilité d'annuler l'opération.\n"
                "\n❗️ Attention : Ce champ est obligatoire.",
            ),
            (
                "birth_date",
                "Date de naissance :",
                "Veuillez entrer la Date de naissance du joueur dans le format JJ-MM-AAAA , JJ/MM/AAAA ou JJMMAAAA.\n"
                "Si vous appuyez sur la touche 'Entrée' sans rien saisir, "
                "vous aurez la possibilité d'annuler l'opération.\n"
                "\n❗️ Attention : Ce champ est obligatoire.",
            ),
            (
                "national_id",
                "Identifiant national :",
                "Veuillez entrer l'Identifiant national du joueur dans le format AB1234.\n"
                "Si vous appuyez sur la touche 'Entrée' sans rien saisir, "
                "vous aurez la possibilité d'annuler l'opération.\n"
                "\n❗️ Attention : Ce champ est obligatoire.",
            ),
        ]

        while self.current_step < len(steps):
            attr, message, instruction = steps[self.current_step]
            if attr == "birth_date":
                value = self.get_valid_date(message)
            elif attr == "national_id":
                value = self.get_valid_national_id(message)
            else:
                value = self.text_with_cancel(message, instruction)

            if value == "edit":
                self.edit_info()
                continue
            elif value is None:
                return None

            setattr(self, attr, value)
            self.update_formatted_info()
            self.current_step += 1

        return self.confirm_player_creation()

    def get_valid_date(self, message):
        """
        Capture et valide la date de naissance du joueur.
        """

        while True:
            date_input = self.text_with_cancel(
                message,
                "Veuillez entrer la Date de naissance du joueur dans le format JJ-MM-AAAA , JJ/MM/AAAA ou JJMMAAAA.\n"
                "Si vous appuyez sur la touche 'Entrée' sans rien saisir,"
                "vous aurez la possibilité d'annuler l'opération.\n"
                "\n❗️ Attention : Ce champ est obligatoire.",
            )
            if date_input is None or date_input == "edit":
                return date_input
            try:
                return parse_birth_date(date_input).strftime("%d-%m-%Y")
            except InvalidDateFormatError as e:
                self.show_message(str(e))
                continue

    def get_valid_national_id(self, message):
        """
        Capture et valide l'identifiant national du joueur.
        """

        while True:
            national_id_input = self.text_with_cancel(
                message,
                "Veuillez entrer l'Identifiant national du joueur dans le format AB1234.\n"
                "Si vous appuyez sur la touche 'Entrée' sans rien saisir,"
                "vous aurez la possibilité d'annuler l'opération.\n"
                "\n❗️ Attention : Ce champ est obligatoire.",
            )
            if national_id_input is None or national_id_input == "edit":
                return national_id_input

            try:
                return normalize_national_id(national_id_input)
            except InvalidNationalIdError as e:
                self.show_message(str(e))
                continue

    def text_with_cancel(self, message, long_instruction):
        """
        Capture un texte avec la possibilité d'annuler ou d'éditer une étape précédente.
        """

        while True:
            # Capture de l'entrée utilisateur avec possibilité d'annuler ou d'éditer
            text_input = inquirer.text(
                message=f"{message}",
                long_instruction=f"{long_instruction}\n\n{self.get_formatted_info_table()}",
                style=self.custom_style,
                qmark="",
                amark="",
            ).execute()
            clear_console()

            # Si l'utilisateur ne saisit rien, afficher des options supplémentaires
            if text_input == "":
                longest_choice_length = max(
                    len("Continuer la création"),
                    len("Éditer une information"),
                    len("Annuler la création du joueur")
                    )

                choice = inquirer.select(
                    message="\nLe champ ne peut pas être vide. Que souhaitez-vous faire ?\n",
                    long_instruction="Vous pouvez soit continuer à créer le joueur "
                    "soit éditer une information déjà saisie, "
                    "soit annuler l'opération.",
                    choices=[
                        Choice(value="continue", name="Continuer la création"),
                        Choice(value="edit", name="Éditer une information"),
                        Separator(line="-" * (longest_choice_length)),
                        Choice(value="cancel", name="Annuler la création du joueur"),
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
        Retourne une table formatée contenant les informations saisies pour le joueur.
        """

        plain_console = Console(force_terminal=False)
        table = Table(show_header=True, box=box.SQUARE, show_lines=True)
        table.add_column("Informations du joueur", justify="left")
        table.add_column("Valeur saisie", justify="left")
        table.add_row("Nom de famille", self.formatted_last_name or "")
        table.add_row("Prénom", self.formatted_first_name or "")
        table.add_row("Date de naissance", self.formatted_birth_date or "")
        table.add_row("Identifiant national", self.formatted_national_id or "")

        # Nous pouvons aussi utiliser la méthode stringIO de Python pour capturer la sortie de la table
        with plain_console.capture() as capture:
            plain_console.print(table)

        return capture.get()

    def get_player_national_id(self, action, list_players_callback=None):
        """
        Demande à l'utilisateur de saisir l'identifiant national du joueur pour une action spécifique.
        Soit pour le supprimer, soit pour le rechercher.
        """
        while True:
            national_id = inquirer.text(
                message=f"\nVeuillez saisir l'identifiant national du joueur à {action} :",
                long_instruction="\nVeuillez entrer l'identifiant national unique du joueur "
                f"que vous souhaitez {action}.\n"
                "Cet identifiant sera utilisé pour retrouver les informations du joueur dans la base de données.",
                style=self.custom_style,
                qmark="",
                amark="",
            ).execute().strip().upper()

            if not national_id:
                clear_console()
                longest_choice_length = max(
                    len("🔄 Rechercher à nouveau un joueur à " + action), len("🔙 Revenir au menu précédent")
                    )
                choice = inquirer.select(
                    message="\nLe champ est vide, que souhaitez-vous faire ?\n",
                    choices=[
                        Choice(value="retry", name="🔄 Rechercher à nouveau un joueur à " + action),
                        Separator(line="-" * (longest_choice_length + 1)),
                        Choice(value="back", name="🔙 Revenir au menu précédent")
                    ],
                    style=self.custom_style,
                    pointer="❯",
                    qmark="",
                    show_cursor=False,
                ).execute()

                if choice == "back":
                    clear_console()
                    return None
                elif choice == "retry":
                    clear_console()
                    if list_players_callback:
                        list_players_callback()
                    continue

            return national_id

    def confirm_deletion(self):
        """
        Demande une confirmation avant de supprimer un joueur.
        """

        confirmation = inquirer.select(
            message="\nÊtes-vous sûr de vouloir supprimer ce joueur ?",
            long_instruction="\n❗️ La suppression d'un joueur est irréversible.\n"
            "Veuillez confirmer si vous souhaitez réellement supprimer ce joueur.",
            choices=[Choice(value="yes", name="Oui"), Choice(value="no", name="Non")],
            style=self.custom_style,
            pointer="❯",
            qmark="",
            show_cursor=False,
        ).execute()
        return confirmation == "yes"

    def edit_info(self):
        """
        Permet à l'utilisateur d'éditer les informations saisies pour le joueur.
        """

        choices = []
        if self.last_name:
            choices.append(Choice(value="last_name", name="Nom de famille"))
        if self.first_name:
            choices.append(Choice(value="first_name", name="Prénom"))
        if self.birth_date:
            choices.append(Choice(value="birth_date", name="Date de naissance"))
        if self.national_id:
            choices.append(Choice(value="national_id", name="Identifiant national"))

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
            "sortez de l'édition pour continuer la création du joueur.\n"
            f"\n{self.get_formatted_info_table()}",
        ).execute()

        if choice == "cancel":
            clear_console()
            return None

        if choice == "last_name":
            self.last_name = self.text_with_cancel("Nom de famille :", "Veuillez entrer le Nom de famille du joueur")
        elif choice == "first_name":
            self.first_name = self.text_with_cancel("Prénom :", "Veuillez entrer le Prénom du joueur")
        elif choice == "birth_date":
            self.birth_date = self.get_valid_date("Date de naissance :")
        elif choice == "national_id":
            self.national_id = self.get_valid_national_id("Identifiant national :")

        self.update_formatted_info()
        return choice

    def show_player(self, player):
        """
        Affiche les informations d'un joueur trouvé en utilisant RichTable.
        """

        table = Table(title="Joueur trouvé", box=box.SQUARE, header_style="bold magenta")
        table.add_column("Prénom")
        table.add_column("Nom de famille")
        table.add_column("Date de naissance")
        table.add_column("Identifiant national")
        table.add_column("Score de carrière")
        table.add_row(
            player["first_name"],
            player["last_name"],
            player["birth_date"],
            player["national_id"],
            str(player["career_score"]),
        )
        self.console.print(table)

    def list_players(self, players_df):
        """
        Affiche la liste de tous les joueurs sous forme de table en utilisant RichTable,
        avec des noms de colonnes cohérents avec ceux utilisés dans show_player.
        """

        # Création de la table all_players
        table_all_players = Table(title="Liste des joueurs", box=box.SQUARE, show_lines=True)

        # ajout des colonnes avec les mêmes noms que dans show_player
        table_all_players.add_column("Prénom", justify="left", header_style="bold magenta")
        table_all_players.add_column("Nom de famille", justify="left", header_style="bold magenta")
        table_all_players.add_column("Date de naissance", justify="left", header_style="bold magenta")
        table_all_players.add_column("Identifiant national", justify="left", header_style="bold magenta")
        table_all_players.add_column("Score de carrière", justify="left", header_style="bold magenta")

        # Remplissage de la table avec les données des joueurs
        for index, row in players_df.iterrows():
            table_all_players.add_row(
                row["first_name"],
                row["last_name"],
                row["birth_date"],
                row["national_id"],
                str(row["career_score"])
            )

        # Afficher la table dans la console
        self.console.print(table_all_players)

    def display_error_message(self, national_id):
        """
        Affiche un message d'erreur sous la forme d'une alerte avec l'identifiant fourni.
        """
        self.console.print(f"\n❌ - Aucun joueur trouvé avec l'identifiant national [bold blue]{national_id}[/bold blue].\n", style="bold red")  # noqa: E501

    def show_message(self, message):
        """
        Affiche un message.
        """

        self.console.print(message)

    def confirm_player_creation(self):
        """
        Confirme la création d'un joueur après avoir vérifié les informations saisies.
        """

        while True:
            # Affiche les informations formatées pour confirmation
            self.update_formatted_info()
            confirmation = inquirer.select(
                message="\nConfirmez-vous la création du joueur "
                f"{self.formatted_last_name} {self.formatted_first_name} ?\n",
                long_instruction="Nous vous invitons à vérifier les informations saisies :\n"
                f"\n{self.get_formatted_info_table()}\n"
                "Puis à confirmer si vous souhaitez créer ce joueur, éditer une information ou annuler l'opération.",
                choices=[
                    Choice(value="yes", name="Créer le joueur"),
                    Choice(value="edit", name="Éditer une information"),
                    Choice(value="no", name="Annuler"),
                ],
                style=self.custom_style,
                pointer="❯",
                qmark="",
                show_cursor=False,
            ).execute()

            if confirmation == "yes":
                return self.last_name, self.first_name, self.birth_date, self.national_id
            elif confirmation == "edit":
                edit_choice = self.edit_info()
                if edit_choice == "cancel":
                    continue
            elif confirmation == "no":
                clear_console()
                return None
