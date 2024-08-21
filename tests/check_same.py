# méthode maison pour vérifier si des joueurs ont joué l'un contre l'autre + 1 fois
# Simplment ocller un tounoit et lancer le script

tournament = {
        "name": "Démo OC",
        "location": "Paris",
        "start_date": "1111-11-11",
        "end_date": "1111-11-11",
        "description": "Démooo",
        "rounds_count": 4,
        "current_round": 4,
        "rounds": [
            {
                "name": "Round 1",
                "matches": [
                    {
                        "player1": {
                            "id": "FV8949",
                            "score_match": 0.5
                        },
                        "player2": {
                            "id": "DC0302",
                            "score_match": 0.5
                        }
                    },
                    {
                        "player1": {
                            "id": "ZE3846",
                            "score_match": 0.5
                        },
                        "player2": {
                            "id": "VQ9711",
                            "score_match": 0.5
                        }
                    }
                ],
                "start_time": "01-08-2024-09-13",
                "end_time": "01-08-2024-09-16"
            },
            {
                "name": "Round 2",
                "matches": [
                    {
                        "player1": {
                            "id": "FV8949",
                            "score_match": 0.5
                        },
                        "player2": {
                            "id": "ZE3846",
                            "score_match": 0.5
                        }
                    },
                    {
                        "player1": {
                            "id": "ZE3846",
                            "score_match": 0.5
                        },
                        "player2": {
                            "id": "ET5927",
                            "score_match": 0.5
                        }
                    }
                ],
                "start_time": "01-08-2024-09-16",
                "end_time": "01-08-2024-09-16"
            },
            {
                "name": "Round 3",
                "matches": [
                    {
                        "player1": {
                            "id": "ZE3846",
                            "score_match": 0.5
                        },
                        "player2": {
                            "id": "DC0302",
                            "score_match": 0.5
                        }
                    },
                    {
                        "player1": {
                            "id": "DC0302",
                            "score_match": 0.5
                        },
                        "player2": {
                            "id": "VQ9711",
                            "score_match": 0.5
                        }
                    }
                ],
                "start_time": "01-08-2024-09-16",
                "end_time": "01-08-2024-09-16"
            },
            {
                "name": "Round 4",
                "matches": [
                    {
                        "player1": {
                            "id": "FV8949",
                            "score_match": 0.5
                        },
                        "player2": {
                            "id": "VQ9711",
                            "score_match": 0.5
                        }
                    }
                ],
                "start_time": "01-08-2024-09-16",
                "end_time": "01-08-2024-09-17"
            }
        ],
        "players": [
            {
                "national_id": "ZE3846",
                "career_score": 2.0
            },
            {
                "national_id": "DC0302",
                "career_score": 1.5
            },
            {
                "national_id": "FV8949",
                "career_score": 1.5
            },
            {
                "national_id": "VQ9711",
                "career_score": 1.5
            },
            {
                "national_id": "ET5927",
                "career_score": 0.5
            }
        ]
    }

# Vérification si des joueurs ont joué l'un contre l'autre plus d'une fois
# D'abord on initialise un dictionnaire vide pour stocker l'historique des matchs entre les joueurs
match_history = {}

# On boucle sur chaque round du tournoi
for round in tournament["rounds"]:
    # On boucle sur chaque match du round
    for match in round["matches"]:
        # On récupère les identifiants des deux joueurs du match
        p1 = match["player1"]["id"]
        p2 = match["player2"]["id"]
        # Si les paires de joueurs sont toujours dans le même ordre, on les inverse
        if p1 > p2:
            p1, p2 = p2, p1
        # Si les paires de joueurs sont déjà dans le dictionnaire match_history, on les incrémente
        if (p1, p2) in match_history:
            match_history[(p1, p2)] += 1
        # Sinon, on les ajoute avec une valeur de 1
        else:
            match_history[(p1, p2)] = 1

# On filtre les paires de joueurs qui ont été jouées plus d'une fois ensemble
repeated_matches = {match: count for match, count in match_history.items() if count > 1}

# On vérifie si ya des matchs répétés
if repeated_matches:
    print("Les joueurs suivants ont joué l'un contre l'autre plus d'une fois :")
    # on affiche le nombre de fois où chaque paire de joueurs a été jouée ensemble
    for match, count in repeated_matches.items():
        print(f"Joueurs {match[0]} et {match[1]}: {count} fois")
else:
    # Si zero matchs répétés, on l'affiche :
    print("Aucun joueur n'a joué contre un autre plus d'une fois.")
