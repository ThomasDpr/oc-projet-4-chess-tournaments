import datetime

from models.player import Player
from models.round import Round


class Tournament:
    def __init__(
        self, name: str, location: str, start_date: str, end_date: str, description: str, rounds_count: int = 4
    ):
        """
        Initialise un nouveau tournoi avec les informations fournies.

        Args:
            name (str): Nom du tournoi.
            location (str): Lieu du tournoi.
            start_date (str): Date de début du tournoi au format 'YYYY-MM-DD'.
            end_date (str): Date de fin du tournoi au format 'YYYY-MM-DD'.
            description (str): Description du tournoi.
            rounds_count (int): Nombre total de rounds du tournoi (par défaut 4).
        """

        # On initialise les attributs de la classe
        self.name = name
        self.location = location
        self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        self.description = description
        self.rounds_count = rounds_count
        self.current_round = 0  # Round actuel du tournoi (initialisé à 0)
        self.rounds = []  # Liste des rounds du tournoi
        self.players = []  # Liste des joueurs du tournoi

    def to_dict(self):
        """
        Convertit l'objet Tournament en un dictionnaire.

        Returns:
            dict: Dictionnaire contenant les informations du tournoi.
        """
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "end_date": self.end_date.strftime("%Y-%m-%d"),
            "description": self.description,
            "rounds_count": self.rounds_count,
            "current_round": self.current_round,
            # On convertit les rounds en un dictionnaire
            "rounds": [round_.to_dict() for round_ in self.rounds],  # Voir à la fin du fichier pour plus de détails
            "players": [
                {"national_id": player.national_id, "career_score": player.career_score} for player in self.players
            ],  # Voir à la fin du fichier pour plus de détails
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crée un objet Tournament à partir d'un dictionnaire.

        Args:
            data (dict): Dictionnaire contenant les informations du tournoi.

        Returns:
            Tournament: Un nouvel objet Tournament.
        """
        tournament = cls(
            data["name"],
            data["location"],
            data["start_date"],
            data["end_date"],
            data["description"],
            data["rounds_count"],
        )

        # On initialise la variable current_round avec la valeur du dictionnaire donc : 0
        tournament.current_round = data["current_round"]

        # On convertit les données de rounds en objets Round (voir le model Round.py)
        tournament.rounds = [Round.from_dict(round_data) for round_data in data["rounds"]]

        # On convertit les données de joueurs en objets Player à partir de l'ID national (voir le model Player.py)
        tournament.players = [Player.from_tournament_dict(player_data) for player_data in data["players"]]

        return tournament

    def add_player(self, player):
        """
        Ajoute un joueur au tournoi.

        Args:
            player (Player): Le joueur à ajouter.
        """
        # La méthode append() ici me permet d’ajouter un nouveau joueur à la fin de la liste des joueurs
        self.players.append(player)

    def add_round(self, round_):
        """
        Ajoute un round au tournoi.

        Args:
            round_ (Round): Le round à ajouter.
        """
        # La méthode append() ici me permet d’ajouter un nouveau round à la fin de la liste des rounds
        self.rounds.append(round_)

    def generate_pairs(self):
        """
        Génère les paires de joueurs pour les matchs en fonction des scores de carrière.

        Returns:
            list: Liste des paires de joueurs.
        """
        # On trie les joueurs par score de carrière (en ordre décroissant)
        self.players.sort(key=lambda p: p.career_score, reverse=True)
        # On initialise une liste vide pour stocker les paires de joueurs
        pairs = []
        # On initialise un ensemble pour suivre les joueurs déjà utilisés dans les paires
        used_players = set()

        # On boucle sur les joueurs en avançant de 2 en 2 à chaque itération,
        # jusqu'à ce qu'il n'y ait plus de joueurs restants à ajouter
        # i est le numéro de l'itération courante
        for i in range(0, len(self.players), 2):
            # Si l'itération courante est inférieure ou égale à la taille des joueurs,
            # cela signifie qu'il reste des joueurs à ajouter
            if i + 1 < len(self.players):
                # On récupère les deux joueurs à ajouter
                player1 = self.players[i]
                player2 = self.players[i + 1]
                # On vérifie si les deux joueurs n'ont pas déjà joué l'un contre l'autre
                if not self.has_played_against_each_other(player1, player2):
                    # Si ce n'est pas le cas, on ajoute les paires à la liste des paires
                    pairs.append((player1, player2))
                    # On ajoute aussi les joueurs à l'ensemble des joueurs déjà utilisés pour ne pas les ajouter 2 fois
                    used_players.add(player1.national_id)
                    used_players.add(player2.national_id)
                else:
                    # Si les 2 joueurs ont déjà joué l'un contre l'autre, chercher un autre joueur pour former 1 paire
                    for j in range(i + 2, len(self.players)):
                        # On récupère un joueur possible pour tenter de former un paire
                        potential_player2 = self.players[j]
                        # Vérifier si le joueur potentiel n'a pas déjà été utilisé + n'a pas joué contre le 1er joueur
                        if (
                            potential_player2.national_id not in used_players
                            and not self.has_played_against_each_other(player1, potential_player2)
                        ):
                            # Si tout est bon, on ajoute la paire à la liste des paires
                            pairs.append((player1, potential_player2))
                            # On ajoute les joueurs à l'ensemble des joueurs déjà utilisés.
                            used_players.add(player1.national_id)
                            used_players.add(potential_player2.national_id)
                            # On sort de la boucle pour passer au prochain joueur
                            break
        # Voilà notre liste des paires de joueurs prête pour le match
        return pairs

    def has_played_against_each_other(self, player1, player2):
        """
        Vérifie si deux joueurs ont déjà joué l'un contre l'autre.

        Args:
            player1 (Player): Le premier joueur.
            player2 (Player): Le deuxième joueur.

        Returns:
            bool: True s'ils ont déjà joué l'un contre l'autre, sinon False.
        """
        # Pour chaque round dans la liste des rounds du tournoi
        for round_ in self.rounds:
            # Pour chaque match de chaque round
            for match in round_.matches:
                # On vérifie si le match a été joué entre player1 et player2
                if (match.player1_id == player1.national_id and match.player2_id == player2.national_id) or (
                    match.player1_id == player2.national_id and match.player2_id == player1.national_id
                ):
                    # Si c'est le cas, on renvoie True
                    return True
        # Si aucun match trouvé entre player1 et player2, je renvoie False
        return False

    def minimum_players_required(self):
        """
        Retourne le nombre minimum de joueurs requis pour le tournoi.

        Returns:
            int: Le nombre minimum de joueurs requis.
        """

        return self.rounds_count + 1

    def is_valid_player_count_for_rounds(self):
        """
        Vérifie si le nombre de joueurs est suffisant pour le nombre de rounds.

        Returns:
            bool: True si le nombre de joueurs est suffisant, sinon False.
        """

        return len(self.players) >= self.minimum_players_required()

    def __repr__(self):
        """
        Retourne la représentation en chaîne de caractères de l'objet Tournament.

        Returns:
            str: Représentation du tournoi.
        """

        return (
            f"Tournament({self.name}, {self.location}, "
            f"{self.start_date.strftime('%Y-%m-%d')} - {self.end_date.strftime('%Y-%m-%d')}, "
            f"Rounds: {self.rounds_count})"
        )


# Aide-mémoire pour mon apprentissage Python :

"""
Exemple output pour "rounds" :

    "rounds": [
        {
            "name": "Round 1",
            "matches": [],
            "start_time": "2024-07-25-09-14",
            "end_time": "2024-07-25-09-15"
        }
    ]

"""

"""
Exemple output pour "players" :

    "players": [
        {
            "national_id": "JK3333",
            "career_score": 3.0
        },
        {
            "national_id": "BN2222",
            "career_score": 3.0
        },
        {
            "national_id": "BN9999",
            "career_score": 2.0
        },
        {
            "national_id": "BN0000",
            "career_score": 2.0
        }
    ]
"""
