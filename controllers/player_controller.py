import pandas as pd

from exceptions import PlayerExistsError
from models.player import Player
from utils.data_manager import PlayerDataManager
from utils.utils import clear_console
from views.player_view import PlayerView


class PlayerController:
    def __init__(self):
        self.data_manager = PlayerDataManager()
        self.players_df = self.load_players()
        self.view = PlayerView()

    def load_players(self):
        self.players_df = self.data_manager.get_data()
        return self.players_df

    def save_players(self):
        self.data_manager.set_data(self.players_df)

    # Cette méthode permet de lancer le menu principal de gestion des joueurs
    def run(self):
        # On boucle en répétant le menu de Gestion des joueurs jusqu'à ce qu'un choix soit effectué
        while True:
            # On affiche le menu de gestion des joueurs (méthode définie dans la classe PlayerView)
            self.view.display_player_menu()
            # On récupère le choix de l'utilisateur (méthode définie dans la classe PlayerView)
            choice = self.view.get_user_choice()
            # Si le choix est "Ajouter un joueur", on clean le terminal et on appelle la méthode add_player()
            if choice == "add_player":
                clear_console()
                self.create_new_player()
            # Si le choix est "Supprimer un joueur", on clean le terminal et on call la méthode delete_player_by_id()
            elif choice == "remove_player":
                clear_console()
                self.delete_player_by_id()
            # Si le choix est "Rechercher un joueur", on clean le terminal et on call la méthode search_player_by_id()
            elif choice == "search_player":
                clear_console()
                self.search_player_by_id()
            # Si le choix est "Liste des joueurs", on clean le terminal et on appelle la méthode list_players()
            elif choice == "player_list":
                clear_console()
                self.list_players()
            # Si le choix est "Retour au menu principal", on clean le terminal et on sort du boucle
            elif choice == "back_to_main_menu":
                clear_console()
                break

    def create_new_player(self):
        """
        Crée un nouveau joueur et l'ajoute à la base de données.

        Fonctionnement général :
        - Récupère les informations du joueur via la vue.
        - Vérifie si le joueur existe déjà dans la base de données en utilisant son identifiant national.
        - Si le joueur existe déjà, lève une exception et affiche un message d'erreur.
        - Sinon, ajoute le nouveau joueur à la base de données et sauvegarde les modifications.
        - Affiche un message de confirmation de l'ajout du joueur.

        La méthode gère également les cas où l'utilisateur annule la création du joueur.
        """

        # Nettoie la console avant de commencer
        clear_console()

        # Récupère les informations du joueur à créer via la vue
        player_info = self.view.get_player_info()

        # Si l'utilisateur a annulé la création du joueur, affiche un message et retourne
        if player_info is None:
            self.view.show_message('Vous avez annulé la création du joueur.\n')
            return

        # Décompose les informations du joueur récupérées en variables distinctes
        last_name, first_name, birth_date, national_id = player_info
        while True:
            try:
                # Crée une instance de joueur avec les informations fournies
                player = Player(first_name, last_name, birth_date, national_id)

                # Vérifie si un joueur avec le même identifiant national existe déjà
                existing_player = self.players_df[
                    self.players_df["national_id"] == player.national_id
                ]

                # Si un joueur existe déjà, lève une exception PlayerExistsError
                if not self.players_df.empty and not existing_player.empty:
                    raise PlayerExistsError(player.national_id)

                # Convertit les informations du joueur en dictionnaire
                player_data = player.to_dict()

                # On concatène le DataFrame des joueurs existants avec le nouveau joueur
                self.players_df = pd.concat([self.players_df, pd.DataFrame([player_data])], ignore_index=True)

                # Sauvegarde les modifications dans le fichier JSON (datas/players.json)
                self.save_players()

                # On recharge les données du joueur
                self.load_players()

                # Nettoie la console
                clear_console()

                # Affiche un message de confirmation
                self.view.show_message(
                    f"\n💾 - Le joueur {player.first_name} {player.last_name} ({player.national_id}) "
                    "a été ajouté avec succès dans la base de données de joueurs.\n"
                )
                break

            except PlayerExistsError as e:
                clear_console()
                self.view.show_message(str(e))

                # Redemande un nouvel identifiant national
                national_id = self.view.get_valid_national_id("Identifiant national :")

                if national_id is None:
                    self.view.show_message("Ajout de joueur annulé.")
                    return
                elif national_id == "edit":
                    # Si l'utilisateur choisit d'éditer les informations
                    edited_info = self.view.edit_info()
                    if edited_info == "cancel":
                        self.view.show_message("Ajout de joueur annulé.")
                        return
                    else:
                        # Reprend les informations éditées
                        last_name = self.view.formatted_last_name
                        first_name = self.view.formatted_first_name
                        birth_date = self.view.formatted_birth_date
                        national_id = self.view.formatted_national_id
                else:
                    # Met à jour seulement l'identifiant national si l'utilisateur en a entré un nouveau
                    player_info = (last_name, first_name, birth_date, national_id)

    def delete_player_by_id(self):
        """
        Permet de supprimer un joueur de la base de données en utilisant son identifiant national.

        Fonctionnement général :
        - Si la base de données des joueurs est vide :
            - Propose à l'utilisateur d'ajouter un joueur ou de revenir au menu précédent.
        - Si la base de données des joueurs n'est pas vide :
            - Affiche la liste des joueurs.
            - Demande à l'utilisateur de saisir l'identifiant national du joueur à supprimer.
            - Si l'identifiant est incorrect (n'existe pas dans la base de données) :
                - Affiche un message d'erreur sous la liste des joueurs.
                - Redemande à l'utilisateur de saisir un identifiant national valide.
            - Si l'identifiant est correct :
                - Affiche les détails du joueur sélectionné.
                - Demande à l'utilisateur de confirmer la suppression.
                - Si l'utilisateur confirme la suppression :
                    - Supprime le joueur de la base de données.
                    - Affiche un message de confirmation de la suppression.
                - Si l'utilisateur annule la suppression :
                    - Affiche un message informant que la suppression a été annulée.

        La méthode continue en boucle jusqu'à ce qu'une action soit confirmée ou annulée.
        """

        # Vérifie si la base de données des joueurs est vide
        if self.players_df.empty:
            # Demande à l'utilisateur s'il souhaite ajouter un joueur
            action = self.view.ask_to_add_player()
            if action == "add_player":
                # Si l'utilisateur choisit d'ajouter un joueur, appelle la méthode de create_new_player()
                self.create_new_player()
            return

        # Initialisation de la variable pour stocker mon message d'erreur de la view
        error_message = None

        while True:
            # Nettoie la console pour une nouvelle itération
            clear_console()

            # Affiche la liste des joueurs
            self.list_players()

            # Si un message d'erreur a été généré lors de l'itération précédente, je l'affiche sous la liste
            if error_message:
                self.view.display_error_message(error_message)
                error_message = None

            # Demande à l'utilisateur de saisir l'identifiant national du joueur à supprimer
            national_id = self.view.get_player_national_id("supprimer", self.list_players)

            # Si l'utilisateur ne saisit rien et choisit de revenir au menu principal, on retourne
            if not national_id:
                return

            # Recherche le joueur correspondant à l'identifiant national saisi
            player = self.players_df[self.players_df["national_id"] == national_id]

            # Si un joueur avec cet identifiant national est trouvé
            if not player.empty:

                # player_info contient les informations du joueur à supprimer
                player_info = player.iloc[0]
                # Données contenues dans player_info si l'identifiant national est : TD2612
                # +------------+-------------+--------------+---------------+
                # | first_name | last_name   | birth_date   | national_id   |
                # +------------+-------------+--------------+---------------+
                # | Thomas     | Dupré       | 26-12-1999   | TD2612        |
                # +------------+-------------+--------------+---------------+

                # Nettoie la console
                clear_console()

                # Affiche les détails du joueur sélectionné
                self.view.show_player(player_info)
                # iloc[0] permet de récupérer le premier élément de la série donc le 1er index du DataFrame
                # Tandis que loc[0] récupère la ligne dont l'étiquette d'index (label) est exactement 0,
                # ce qui peut ne pas être la première ligne du DataFrame.

                # Demander la confirmation de la suppression
                if self.view.confirm_deletion():

                    # Nettoie la console
                    clear_console()

                    # Supprime le joueur de la base de données
                    # J'utilise une condition pour filtrer les lignes du DataFrame :
                    # self.players_df["national_id"] != national_id
                    # Cette condition ca me retourner une série de valeurs True ou False :
                    # - True si la valeur dans "national_id" est différente de "national_id" spécifié en input
                    # - False si la valeur correspond à "national_id" spécifié en input

                    # Exemple :
                    # Pour un "national_id" à supprimer égal à "TD2612" (ce qui a été saisi en input),
                    # cela produit :
                    # +------------+-------------+--------------+---------------+--------+
                    # | first_name | last_name   | birth_date   | national_id   | Result |
                    # +------------+-------------+--------------+---------------+--------+
                    # | John       | Doe         | 01-01-1990   | JD1990        | True   |
                    # | Thomas     | Dupré       | 26-12-1999   | TD2612        | False  |
                    # | Jane       | Smith       | 05-05-1985   | JS1985        | True   |
                    # +------------+-------------+--------------+---------------+--------+

                    # Le code self.players_df[self.players_df["national_id"] != national_id]
                    # filtre le DataFrame, et conserve uniquement les lignes où le résultat est True
                    # Ça veut dire que la ligne où "national_id" est égale à "TD2612" (qui retourne False) sera exclue.

                    self.players_df = self.players_df[self.players_df["national_id"] != national_id]

                    # DataFrame après suppression
                    # +------------+-------------+--------------+---------------+
                    # | first_name | last_name   | birth_date   | national_id   |
                    # +------------+-------------+--------------+---------------+
                    # | John       | Doe         | 01-01-1990   | JD1990        |
                    # | Jane       | Smith       | 05-05-1985   | JS1985        |
                    # +------------+-------------+--------------+---------------+

                    # Sauvegarde les modifications dans le fichier JSON (datas/players.json)
                    self.save_players()

                    # Afficher un message de confirmation en utilisant les informations du joueur supprimé
                    self.view.show_message(
                        "\n🗑️ - Le joueur "
                        f"{player_info['first_name']} {player_info['last_name']} ({player_info['national_id']}) "
                        "a été supprimé avec succès.\n"
                    )

                    # Sortir de la boucle
                    break

                else:
                    # Nettoie la console
                    clear_console()

                    # Affiche un message d'information
                    self.view.show_message(
                        "Vous avez [bold red]annulé[/bold red] "
                        "la suppression du joueur "
                        f"[bold blue]{player_info['first_name']} {player_info['last_name']} "
                        f"({player_info['national_id']})[/bold blue].\n")
                    break
            else:
                # Stocker le message d'erreur pour l'afficher sous le tableau des joueurs lors de la future itération
                error_message = national_id

    def search_player_by_id(self):
        """
        Permet de rechercher un joueur dans la base de données en utilisant son identifiant national.

        Fonctionnement général :
        - Si la base de données des joueurs est vide :
            - Propose à l'utilisateur d'ajouter un joueur ou de revenir au menu précédent.
        - Si la base de données des joueurs n'est pas vide :
            - Affiche la liste des joueurs.
            - Demande à l'utilisateur de saisir l'identifiant national du joueur à rechercher.
            - Si l'identifiant est incorrect (n'existe pas dans la base de données) :
                - Affiche un message d'erreur sous la liste des joueurs.
                - Redemande à l'utilisateur de saisir un identifiant national valide.
            - Si l'identifiant est correct :
                - Affiche les détails du joueur trouvé.
                - Sort de la boucle après avoir affiché le joueur.

        La méthode continue en boucle jusqu'à ce qu'un joueur soit trouvé ou qu'on choisisse de revenir au menu.
        """

        # Vérifie si la base de données des joueurs est vide
        if self.players_df.empty:
            # Demande à l'utilisateur s'il souhaite ajouter un joueur
            action = self.view.ask_to_add_player()
            if action == "add_player":
                # Si l'utilisateur choisit d'ajouter un joueur, appelle la méthode de create_new_player()
                self.create_new_player()
            return

        # Initialisation de la variable pour stocker mon message d'erreur de la view
        error_message = None

        while True:
            # Nettoie la console pour une nouvelle itération
            clear_console()

            # Affiche la liste des joueurs
            self.list_players()

            # Si un message d'erreur a été généré lors de l'itération précédente, je l'affiche sous la liste
            if error_message:
                self.view.display_error_message(error_message)
                error_message = None

            # Demande à l'utilisateur de saisir l'identifiant national du joueur à rechercher
            national_id = self.view.get_player_national_id("rechercher", self.list_players)

            # Si l'utilisateur ne saisit rien et choisit de revenir au menu principal, on retourne
            if not national_id:
                return

            # Recherche le joueur correspondant à l'identifiant national saisi
            player = self.players_df[self.players_df["national_id"] == national_id]

            # Si un joueur avec cet identifiant national est trouvé
            if not player.empty:

                # Récupère les informations du joueur
                player_info = player.iloc[0]

                # Nettoie la console
                clear_console()

                # Affiche les détails du joueur trouvé
                self.view.show_player(player_info)

                # Sort de la boucle une fois le joueur trouvé et affiché
                break

            else:
                # Stocker le message d'erreur pour l'afficher sous le tableau des joueurs lors de la future itération
                error_message = national_id

    def list_players(self):
        if self.players_df.empty:
            self.view.show_message("Oh-oh ! La base de données des joueurs est actuellement vide.\n"
                                   "\nCommencez par ajouter au moins un joueur 👇\n")
        else:
            self.view.list_players(self.players_df)

    def get_player_by_national_id(self, national_id):
        player_data = self.players_df[self.players_df["national_id"].str.strip() == national_id.strip()]
        if not player_data.empty:
            return Player.from_dict(player_data.iloc[0].to_dict())
        else:
            print(f"Erreur : Le joueur {national_id} n'a pas été trouvé dans players_df.")
            return None
