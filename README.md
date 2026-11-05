# BookScope
- ANDRÉ Mathis
- VIALE Jean-Jacques

## Créer la base de données

### Prérequis
- Python 3
- Un serveur MongoDB lancé en local sur `mongodb://localhost:27017`
- Les CSV Goodbooks-10k dans le dossier `goodbooks-10k-1.0/` à la racine du projet

### Installation (une seule fois)
Depuis la racine du projet :
```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt     # Windows
# .venv/bin/python -m pip install -r requirements.txt       # Linux / macOS
```

### Chargement
```bash
cd bookscope
../.venv/Scripts/python load_db.py
```
Le script supprime la base `bookscope` si elle existe, puis la recrée avec une collection par CSV : `books`, `tags`, `book_tags`, `ratings` et `to_read`. Le chargement complet prend environ 7 à 8 minutes.

Les paramètres se trouvent dans [bookscope/config.py](bookscope/config.py) :
- `MONGO_URI` et `DB_NAME` : connexion à MongoDB ;
- `DATA_DIR` : dossier des CSV ;
- `MAX_USER_ID` : règle de sélection, seuls les ratings des lecteurs avec `user_id < MAX_USER_ID` sont chargés.

## Utilisation de l'IA
Claude Code (Anthropic) a été utilisé pour écrire le script de base qui charge les CSV dans MongoDB ([bookscope/load_db.py](bookscope/load_db.py)). 



