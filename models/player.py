from datetime import datetime
from typing import Dict

from exceptions import InvalidDateFormatError, InvalidNationalIdError
from utils.utils import capitalize_name, normalize_national_id, parse_birth_date


class Player:
    def __init__(self, first_name: str, last_name: str, birth_date: str, national_id: str, career_score: int = 0):
        """
        Initialise un nouveau joueur avec les informations fournies.

        Args:
            first_name (str): Prénom du joueur.
            last_name (str): Nom de famille du joueur.
            birth_date (str): Date de naissance du joueur au format 'JJ-MM-AAAA' ou 'JJ/MM/AAAA'.
            national_id (str): Identifiant national du joueur.
            career_score (int): Score de carrière du joueur (par défaut 0).
        """
        self.first_name: str = capitalize_name(first_name)
        self.last_name: str = capitalize_name(last_name)

        try:
            self.birth_date: datetime = parse_birth_date(birth_date)
        except ValueError:
            raise InvalidDateFormatError(birth_date)

        try:
            self.national_id: str = normalize_national_id(national_id)
        except ValueError:
            raise InvalidNationalIdError(national_id)

        self.career_score: int = career_score

    def to_dict(self) -> Dict[str, str]:
        """
        Convertit l'objet Player en dictionnaire.

        Returns:
            Dict[str, str]: Dictionnaire contenant les informations du joueur.
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date.strftime("%d-%m-%Y"),
            "national_id": self.national_id,
            "career_score": str(self.career_score),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Player":
        """
        Crée un objet Player à partir d'un dictionnaire.

        Args:
            data (Dict[str, str]): Dictionnaire contenant les informations du joueur.

        Returns:
            Player: Un nouvel objet Player.
        """
        return cls(
            data["first_name"],
            data["last_name"],
            data["birth_date"],
            data["national_id"],
            int(data.get("career_score", 0)),
        )

    @classmethod
    def from_tournament_dict(cls, data: Dict[str, str]) -> "Player":
        """
        Crée un objet Player à partir d'un dictionnaire.

        Args:
            data (Dict[str, str]): Dictionnaire contenant les informations du joueur.

        Returns:
            Player: Un nouvel objet Player.
        """
        return cls(
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            birth_date=data.get("birth_date", "01-01-1900"),
            national_id=data["national_id"],
            career_score=data.get("career_score", 0),
        )

    def __repr__(self) -> str:
        """
        Retourne la représentation en chaîne de caractères de l'objet Player.

        Returns:
            str: Représentation du joueur.
        """
        return f"{self.first_name} {self.last_name} ({self.national_id}), Score de carrière: {self.career_score}"
