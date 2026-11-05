# Crée la base MongoDB à partir des CSV.
#
# Une collection par fichier CSV, avec les mêmes colonnes que le fichier.
# Seule transformation : les nombres sont convertis en nombres (le CSV ne contient que du texte)
# et une cellule vide devient null.
#
# Usage : python load_db.py

import csv

from pymongo import MongoClient

from config import DATA_DIR, DB_NAME, MAX_USER_ID, MONGO_URI

FILES = ["books.csv", "tags.csv", "book_tags.csv", "ratings.csv", "to_read.csv"]
BATCH_SIZE = 50_000

# Colonnes toujours gardées en texte (ex. ISBN "0439023483" perdrait son 0 en nombre,
# un tag nommé "2015" ou un titre "1984" deviendraient des nombres)
TEXT_COLUMNS = {"isbn", "isbn13", "title", "original_title", "authors", "tag_name",
                "language_code", "image_url", "small_image_url"}


def convert(column, value):
    """'12' -> 12, '4.34' -> 4.34, '' -> None, sinon le texte tel quel."""
    if value == "":
        return None
    if column in TEXT_COLUMNS:
        return value
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def load_file(db, filename):
    collection = db[filename.removesuffix(".csv")]
    batch, total = [], 0
    with open(DATA_DIR / filename, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            doc = {col: convert(col, val) for col, val in row.items()}
            # Règle de sélection : ratings des lecteurs avec user_id < MAX_USER_ID uniquement
            if filename == "ratings.csv" and doc["user_id"] >= MAX_USER_ID:
                continue
            batch.append(doc)
            if len(batch) == BATCH_SIZE:
                collection.insert_many(batch)
                total += len(batch)
                batch = []
    if batch:
        collection.insert_many(batch)
        total += len(batch)
    print(f"{collection.name}: {total} documents")


def main():
    client = MongoClient(MONGO_URI)
    client.drop_database(DB_NAME)  # on repart d'une base vide
    db = client[DB_NAME]

    for filename in FILES:
        load_file(db, filename)

    # Index pour que les recherches de F1 soient rapides (ils n'ajoutent aucune donnée)
    db.books.create_index("book_id")
    db.books.create_index("goodreads_book_id")
    db.book_tags.create_index("goodreads_book_id")
    db.book_tags.create_index("tag_id")


if __name__ == "__main__":
    main()
