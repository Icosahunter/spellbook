import typer
from typing_extensions import Annotated
from pathlib import Path

from mtg_db import *
from directories import *
from card_collection import CardCollection
from card_list import CardList

app = typer.Typer()

@app.command()
def update_db():
    mtg_db.scryfall_bulk_update()

@app.command()
def add(name: str, collection: str='default'):
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
