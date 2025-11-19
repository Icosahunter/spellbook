import typer
from pathlib import Path
from spellbook.mtg_db import *
from spellbook.directories import *
from spellbook.card_collection import CardCollection
from spellbook.card_list import CardList

app = typer.Typer()

@app.command()
def update_db():
    """
        Update the local MTG card database. This is used for spellchecking your cards among other things.
        It is automatically updated if the current database file is older than 30 days.
    """
    print("Updating MTG card database...")
    mtg_db.scryfall_bulk_update()
    print("Done")

@app.command()
def search(name: str, collection: str='default'):
    """
        Search the collection for a card by name.
    """
    col = CardCollection(collection, collection_dir)
    print(col.cards.search(name).dumps())

@app.command()
def log(collection: str='default'):
    """
        List the log files for the collection.
        These files track cards you've added or removed.
    """
    print(collection + ' logs')
    col = CardCollection(collection, collection_dir)
    for x in col.history_path.glob('*.txt'):
        print(x.stem)

@app.command()
def backups(collection: str='default'):
    """
        List backup files.
        These files are created right before you add or remove cards.
    """
    print(collection + ' backups')
    col = CardCollection(collection, collection_dir)
    for x in col.backups_path.glob('*.txt'):
        print(x.stem)

@app.command()
def restore(backup: str, collection: str='default'):
    """
        Restore your collection from a backup file.
    """
    col = CardCollection(collection, collection_dir)
    col.restore(backup)

@app.command()
def add(name: str, collection: str='default'):
    """
        Add cards to a collection.
        You can specify a single card by name, or a path to a text file containing a list of cards.
    """
    col = CardCollection(collection, collection_dir)
    if Path(name).exists():
        cards = CardList(name)
        cards.resolve_cards()
        col.add_cardlist(cards, comment=Path(name).stem)
    else:
        card = get_card(name)
        if card:
            col.add_card(card.name, comment=Path(name).stem)
    col.save()

@app.command()
def remove(name: str, collection: str='default'):
    """
        Remove cards from a collection.
        You can specify a single card by name, or a path to a text file containing a list of cards.
    """
    col = CardCollection(collection, collection_dir)
    if Path(name).exists():
        cards = CardList(name)
        cards.resolve_cards()
        col.remove_cardlist(cards, comment=Path(name).stem)
    else:
        card = get_card(name)
        if card:
            col.remove_card(card.name, comment=Path(name).stem)
    col.save()

if __name__ == "__main__":
    app()
