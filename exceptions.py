# Ces exceptions personnalisées permettent de gérer plus éfficacement et spécifiquement les erreurs liés :
# - aux joueurs
# - aux formats des données
# Elles fournissent des messages d'erreur plus clairs et plus précis afin de faciliter le parcours de l'utilisateur.

# Source d'inspiration (vidéo youtube): https://www.youtube.com/watch?v=U8f4ugPvfbg


class PlayerExistsError(ValueError):
    """
    Exception levée lorsqu'un joueur avec le même identifiant national existe déjà.

    Attributs:
        national_id (str): L'identifiant national du joueur existant.
    """

    def __init__(self, national_id):
        self.national_id = national_id

    def __str__(self):
        return f"Un joueur avec l'identifiant national [bold blue]{self.national_id}[/bold blue] existe déjà.\n"


class InvalidNationalIdError(ValueError):
    """
    Exception levée lorsque l'identifiant national d'un joueur est invalide.

    Attributs:
        national_id (str): L'identifiant national invalide.
    """

    def __init__(self, national_id):
        self.national_id = national_id

    def __str__(self):
        return f"Le format de l'Identifiant national [bold blue]{self.national_id}[/bold blue] est [bold red]invalide.[/bold red] Il doit être au format 'AB1234'.\n"  # noqa: E501


class InvalidDateFormatError(ValueError):
    """
    Exception levée lorsque le format de la date est invalide.

    Attributs:
        date_str (str): La chaîne de caractères de la date invalide.
    """

    def __init__(self, date_str):
        self.date_str = date_str

    def __str__(self):
        return f"Le format de la date [bold blue]{self.date_str}[/bold blue] est [bold red]invalide.[/bold red] Utilisez le format 'JJ-MM-AAAA' , 'JJ/MM/AAAA' ou 'JJMMAAAA'.\n"  # noqa: E501


class DataLoadingError(Exception):
    """
    Exception levée lorsque le chargement des données échoue.

    Attributs:
        file_path (str): Le chemin vers le fichier qui a causé l'erreur.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def __str__(self):
        return f"Erreur lors du chargement des données depuis le fichier : {self.file_path}"


class DataSavingError(Exception):
    """
    Exception levée lorsque la sauvegarde des données échoue.

    Attributs:
        file_path (str): Le chemin vers le fichier qui a causé l'erreur.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def __str__(self):
        return f"Erreur lors de l'enregistrement des données dans le fichier : {self.file_path}"
