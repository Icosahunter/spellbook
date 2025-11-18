from difflib import SequenceMatcher
from spellbook.directories import db_file
import os
import time
import warnings
with warnings.catch_warnings():
    warnings.simplefilter('ignore', UserWarning)
    import mtgtools.MtgDB
    MtgDB = mtgtools.MtgDB.MtgDB

mtg_db = MtgDB(str(db_file))

if time.time() - os.path.getmtime(db_file) > 2592000:
    print("Updating MTG card database...")
    mtg_db.scryfall_bulk_update()
    print("Done.\n")

def get_card(name):
    matches = mtg_db.root.scryfall_cards.where_exactly(name=name)
    matches = [x for x in matches if x.layout not in ['token', 'art_series', 'double_faced_token', 'emblem']]
    if matches:
        return matches[0]
    matches = mtg_db.root.scryfall_cards.filtered(card_filter(name))
    matches.sort(lambda card: fuzzy_compare(card.name, name))
    if matches:
        if len(matches) > 1:
            if len(set((x.name for x in matches))) == 1:
                return matches[0]
            else:
                print(f'Multiple possible matches for "{name}", select one:')
                for i in range(len(matches)):
                    print(f'  [{i}] {matches[i]}')
                print(f'  [{len(matches)}] None of the above')
                selection = None
                while not selection:
                    selection_str = input()
                    if selection_str.isdigit():
                        selection = int(selection_str)
                        if selection < 0 or selection > len(matches):
                            selection = None
                    if not selection:
                        print('Invalid selection.')
                if selection != len(matches):
                    return matches[selection]
        else:
            return matches[0]
        print(f'Could not find any cards matching "{name}"')
    return None


def card_filter(query, threshold = 0.7):
    def _card_filter(card):
        if card.layout in ['token', 'art_series', 'double_faced_token', 'emblem']:
            return False
        if card.card_faces:
            compares = [fuzzy_compare(query, x['name']) for x in card.card_faces]
            compares.append(fuzzy_compare(query, card.name))
            return max(compares) > threshold
        else:
            return fuzzy_compare(query, card.name) > threshold
    return _card_filter

def fuzzy_compare(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()
