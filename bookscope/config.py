##################### Configuration de BookScope

from pathlib import Path

# Connexion MongoDB (serveur local)
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "bookscope"

# Dossier contenant les CSV Goodbooks-10k
DATA_DIR = Path(__file__).resolve().parent.parent / "goodbooks-10k-1.0"

# Règle de sélection : on ne garde que les ratings des lecteurs avec user_id < MAX_USER_ID
MAX_USER_ID = 100_000

# F1 : nombre minimum de tags en commun pour considérer deux livres comme similaires
MIN_SHARED_TAGS = 10
