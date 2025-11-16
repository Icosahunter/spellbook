from mtg_db import *
from card_list import CardList
import shutil
from datetime import datetime

class CardCollection:
    def __init__(self, name, dir):
        self.name = name
        self.dir = dir
        self.path = dir / name / 'cards.txt'
        self.history_path = dir / name / 'history'
        self.backups_path = dir / name / 'backups'

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.history_path.mkdir(parents=True, exist_ok=True)
        self.backups_path.mkdir(parents=True, exist_ok=True)

        self.cards = CardList(self.path)

    def add_card(self, name, set=None, count=1, log=True, comment=''):
        self.cards.add(name, set, count)
        if log:
            self.log_cards(name, 'added - ' + comment)

    def remove_card(self, name, set=None, count=1, log=True, comment=''):
        self.cards.sub(name, set, count)
        if log:
            self.log_cards(name, 'removed - ' + comment)

    def add_cardlist(self, cardlist, log=True, comment=''):
        self.cards.extend(cardlist)
        self.cards.consolidate_cards()
        if log:
            self.log_cards(cardlist, 'added - ' + comment)

    def remove_cardlist(self, cardlist, log=True, comment=''):
        for card in cardlist:
            self.cards.sub(card['name'], card['set'], card['count'])
        if log:
            self.log_cards(cardlist, 'removed - ' + comment)

    def log_cards(self, cards, comment):
        timestamp = (datetime.now().strftime('%Y%m%dT%H%M%S.%f')[0:-3])
        log_filepath = self.history_path / f'{timestamp} - {comment}.txt'
        if isinstance(cards, CardList):
            cards.dump(log_filepath)
        else:
            with open(log_filepath, 'w+') as f:
                f.write(cards)

    def save(self):
        backup_filepath = (self.backups_path / (datetime.now().strftime('%Y%m%dT%H%M%S.%f')[0:-3])).with_suffix('.txt')
        shutil.move(self.path, backup_filepath)
        self.cards.dump(self.path)
