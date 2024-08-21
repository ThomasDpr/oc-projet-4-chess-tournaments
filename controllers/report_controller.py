import os

import pandas as pd

from models.player import Player
from models.round import Round
from utils.utils import clear_console, sanitize
from views.report_view import ReportView


class ReportController:
    def __init__(self, players_df, tournaments_df, player_controller):
        self.players_df = players_df
        self.tournaments_df = tournaments_df
        self.player_controller = player_controller

        self.view = ReportView()

    def run(self):
        while True:
            self.view.show_menu()
            choice = self.view.get_user_choice()

            self.player_controller.load_players()
            self.players_df = self.player_controller.players_df

            if choice == "1":
                clear_console()
                self.list_players_alphabetically()
            elif choice == "2":
                clear_console()
                self.list_tournaments()
            elif choice == "3":
                clear_console()
                self.show_tournament_details()
            elif choice == "4":
                clear_console()
                self.list_tournament_players_alphabetically()
            elif choice == "5":
                clear_console()
                self.list_tournament_rounds_and_matches()
            elif choice == "6":
                clear_console()
                break

    def reload_players_data(self):
        """Recharger les données des joueurs depuis le PlayerController."""
        self.player_controller.load_players()
        self.players_df = self.player_controller.players_df

    def list_players_alphabetically(self):
        self.reload_players_data()

        if self.players_df.empty or self.players_df is None:
            self.view.show_message("Aucun joueur trouvé.")
        else:
            # Recharger les données à partir du fichier pour s'assurer qu'elles sont à jour
            self.players_df = self.player_controller.data_manager.get_data()
            players_sorted = self.players_df.sort_values(by=["first_name", "last_name"])
            self.view.list_players(players_sorted)

            export_choice = self.view.ask_export_choice()
            if export_choice == "Exporter":
                format_choice = self.view.ask_export_format()
                if format_choice != "Annuler":
                    self.export_players_alphabetically(players_sorted, format_choice)

    def export_players_alphabetically(self, players_sorted, format_choice):
        file_name = "players_list"
        file_path = f"reports/players/{format_choice.lower()}/{file_name}.{format_choice.lower()}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if format_choice == "TXT":
            content = players_sorted.to_string(index=False)
        elif format_choice == "CSV":
            content = players_sorted.to_csv(index=False)
        elif format_choice == "HTML":
            content = players_sorted.to_html(index=False)

        with open(file_path, "w") as file:
            file.write(content)
        clear_console()
        self.view.show_message(
            f"\n🎉 Rapport exporté avec succès !\n" f"\nFichier exporté à cet endroit : {file_path}\n"
        )

    def list_tournaments(self):
        # Si aucun tournoi n'a été trouvé, afficher le message : Aucun tournoi trouvé.
        if self.tournaments_df.empty:
            self.view.show_message("Aucun tournoi trouvé.")
        # Sinon, afficher les tournois dans un tableau
        else:
            self.view.list_tournaments(self.tournaments_df)

            export_choice = self.view.ask_export_choice()
            if export_choice == "Exporter":
                format_choice = self.view.ask_export_format()
                if format_choice != "Annuler":
                    self.export_tournaments(self.tournaments_df, format_choice)

    def export_tournaments(self, tournaments_df, format_choice):
        file_name = "tournaments_list"
        file_path = f"reports/tournaments/{format_choice.lower()}/{file_name}.{format_choice.lower()}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if format_choice == "TXT":
            content = tournaments_df.to_string(index=False)
        elif format_choice == "CSV":
            content = tournaments_df.to_csv(index=False)
        elif format_choice == "HTML":
            content = tournaments_df.to_html(index=False)

        with open(file_path, "w") as file:
            file.write(content)
        clear_console()
        self.view.show_message(
            f"\n🎉 Rapport exporté avec succès !\n" f"\nFichier exporté à cet endroit : {file_path}\n"
        )

    def show_tournament_details(self):
        if self.tournaments_df.empty:
            self.view.show_message("Aucun tournoi trouvé.")
        else:
            tournament_choices = [(tournament["name"], i) for i, tournament in self.tournaments_df.iterrows()]
            choice = self.view.select_tournament(tournament_choices)
            if choice is not None:
                tournament_data = self.tournaments_df.iloc[choice].to_dict()
                self.view.show_tournament_details(tournament_data)

                export_choice = self.view.ask_export_choice()
                if export_choice == "Exporter":
                    format_choice = self.view.ask_export_format()
                    if format_choice != "Annuler":
                        self.export_tournament_details(tournament_data, format_choice)

    def export_tournament_details(self, tournament_data, format_choice):
        tournament_name = sanitize(
            tournament_data["name"]
        )  # J'utilise ma fonction "sanitize" pour nettoyer le nom du tournoi avant de l'exporter
        file_name = f"tournament_details_{tournament_name}"
        file_path = f"reports/tournaments/{format_choice.lower()}/{file_name}.{format_choice.lower()}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        tournament_df = pd.DataFrame([tournament_data])

        if format_choice == "TXT":
            content = tournament_df.to_string(index=False)
        elif format_choice == "CSV":
            content = tournament_df.to_csv(index=False)
        elif format_choice == "HTML":
            content = tournament_df.to_html(index=False)

        with open(file_path, "w") as file:
            file.write(content)
        clear_console()
        self.view.show_message(
            f"\n🎉 Rapport exporté avec succès !\n" f"\nFichier exporté à cet endroit : {file_path}\n"
        )

        # Afficher la liste des joueurs (A-Z) d'un tournoi sélectionné

    def list_tournament_players_alphabetically(self):
        self.reload_players_data()

        if self.tournaments_df.empty:
            self.view.show_message("Aucun tournoi trouvé.")
            return

        tournament_choices = [(tournament["name"], i) for i, tournament in self.tournaments_df.iterrows()]
        choice = self.view.select_tournament(tournament_choices)

        if choice is None:
            return

        tournament_data = self.tournaments_df.iloc[choice].to_dict()
        clear_console()
        if not tournament_data["players"]:
            self.view.show_message("Aucun joueur n'est inscrit dans ce tournoi.")
            return

        # Récupération des données complètes des joueurs depuis players_df
        players = []
        for player_data in tournament_data["players"]:
            national_id_stripped = player_data["national_id"].strip()
            player_info = self.players_df[
                self.players_df["national_id"].str.strip() == national_id_stripped
            ].iloc[0]
            player = Player.from_dict(player_info.to_dict())
            # Mettre à jour le score du joueur avec le score actuel du tournoi
            player.career_score = player_data["career_score"]
            players.append(player)

        players_sorted = sorted(players, key=lambda x: (x.first_name, x.last_name))
        self.view.list_players(pd.DataFrame([player.to_dict() for player in players_sorted]))

        export_choice = self.view.ask_export_choice()
        if export_choice == "Exporter":
            format_choice = self.view.ask_export_format()
            if format_choice != "Annuler":
                self.export_tournament_players_alphabetically(players_sorted, tournament_data["name"], format_choice)

    def export_tournament_players_alphabetically(self, players_sorted, tournament_name, format_choice):
        tournament_name = sanitize(tournament_name)
        file_name = f"tournament_{tournament_name}_players_list"
        file_path = f"reports/tournaments/{format_choice.lower()}/{file_name}.{format_choice.lower()}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if format_choice == "TXT":
            content = pd.DataFrame(players_sorted).to_string(index=False)
        elif format_choice == "CSV":
            content = pd.DataFrame(players_sorted).to_csv(index=False)
        elif format_choice == "HTML":
            content = pd.DataFrame(players_sorted).to_html(index=False)

        with open(file_path, "w") as file:
            file.write(content)
        clear_console()
        self.view.show_message(
            f"\n🎉 Rapport exporté avec succès !\n" f"\nFichier exporté à cet endroit : {file_path}\n"
        )

    def list_tournament_rounds_and_matches(self):
        self.reload_players_data()

        if self.tournaments_df.empty:
            self.view.show_message("Aucun tournoi trouvé.")
        else:
            tournament_choices = [(tournament["name"], i) for i, tournament in self.tournaments_df.iterrows()]
            choice = self.view.select_tournament(tournament_choices)

            if choice is None:
                return

            tournament_data = self.tournaments_df.iloc[choice].to_dict()
            rounds = [Round.from_dict(round) for round in tournament_data["rounds"]]

            if not rounds:
                self.view.show_message(f"Le tournoi '{tournament_data['name']}' n'a pas encore de rounds.")
                return

            # Appel de la fonction pour afficher les matchs
            self.view.display_rounds_and_matches(tournament_data["name"], rounds, self.players_df)

            export_choice = self.view.ask_export_choice()
            if export_choice == "Exporter":
                format_choice = self.view.ask_export_format()
                if format_choice != "Annuler":
                    self.export_tournament_rounds_and_matches(rounds, tournament_data["name"], format_choice)

    def export_tournament_rounds_and_matches(self, rounds, tournament_name, format_choice):
        tournament_name = sanitize(tournament_name)
        file_name = f"tournament_{tournament_name}_rounds_and_matches"
        file_path = f"reports/tournaments/{format_choice.lower()}/{file_name}.{format_choice.lower()}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        rounds_data = []
        for round_ in rounds:
            for match in round_.matches:
                match_data = {
                    "round": round_.name,
                    "player1_id": match.player1_id,
                    "player2_id": match.player2_id,
                    "score_player1": match.score_player1,
                    "score_player2": match.score_player2,
                }
                rounds_data.append(match_data)

        rounds_df = pd.DataFrame(rounds_data)

        if format_choice == "TXT":
            content = rounds_df.to_string(index=False)
        elif format_choice == "CSV":
            content = rounds_df.to_csv(index=False)
        elif format_choice == "HTML":
            content = rounds_df.to_html(index=False)
        with open(file_path, "w") as file:
            file.write(content)
        clear_console()
        self.view.show_message(
            f"\n🎉 Rapport exporté avec succès !\n" f"\nFichier exporté à cet endroit : {file_path}\n"
        )
