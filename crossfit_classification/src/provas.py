# provas.py

from typing import List

def obter_provas() -> List[str]:
    """Retorna a lista de provas disponíveis."""
    return [
        "1a", "1b", "1c", "1d",
        "2a", "2b",
        "3a Snatch", "3b Clean & Jerk",  # Provas onde maior pontuação é melhor
        "4a", "4b", "4c", "4d"
    ]
