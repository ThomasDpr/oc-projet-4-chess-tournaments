import os
import random
from datetime import timedelta

import pandas as pd
from faker import Faker
from faker.providers import BaseProvider
from rich.console import Console
from rich.table import Table, box

fake = Faker("fr_FR")


# Création d'un fournisseur personnalisé pour les noms de tournois d'échecs
class ChessTournamentProvider(BaseProvider):
    def __init__(self, generator):
        super().__init__(generator)
        self.used_names = set()
        self.used_descriptions = set()

    def chess_tournament_name(self):
        names = [
            "Tournoi des Maîtres",
            "Championnat des Échecs",
            "Open d'Échecs",
            "Coupe des Stratèges",
            "Grand Prix des Échecs",
            "Festival des Échecs",
            "Rencontre des Grands Maîtres",
            "Tournoi International d'Échecs",
            "Challenge des Échecs",
            "Olympiade des Échecs",
        ]
        name = random.choice(names)
        while name in self.used_names:
            name = random.choice(names)
        self.used_names.add(name)
        return name

    def chess_tournament_description(self):
        descriptions = [
            "Un tournoi prestigieux pour les meilleurs joueurs d'échecs.",
            "Une compétition intense réunissant des passionnés d'échecs du monde entier.",
            "Un événement annuel où se confrontent les stratèges les plus talentueux.",
            "Un tournoi international d'échecs avec des participants de haut niveau.",
            "Un rendez-vous incontournable pour les amateurs et professionnels des échecs.",
            "Un défi épique pour couronner le meilleur joueur d'échecs.",
            "Une compétition féroce avec des prix prestigieux à gagner.",
            "Un tournoi d'échecs où l'intelligence et la stratégie priment.",
            "Une rencontre d'échecs avec des parties captivantes et intenses.",
            "Un événement majeur dans le monde des échecs, attirant des talents de tous horizons.",
        ]
        description = random.choice(descriptions)
        while description in self.used_descriptions:
            description = random.choice(descriptions)
        self.used_descriptions.add(description)
        return description


fake.add_provider(ChessTournamentProvider(fake))


def generate_initial_tournaments(num_tournaments):
    tournaments = []
    for _ in range(num_tournaments):
        name = fake.chess_tournament_name()
        location = fake.city()
        start_date = fake.date_between(start_date="-1y", end_date="today")
        end_date = start_date + timedelta(days=random.randint(1, 7))
        description = fake.chess_tournament_description()
        rounds_count = random.randint(4, 7)  # Le nombre de rounds est au minimum 4 et peut aller jusqu'à 7
        tournament = {
            "name": name,
            "location": location,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "description": description,
            "rounds_count": rounds_count,
            "current_round": 0,
            "rounds": [],
            "players": [],
        }
        tournaments.append(tournament)
    return tournaments


def save_tournaments_to_json(tournaments, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Lire les tournois existants avec pandas
    if os.path.exists(filename):
        existing_tournaments = pd.read_json(filename)
    else:
        existing_tournaments = pd.DataFrame()

    # Convertir les nouveaux tournois en DataFrame
    new_tournaments = pd.DataFrame(tournaments)

    # Ajouter les nouveaux tournois aux tournois existants
    updated_tournaments = pd.concat([existing_tournaments, new_tournaments], ignore_index=True)

    # Sauvegarder les tournois mis à jour
    updated_tournaments.to_json(filename, orient="records", indent=2, force_ascii=False)


def display_tournaments_table(tournaments):
    console = Console()
    table = Table(title="Tournois ajoutés", box=box.SQUARE, show_lines=True)
    table.add_column("Nom", header_style="bold cyan")
    table.add_column("Lieu", header_style="bold cyan")
    table.add_column("Date de début", header_style="bold cyan")
    table.add_column("Date de fin", header_style="bold cyan")
    table.add_column("Description", header_style="bold cyan")
    table.add_column("Rounds", header_style="bold cyan")

    for tournament in tournaments:
        table.add_row(
            tournament["name"],
            tournament["location"],
            tournament["start_date"],
            tournament["end_date"],
            (
                (tournament["description"][:30] + "...")
                if len(tournament["description"]) > 30
                else tournament["description"]
            ),
            str(tournament["rounds_count"]),
        )

    console.print(table)


if __name__ == "__main__":
    num_tournaments = 10
    tournaments = generate_initial_tournaments(num_tournaments)
    save_tournaments_to_json(tournaments, "datas/tournaments.json")
    display_tournaments_table(tournaments)
    print(f"{num_tournaments} tournois fictifs générés et sauvegardés dans 'datas/tournaments.json'.")
