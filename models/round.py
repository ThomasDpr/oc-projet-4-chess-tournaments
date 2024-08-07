from models.match import Match
from utils.utils import get_timestamp


class Round:
    def __init__(self, name: str):
        """
        Initialise un nouveau round avec un nom et des valeurs par défaut.

        Args:
            name (str): Le nom du round.
        """
        self.name = name  # Nom du round
        self.matches = []  # Liste des matchs du round
        self.start_time = get_timestamp()  # Heure de début du round
        self.end_time = None  # Heure de fin du round (initialisé à None car pas encore terminé)

    def add_match(self, match):
        """
        Ajoute un match à la liste des matchs du round.

        Args:
            match (Match): Le match à ajouter.
        """
        # La méthode append() ici me permet d’ajouter un nouveau match à la fin de la liste des matchs
        self.matches.append(match)

    def close_round(self):
        """
        Marque le round comme terminé en enregistrant le timestamp de fin.
        """
        self.end_time = get_timestamp()

    def to_dict(self):
        """
        Convertit l'objet Round en dictionnaire.

        Returns:
            dict: Dictionnaire contenant les informations du round.
        """
        return {
            "name": self.name,
            "matches": [match.to_dict() for match in self.matches],  # Voir à la fin du fichier pour plus de détails
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crée un objet Round à partir d'un dictionnaire.

        Args:
            data (dict): Dictionnaire contenant les informations du round.

        Returns:
            Round: Un nouvel objet Round.

        Raises:
            TypeError: Si les données fournies ne sont pas un dictionnaire.
        """
        if isinstance(data, dict):
            # On initialise le round avec les infos du dict et ici le nom du round
            round_ = cls(data["name"])
            # On convertit les données de matchs en objets Match pour chaque match
            round_.matches = [Match.from_dict(match_data) for match_data in data.get("matches", [])]
            round_.start_time = data.get("start_time")
            round_.end_time = data.get("end_time")
            return round_
        # Si mes datas ne sont pas un dictionnaire, je renvoie une erreur
        else:
            raise TypeError("Les données fournies ne sont pas un dictionnaire")


# Aide-mémoire pour mon apprentissage Python :

"""
Exemple output pour "matches" :

    "matches": [
        {
            "player1": {
                "id": "JK3333",
                "score_match": 3.0
            },
            "player2": {
                "id": "BN2222",
                "score_match": 3.0
            }
        },
        {
            "player1": {
                "id": "BN9999",
                "score_match": 2.0
            },
            "player2": {
                "id": "BN0000",
                "score_match": 2.0
            }
        }
    ]

"""
