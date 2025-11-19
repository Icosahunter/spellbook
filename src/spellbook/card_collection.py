from spellbook.mtg_db import *
from spellbook.card_list import CardList
import shutil
from datetime import datetime
from pathlib import Path

class CardCollection:
    def __init__(self, name, dir):
        self.name = name
        self.dir = Path(dir)
        self.path = dir / name / 'cards.txt'
        self.history_path = dir / name / 'history'
        self.backups_path = dir / name / 'backups'

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.history_path.mkdir(parents=True, exist_ok=True)
        self.backups_path.mkdir(parents=True, exist_ok=True)

        self.cards = CardList(self.path)

    def add_card(self, name, set_code=None, collector_number=None, count=1, log=True, comment=''):
        self.cards.add(name, set_code, collector_number, count)
        if log:
            self.log_cards(name, 'added - ' + comment)

    def remove_card(self, name, set_code=None, collector_number=None, count=1, log=True, comment=''):
        self.cards.sub(name, set_code, collector_number, count)
        if log:
            self.log_cards(name, 'removed - ' + comment)

    def add_cardlist(self, cardlist, log=True, comment=''):
        self.cards.extend(cardlist)
        self.cards.consolidate_cards()
        if log:
            self.log_cards(cardlist, 'added - ' + comment)

    def remove_cardlist(self, cardlist, log=True, comment=''):
        for card in cardlist:
            self.cards.sub(card['name'], card['set_code'], card['collector_number'], card['count'])
        if log:
            self.log_cards(cardlist, 'removed - ' + comment)

    def log_cards(self, cards, comment):
        timestamp = (datetime.now().strftime('%Y%m%dT%H%M%S'))
        log_filepath = self.history_path / f'{timestamp} - {comment}.txt'
        if isinstance(cards, CardList):
            cards.dump(log_filepath)
        else:
            with open(log_filepath, 'w+') as f:
                f.write(cards)

    def _backup(self):
        timestamp = (datetime.now().strftime('%Y%m%dT%H%M%S'))
        backup_filepath = (self.backups_path / timestamp).with_suffix('.txt')
        shutil.move(self.path, backup_filepath)

    def save(self):
        self._backup()
        self.cards.dump(self.path)

    def restore(self, backup):
        backup_path = (self.backups_path / backup).with_suffix('.txt')
        if backup_path.exists():
            self._backup()
            shutil.copy(backup_path, self.path)
            self.log_cards(self.cards, f'restored - {backup}')
            self.cards = CardList(self.path)
        else:
            print(f'ERROR: No backup found named {backup}.')
