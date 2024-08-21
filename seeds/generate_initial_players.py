import json
import os

from faker import Faker

fake = Faker()


def generate_initial_players():
    players = []
    for _ in range(num_players):
        first_name = fake.first_name()
        last_name = fake.last_name()
        birth_date = fake.date_of_birth(minimum_age=10, maximum_age=90).strftime("%d-%m-%Y")
        national_id = fake.bothify(text="??####", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        player = {
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "national_id": national_id,
            "career_score": 0,  # Score par défaut à 0 pour chaque joueur
        }
        players.append(player)
    return players


def save_players_to_json(players, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(players, f, indent=4)


if __name__ == "__main__":
    num_players = 100
    players = generate_initial_players()
    save_players_to_json(players, "datas/players.json")
    print(f"{num_players} joueurs fictifs générés et sauvegardés dans 'datas/players.json'.")
