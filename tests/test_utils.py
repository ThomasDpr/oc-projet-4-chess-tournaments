import os
from datetime import datetime

import pytest

from exceptions import InvalidDateFormatError, InvalidNationalIdError
from utils.utils import (
    capitalize_name,
    get_timestamp,
    get_username,
    normalize_national_id,
    parse_birth_date,
    sanitize,
    validate_date_format,
)


# Test de la fonction capitalize_name
def test_capitalize_name():
    # Vérifie que chaque mot d'une string est mis en capitale
    assert capitalize_name("jean michel") == "Jean Michel"
    assert capitalize_name("dupont") == "Dupont"
    assert capitalize_name("thomas dupré") == "Thomas Dupré"


# Test de la fonction normalize_national_id
def test_normalize_national_id():
    # Vérifie que l'Identifiant National est correctement normalisé
    assert normalize_national_id("ab 1234") == "AB1234"
    assert normalize_national_id("A B1234") == "AB1234"
    assert normalize_national_id("ab1234") == "AB1234"
    assert normalize_national_id("AB1234") == "AB1234"
    assert normalize_national_id("ab-1234") == "AB1234"
    assert normalize_national_id("AB-1234") == "AB1234"
    # Vérifie que la fonction lève une exception (InvalidNationalIdError) si l'Identifiant National est incorrect
    with pytest.raises(InvalidNationalIdError):
        # Si l'Identifiant National contient des caractères non alphanumériques
        normalize_national_id("invalid_id")
    with pytest.raises(InvalidNationalIdError):
        # Si l'Identifiant National ne respecte pas le format 'AB1234'
        normalize_national_id("1234AB")


# Test de la fonction validate_date_format
def test_validate_date_format():
    # Vérifie que le format de la date est correctement validé
    assert validate_date_format("01-01-2020") is True
    assert validate_date_format("01/01/2020") is True
    assert validate_date_format("01012020") is True
    assert validate_date_format("2020-01-01") is False
    assert validate_date_format("01-01-20") is False
    assert validate_date_format("010120") is False


# Test de la fonction parse_birth_date
def test_parse_birth_date():
    # Vérifie que la fonction convertit correctement une date de naissance en objet datetime
    assert parse_birth_date("01-01-2020") == datetime(2020, 1, 1)
    assert parse_birth_date("01/01/2020") == datetime(2020, 1, 1)
    assert parse_birth_date("01012020") == datetime(2020, 1, 1)
    # Vérifie que la fonction lève une exception (InvalidDateFormatError) si la date de naissance est incorrecte
    with pytest.raises(InvalidDateFormatError):
        parse_birth_date("2020-01-01")
    with pytest.raises(InvalidDateFormatError):
        parse_birth_date("01-01-20")
    with pytest.raises(InvalidDateFormatError):
        parse_birth_date("010120")
    with pytest.raises(InvalidDateFormatError):
        parse_birth_date("invalid_date")


# Test de la fonction sanitize
def test_sanitize():
    # Vérifie que la chaîne de caractères est correctement nettoyée et normalisée
    assert sanitize("Jean-Pierre") == "jeanpierre"
    assert sanitize("Café du coin") == "cafe_du_coin"
    assert sanitize("L'été est chaud!") == "lete_est_chaud"
    assert sanitize("Espaces multiples") == "espaces_multiples"


# Test de la fonction get_username
def test_get_username():
    # Vérifie que la fonction renvoie le nom d'utilisateur courant
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
    assert get_username() == username


# Test de la fonction get_timestamp
def test_get_timestamp():
    # Vérifie que la fonction renvoie une chaîne de caractères de la forme "JJ-MM-AAAA-HH-MM-SS"
    # On utilise la fonction datetime.now() pour obtenir la date et l'heure actuelles
    # On utilise la méthode strftime() pour formater la date et l'heure en "JJ-MM-AAAA-HH-MM-SS"
    # On supprime la dernière partie ("SS") pour obtenir la chaîne de caractères de la forme "JJ-MM-AAAA-HH-MM"
    assert get_timestamp() == datetime.now().strftime("%d-%m-%Y-%H-%M-%S")[:-3]
