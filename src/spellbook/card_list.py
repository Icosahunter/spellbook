from spellbook.mtg_db import *

class CardList(list):

    def __init__(self, path=None, cleanup=False):
        if path:
            self.load(path)
            if cleanup:
                self.cleanup()

    @staticmethod
    def from_list(lst):
        cardlist = CardList()
        for item in lst:
            cardlist.append(item)
        return cardlist

    def loads(self, str):
        self.clear()
        for line in str.split('\n'):
            self._load_line(line)

    def load(self, path):
        self.clear()
        with open(path, 'r') as f:
            for line in f.readlines():
                self._load_line(line)

    def _load_line(self, line):
        if not line.startswith('//') and not line.startswith('#'):
            count = 1
            set_code = None
            name = None
            split_line = line.split()
            if split_line[0].isdigit():
                count = int(split_line[0])
                split_line = split_line[1:]
            set_codes = [x for x in split_line if x.startswith('[') and x.endswith(']')]
            if len(set_codes) > 0:
                set_code = set_codes[0][1:-1]
                split_line.remove(set_codes[0])
            name = ' '.join(split_line)
            self.append(
                {
                    'name': name,
                    'set': set_code,
                    'count': count
                }
            )

    def dump(self, file):
        with open(file, 'w+') as f:
            f.write(self.dumps())

    def dumps(self):
        text = ''
        for card in self:
            text += str(card['count']) + ' ' + card['name'] + (' ' + card['set'] if card['set'] else '') + '\n'
        return text

    def cleanup(self):
        self.resolve_cards()
        self.consolidate_cards()

    def resolve_cards(self):
        print('Resolving cards...')
        new_cards = []
        for card in self:
            resolved_card = get_card(card['name'])
            if resolved_card:
                new_cards.append({
                    'name': resolved_card.name,
                    'set': card['set'],
                    'count': card['count']
                })

        self.clear()
        self.extend(new_cards)

    def consolidate_cards(self):
        new_cards = []
        done = []
        for card in self:
            if (card['name'], card['set']) not in done:
                dups = [x for x in self if x['name'] == card['name'] and x['set'] == card['set']]
                new_cards.append({
                        'name': card['name'],
                        'set': card['set'],
                        'count': sum([x['count'] for x in dups])
                    })
                done.append((card['name'], card['set']))
        self.clear()
        self.extend(new_cards)

    def search(self, name, set:None|str='*'):
        results = [x for x in self if name.lower() in x['name'].lower()]
        if set != '*':
            results = [x for x in results if x['set'] == set]
        return CardList.from_list(results)

    def add(self, name, set:str|None=None, count=1):
        results = self.search(name, set)
        if results:
            results[0]['count'] += count
        else:
            self.append({'name': name, 'set': set, 'count': count})

    def sub(self, name, set:str|None=None, count=1):
        results = self.search(name, set)
        remaining = count
        if results:
            for result in results:
                if results[0]['count'] <= remaining:
                    remaining -= results[0]['count']
                    self.remove(results[0])
                else:
                    results[0]['count'] -= remaining
                    break
        else:
            print(f'ERROR: No matching cards found.')
        if remaining:
            print(f'WARNING: Only {count - remaining} matching cards found. These have been removed.')

    def to_PCardList(self):
        return mtg_db.root.scryfall_cards.from_str(self.dumps())
