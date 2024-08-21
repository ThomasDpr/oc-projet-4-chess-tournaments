import os

import pandas as pd

from exceptions import DataLoadingError, DataSavingError


class DataManager:
    """
    Gestionnaire de données de base pour charger, sauvegarder et manipuler les données stockées dans des fichiers JSON.

    Attributs:
        file_path (str): Chemin vers le fichier JSON contenant les données.
        columns (list): Liste des colonnes de la structure des données.
        data_df (pd.DataFrame): DataFrame contenant les données chargées depuis le fichier JSON.
    """

    def __init__(self, file_path, columns):
        self.file_path = file_path
        self.columns = columns
        self.data_df = self.load_data()

    def load_data(self):
        """
        Charge les données depuis le JSON. S'il n'existe pas, il est créé avec les colonnes spécifiées.

        Returns:
            pd.DataFrame: DataFrame contenant les données chargées.

        Raises:
            DataLoadingError: Si le fichier JSON ne peut pas être chargé.
        """
        # Si le fichier n'existe pas, créer un DataFrame vide avec les colonnes spécifiées
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            pd.DataFrame(columns=self.columns).to_json(self.file_path, orient="records", indent=4, force_ascii=False)
        # On tente de charger les données depuis le fichier JSON
        try:

            data = pd.read_json(self.file_path)

            if data.empty:
                data = pd.DataFrame(columns=self.columns)
            elif not all(col in data.columns for col in self.columns):
                # Si les colonnes du DataFrame ne correspondent pas aux colonnes attendues, on les réinitialise
                data = pd.DataFrame(columns=self.columns)
            return data
        # Sinon, on génère une exception DataLoadingError
        except ValueError:
            raise DataLoadingError(self.file_path)

    def save_data(self):
        """
        Sauvegarde les données dans le fichier JSON.

        Raises:
            DataSavingError: Si les données ne peuvent pas être sauvegardées.
        """
        try:
            self.data_df.to_json(self.file_path, orient="records", indent=4, force_ascii=False)
        except ValueError:
            raise DataSavingError(self.file_path)

    def get_data(self):
        """
        Retourne les données actuellement chargées.

        Returns:
            pd.DataFrame: DataFrame contenant les données.
        """
        return self.data_df

    def set_data(self, data_df):
        """
        Met à jour les données et les sauvegarde dans le fichier JSON.

        Args:
            data_df (pd.DataFrame): DataFrame contenant les nouvelles données.
        """
        self.data_df = data_df
        self.save_data()


class PlayerDataManager(DataManager):
    """
    Gestionnaire de données spécifique pour les joueurs.

    Args:
        file_path (str): Chemin vers le fichier JSON des joueurs. Par défaut "datas/players.json".
    """

    def __init__(self, file_path="datas/players.json"):
        columns = ["first_name", "last_name", "birth_date", "national_id", "career_score"]
        super().__init__(file_path, columns)


class TournamentDataManager(DataManager):
    """
    Gestionnaire de données spécifique pour les tournois.

    Args:
        file_path (str): Chemin vers le fichier JSON des tournois. Par défaut "datas/tournaments.json".
    """

    def __init__(self, file_path="datas/tournaments.json"):
        columns = [
            "name",
            "location",
            "start_date",
            "end_date",
            "description",
            "rounds_count",
            "current_round",
            "rounds",
            "players",
        ]
        super().__init__(file_path, columns)
