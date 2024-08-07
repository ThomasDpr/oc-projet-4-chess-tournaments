from InquirerPy import get_style
from rich.console import Console


class BaseView:
    def __init__(self):
        self.console = Console()
        self.custom_style = get_style(
            {
                "questionmark": "#e5c07b",      # Point d'interrogation avant la question
                "answermark": "#e5c07b",        # Symbole avant la réponse après que la question soit répondue
                "answer": "#61afef",            # La réponse donnée par l'utilisateur
                "input": "#98c379",             # Texte de l'entrée de l'utilisateur pendant qu'il tape
                "question": "#61afef bold",     # Style de la question posée
                "answered_question": "",        # Style de la question après qu'elle ait été répondue
                "instruction": "#abb2bf",       # Instructions courtes affichées à côté de la question
                "long_instruction": "#abb2bf",  # Instructions longues affichées en bas du prompt
                "pointer": "#61afef",           # Pointeur qui indique la sélection actuelle
                "checkbox": "#98c379",          # La case à cocher pour les sélections multiples
                "separator": "",                # Séparateurs entre les options
                "skipped": "#5c6370",           # Texte pour les questions sautées
                "validator": "",                # Messages de validation
                "marker": "#e5c07b",            # Marqueur utilisé pour les éléments sélectionnés
                "fuzzy_prompt": "#c678dd",      # Texte du prompt pendant la recherche floue
                "fuzzy_info": "#abb2bf",        # Informations affichées pendant la recherche floue
                "fuzzy_border": "#4b5263",      # La bordure pendant la recherche floue
                "fuzzy_match": "#c678dd",       # Couleur des correspondances trouvées pendant la recherche floue
                "spinner_pattern": "#e5c07b",   # Motif de spinner pendant le chargement
                "spinner_text": "",             # Texte du spinner pendant le chargement
            }
        )
