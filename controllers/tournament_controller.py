import pandas as pd

from models.match import Match
from models.player import Player
from models.round import Round
from models.tournament import Tournament
from utils.data_manager import TournamentDataManager
from utils.utils import clear_console
from views.player_view import PlayerView
from views.tournament_view import TournamentView


class TournamentController:
    def __init__(self, player_controller):
        self.data_manager = TournamentDataManager()
        self.tournaments_df = self.data_manager.get_data()
        self.player_controller = player_controller
        self.tournament_view = TournamentView()
        self.player_view = PlayerView()
        self.players_df = self.player_controller.players_df

    def run(self):
        while True:
            self.tournament_view.display_tournament_menu()
            choice = self.tournament_view.get_user_select_choice()

            if choice == "tournament_list":
                clear_console()
                self.list_tournaments()

            elif choice == "add_tournament":
                clear_console()
                self.create_new_tournament()

            elif choice == "start_tournament":
                clear_console()
                result = self.start_tournament()

                if result == "main_menu":
                    return "main_menu"

            elif choice == "resume_tournament":
                clear_console()
                self.resume_tournament()

            elif choice == "back_to_main_menu":
                clear_console()
                break

    # Méthode pour charger les données des tournois
    def load_tournaments(self):
        self.tournaments_df = self.data_manager.get_data()

    # Méthode pour sauvegarder les données des tournois
    def save_tournaments(self):
        self.data_manager.set_data(self.tournaments_df)

    # Méthode pour créer un nouveau tournoi
    def create_new_tournament(self):
        # Récupère les informations du tournoi via la vue
        tournament_info = self.tournament_view.get_tournament_info()
        # Si l'utilisateur a annulé la création du tournoi, affiche un message et retourne
        if tournament_info is None:
            self.tournament_view.show_message("Ajout de tournoi annulé.")
            return

        name, location, start_date, end_date, description, rounds_count = tournament_info
        rounds_count = int(rounds_count) if rounds_count else 4  # Utiliser 4 si aucune valeur n'est fournie
        tournament = Tournament(name, location, start_date, end_date, description, rounds_count)
        tournament_data = tournament.to_dict()

        # Ajoute le nouveau tournoi aux données existantes
        self.tournaments_df = pd.concat([self.tournaments_df, pd.DataFrame([tournament_data])], ignore_index=True)

        clear_console()
        self.tournament_view.show_message(f"🎉 - Le tournoi '{tournament.name}' a été ajouté avec succès.")
        self.save_tournaments()

    def list_tournaments(self):
        clear_console()
        if self.tournaments_df.empty:
            self.tournament_view.show_message("Oh-oh ! La base de données des tournois est actuellement vide.\n"
                                              "\nCommencez par ajouter au moins un tournoi 👇\n")
        else:
            self.tournament_view.list_tournaments(self.tournaments_df)

    def initialize_round(self, tournament):
        round_name = f"Round {tournament.current_round + 1}"
        new_round = Round(round_name)
        tournament.add_round(new_round)
        tournament.current_round += 1  # Incrémenter le numéro de round
        self.update_tournament(tournament)

    def add_players_to_tournament(self, tournament, return_to_menu=False):
        while True:
            # Recharger la liste des joueurs pour obtenir les mises à jour
            self.player_controller.load_players()

            self.player_view.list_players(self.player_controller.players_df)
            player_in_tournament_df = [player.to_dict() for player in tournament.players]
            self.tournament_view.list_players_in_tournament(player_in_tournament_df, self.player_controller.players_df)

            choice = self.tournament_view.get_player_add_choice()

            if choice.lower() == "done":
                if return_to_menu:
                    return
                break
            elif choice.lower() == "new":
                player_info = self.player_view.get_player_info()
                if player_info is None:
                    self.player_view.show_message("Ajout de joueur annulé.")
                    continue

                first_name, last_name, birth_date, national_id = player_info
                try:
                    player = Player(first_name, last_name, birth_date, national_id)
                    player_data = player.to_dict()
                    self.player_controller.players_df = pd.concat(
                        [self.player_controller.players_df, pd.DataFrame([player_data])],
                        ignore_index=True,
                    )
                    self.player_controller.save_players()
                    self.player_controller.load_players()

                    tournament.add_player(player)

                except ValueError as e:
                    self.player_view.show_message(str(e))
            else:
                self.player_controller.load_players()
                player_data = self.player_controller.players_df.loc[
                    self.player_controller.players_df["national_id"] == choice.upper()
                ]

                if not player_data.empty:
                    player = Player.from_dict(player_data.iloc[0].to_dict())
                    tournament.add_player(player)
                else:
                    self.player_view.show_message("Identifiant national invalide ou joueur non trouvé.")
            self.update_tournament(tournament)

    def remove_player_from_tournament(self, tournament):
        while True:
            clear_console()
            if not tournament.players:
                self.tournament_view.show_message("\nIl n'y a actuellement aucun joueur inscrit dans ce tournoi.\n")
                choice = self.tournament_view.show_no_player_actions()
                if choice == "add":
                    self.add_players_to_tournament(tournament, return_to_menu=True)
                    break
                elif choice == "back":
                    clear_console()
                    break
                elif choice == "main_menu":
                    return "main_menu"
            else:
                player_data = [
                    {
                        **self.player_controller.players_df.loc[
                            self.player_controller.players_df["national_id"] == player.national_id
                        ]
                        .iloc[0]
                        .to_dict(),
                        "national_id": player.national_id,
                        "career_score": player.career_score,
                    }
                    for player in tournament.players
                ]
                self.tournament_view.list_players_in_tournament(player_data, self.player_controller.players_df)
                choice = self.tournament_view.select_player_to_remove(player_data)
                if choice == "back":
                    break
                elif choice == "main_menu":
                    return "main_menu"

                player = next((player for player in tournament.players if player.national_id == choice), None)
                if player:
                    tournament.players.remove(player)
                    self.tournament_view.show_message(
                        f"Joueur {player.first_name} {player.last_name} retiré du tournoi {tournament.name}"
                    )
                self.update_tournament(tournament)

    def run_tournament(self, tournament):
        try:
            while tournament.current_round <= tournament.rounds_count:
                round_name = f"Round {tournament.current_round}"
                if len(tournament.rounds) < tournament.current_round:
                    self.initialize_round(tournament)
                round_ = tournament.rounds[-1]
                pairs = tournament.generate_pairs()
                already_played_matches = [match.player1_id for match in round_.matches]
                match_number = 1

                for player1, player2 in pairs:
                    if player1.national_id in already_played_matches:
                        match_number += 1
                        continue

                    match = Match(player1.national_id, player2.national_id)
                    player1_data = self.player_controller.players_df.loc[
                        self.player_controller.players_df["national_id"] == match.player1_id
                    ].iloc[0]
                    player2_data = self.player_controller.players_df.loc[
                        self.player_controller.players_df["national_id"] == match.player2_id
                    ].iloc[0]
                    player1_info = f"{player1_data['first_name']} {player1_data['last_name']} ({match.player1_id})"
                    player2_info = f"{player2_data['first_name']} {player2_data['last_name']} ({match.player2_id})"
                    clear_console()
                    self.tournament_view.create_tournament_tables(
                        tournament, pairs, round_name, match_number, player1_info, player2_info
                    )

                    score1, score2 = self.get_match_result(match, player1_data, player2_data)
                    if score1 is not None and score2 is not None:
                        match.set_scores(score1, score2)
                        self.update_player_scores(match, tournament)
                        round_.add_match(match)
                        self.update_tournament(tournament)
                    match_number += 1

                round_.close_round()
                self.update_tournament(tournament)
                if tournament.current_round < tournament.rounds_count:
                    self.initialize_round(tournament)
                    self.tournament_view.show_message(f"{round_name} terminé")
                else:
                    print(f"\nLe tournoi {tournament.name} est terminé.\n")
                    break

            self.update_tournament(tournament)
            self.save_tournaments()
        except InterruptedError:
            self.update_tournament(tournament)
            self.tournament_view.show_message("\nTournoi interrompu. Vous pouvez reprendre plus tard.\n")

    def get_match_result(self, match, player1, player2):
        return self.tournament_view.get_match_result(player1, player2)

    def update_player_scores_in_players_df(self, match):
        self.player_controller.players_df["career_score"] = self.player_controller.players_df["career_score"].astype(
            float
        )

        player1 = self.player_controller.get_player_by_national_id(match.player1_id)
        if player1:
            player1_filter = self.player_controller.players_df["national_id"] == match.player1_id
            player1_row = self.player_controller.players_df[player1_filter]
            new_career_score_player1 = player1_row.iloc[0]["career_score"] + match.score_player1
            self.player_controller.players_df.loc[player1_filter, "career_score"] = new_career_score_player1

        player2 = self.player_controller.get_player_by_national_id(match.player2_id)
        if player2:
            player2_filter = self.player_controller.players_df["national_id"] == match.player2_id
            player2_row = self.player_controller.players_df[player2_filter]
            new_career_score_player2 = player2_row.iloc[0]["career_score"] + match.score_player2
            self.player_controller.players_df.loc[player2_filter, "career_score"] = new_career_score_player2

        self.player_controller.save_players()

    def update_player_scores_in_tournaments_df(self, match, tournament):
        for player in tournament.players:
            if player.national_id == match.player1_id:
                new_career_score_player1 = player.career_score + match.score_player1
                player.career_score = float(new_career_score_player1)
            elif player.national_id == match.player2_id:
                new_career_score_player2 = player.career_score + match.score_player2
                player.career_score = float(new_career_score_player2)

        self.update_tournament(tournament)

    def update_tournament(self, tournament):
        tournament_data = pd.DataFrame([tournament.to_dict()])
        for i in range(len(self.tournaments_df)):
            if self.tournaments_df.at[i, "name"] == tournament.name:
                self.tournaments_df = pd.concat(
                    [
                        self.tournaments_df.iloc[:i],
                        tournament_data,
                        self.tournaments_df.iloc[i + 1:],
                    ]
                ).reset_index(drop=True)
                break
        self.save_tournaments()

    def update_player_scores(self, match, tournament):
        self.update_player_scores_in_players_df(match)
        self.update_player_scores_in_tournaments_df(match, tournament)

    def start_tournament(self):
        clear_console()
        tournament_choices = self.tournaments_df.to_dict(orient="records")
        if self.tournaments_df.empty:
            self.tournament_view.show_message("Oh-oh ! La base de données des tournois est actuellement vide.\n"
                                              "\nCommencez par ajouter au moins un tournoi 👇\n")
            return
        else:
            choice = self.tournament_view.select_tournament("démarrer", tournament_choices)

        if choice == "main_menu":
            clear_console()
            return
        if choice is not None:
            tournament_data = self.tournaments_df.iloc[choice].to_dict()
            tournament = Tournament.from_dict(tournament_data)
            while True:
                clear_console()
                action = self.tournament_view.show_tournament_actions()
                if action == "add":
                    self.add_players_to_tournament(tournament)
                elif action == "remove":
                    result = self.remove_player_from_tournament(tournament)
                    if result == "main_menu":
                        return "main_menu"
                elif action == "start":
                    clear_console()
                    min_players = tournament.minimum_players_required()
                    if tournament.is_valid_player_count_for_rounds():
                        if tournament.current_round == 0 and len(tournament.players) > 0:
                            self.initialize_round(tournament)
                            self.run_tournament(tournament)
                    elif len(tournament.players) < min_players:
                        self.tournament_view.show_message(
                            f"\nOh-oh ! Le nombre de joueurs est insuffisant pour le nombre de rounds définis.\n"
                            f"\nLe tournoi '{tournament.name}' nécessite au minimum "
                            f"[bold red]{min_players} joueurs[/bold red] pour "
                            f"[bold blue]{tournament.rounds_count} rounds[/bold blue]\n"
                            f"\nChaque joueurs doivent jouer contre un autre joueur au moins une fois.\n"
                            f"\nDonc le nombre de joueurs doit être [underline ]supérieur ou égal[/underline] à "
                            f"[bold red]{min_players} joueurs minimum[/bold red].\n"
                            f"\nActuellement, il y a [bold red]{len(tournament.players)} joueurs[/bold red] "
                            "inscrits dans le tournoi.\n"
                        )
                        choice = self.tournament_view.show_no_player_actions()
                        if choice == "add":
                            self.add_players_to_tournament(tournament, return_to_menu=True)
                            break
                        elif choice == "back":
                            clear_console()
                            break
                        elif choice == "main_menu":
                            return "main_menu"
                    break
                elif action == "cancel":
                    clear_console()
                    break

            clear_console()

    def resume_tournament(self):
        clear_console()
        ongoing_tournaments = self.tournaments_df[
            (self.tournaments_df["current_round"] > 0)
            & (self.tournaments_df["current_round"] < self.tournaments_df["rounds_count"])
        ]

        if ongoing_tournaments.empty:
            self.tournament_view.show_message("Oh-oh ! Actuellement, il n'y a aucun tournoi en cours.\n")
            return

        tournament_choices = ongoing_tournaments.to_dict(orient="records")
        choice = self.tournament_view.select_tournament("reprendre", tournament_choices)

        if choice == "main_menu":
            return

        if choice is not None:
            tournament_data = ongoing_tournaments.iloc[choice].to_dict()
            tournament = Tournament.from_dict(tournament_data)
            self.run_tournament(tournament)

            clear_console()
