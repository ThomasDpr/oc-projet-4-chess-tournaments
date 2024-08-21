import os
import re
from datetime import datetime

from unidecode import unidecode

from exceptions import InvalidDateFormatError, InvalidNationalIdError


def capitalize_name(name: str) -> str:
    """
    Capitalise chaque mot dans une chaîne de caractères.

    Args:
        name (str): La chaîne de caractères à capitaliser.

    Returns:
        str: La chaîne de caractères avec chaque mot capitalisé.

    Exemple:
        >>> capitalize_name("jean pierre")
        'Jean Pierre'
        >>> capitalize_name("dupont")
        'Dupont'
    """
    return " ".join(word.capitalize() for word in name.split())


def normalize_national_id(national_id: str) -> str:
    """
    Normalise un identifiant national en supprimant les caractères non alphanumériques
    et en vérifiant le format.

    Args:
        national_id (str): L'identifiant national à normaliser.

    Returns:
        str: L'identifiant national normalisé.

    Raises:
        ValueError: Si l'identifiant national ne respecte pas le format 'AB1234'.
    """
    national_id = re.sub(r"[^A-Za-z0-9]", "", national_id).upper()
    if re.match(r"^[A-Z]{2}\d{4}$", national_id):
        return national_id
    else:
        raise InvalidNationalIdError(national_id)


def validate_date_format(date_str: str) -> bool:
    """
    Valide le format de la date en 'JJ-MM-AAAA' , 'JJ/MM/AAAA' ou 'JJMMAAAA'.

    Args:
        date_str (str): La chaîne de caractères de la date à valider.

    Returns:
        bool: True si la date est valide, False sinon.
    """
    return bool(
        re.match(r"^\d{2}-\d{2}-\d{4}$", date_str)
        or re.match(r"^\d{2}/\d{2}/\d{4}$", date_str)
        or re.match(r"^\d{8}$", date_str)
    )


def parse_birth_date(date_str: str) -> datetime:
    """
    Convertit une date de naissance en objet datetime.

    Args:
        date_str (str): Date de naissance au format 'JJ-MM-AAAA', 'JJ/MM/AAAA' ou 'JJMMAAAA'.

    Returns:
        datetime: Objet datetime représentant la date de naissance.

    Raises:
        InvalidDateFormatError: Si le format de la date est incorrect.
    """
    try:
        if re.match(r"^\d{2}-\d{2}-\d{4}$", date_str):
            return datetime.strptime(date_str, "%d-%m-%Y")
        elif re.match(r"^\d{2}/\d{2}/\d{4}$", date_str):
            return datetime.strptime(date_str, "%d/%m/%Y")
        elif re.match(r"^\d{8}$", date_str):
            return datetime.strptime(date_str, "%d%m%Y")
        else:
            raise InvalidDateFormatError(date_str)
    except ValueError:
        raise InvalidDateFormatError(date_str)


def sanitize(text):
    text = unidecode(text)  # Convertir les caractères Unicode en ASCII
    text = text.lower().replace(" ", "_")  # Remplacer les espaces par des underscores et convertir en minuscule
    text = re.sub(r"[^\w\s]", "", text)  # Supprimer les caractères non alphanumériques
    return text.replace("'", "")  # Supprimer les apostrophes


def clear_console():
    """
    Efface la console.
    """
    os.system("cls" if os.name == "nt" else "clear")


def get_username():
    system = os.name
    # Si le système est POSIX (Linux ou macOS)
    if system == "posix":
        # On récupère le nom d'utilisateur courant à partir des variables d'environnement (LOGNAME ou USER)
        username = os.environ.get("LOGNAME") or os.environ.get("USER")
    # Si le système est NT (Windows)
    elif system == "nt":
        # On récupère le nom d'utilisateur courant à partir de la variable d'environnement (USERNAME)
        username = os.environ.get("USERNAME")
    # Si le système n'est pas reconnu
    else:
        # On renvoie None
        username = None
    return username


def get_timestamp():
    # On utilise la fonction datetime.now() pour obtenir la date et l'heure actuelles
    # On utilise la méthode strftime() pour formater la date et l'heure en "JJ-MM-AAAA-HH-MM-SS"
    # On supprime la dernière partie ("SS") pour obtenir la chaîne de caractères de la forme "JJ-MM-AAAA-HH-MM"
    # Verifier traitement x2
    return datetime.now().strftime("%d-%m-%Y-%H-%M-%S")[:-3]
