class Match:
    def __init__(self, player1_id, player2_id):
        """
        Initialise un nouveau match entre deux joueurs.

        Args:
            player1_id (str): L'identifiant du premier joueur.
            player2_id (str): L'identifiant du deuxième joueur.
        """
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.score_player1 = 0  # Initialisation du score du premier joueur à 0
        self.score_player2 = 0  # Initialisation du score du deuxième joueur à 0

    def set_scores(self, score1, score2):
        """
        Définit les scores des joueurs pour ce match.

        Args:
            score1 (float): Le score du premier joueur.
            score2 (float): Le score du deuxième joueur.
        """
        self.score_player1 = score1
        self.score_player2 = score2

    def to_dict(self):
        """
        Convertit l'objet Match en dictionnaire.

        Returns:
            dict: Dictionnaire contenant les informations du match.
        """
        return {
            "player1": {"id": self.player1_id, "score_match": self.score_player1},
            "player2": {"id": self.player2_id, "score_match": self.score_player2},
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crée un objet Match à partir d'un dictionnaire.

        Args:
            data (dict): Dictionnaire contenant les informations du match.

        Returns:
            Match: Un nouvel objet Match.
        """

        match = cls(data["player1"]["id"], data["player2"]["id"])
        match.set_scores(data["player1"]["score_match"], data["player2"]["score_match"])
        return match

    def __repr__(self):
        """
        Retourne la représentation en chaîne de caractères de l'objet Match.

        Returns:
            str: Représentation du match.
        """

        return f"Match entre {self.player1_id} et {self.player2_id}, Scores: {self.score_player1}-{self.score_player2}"
