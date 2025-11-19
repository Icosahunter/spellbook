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
            collector_num = None
            name = None

            if line.split()[0].isdigit():
                count = int(line.split()[0])
                line = ' '.join(line.split()[1:])

            lb = min(line.find('['), line.find('('))
            if lb > -1:
                set_code = line[lb:].split()[0].lstrip('[(')
                collector_num = line[lb:].split()[1].rstrip('])')
                name = line[0:lb].strip()
            else:
                name = line.strip()

            self.append(
                {
                    'name': name,
                    'set_code': set_code,
                    'collector_number': collector_num,
                    'count': count
                }
            )

    def dump(self, file):
        with open(file, 'w+') as f:
            f.write(self.dumps())

    def dumps(self):
        text = ''
        for card in self:

            collector_info = ''

            if card['set_code'] or card['collector_number']:
                collector_info += ' ['
                collector_info += card['set_code'] if card['set_code'] else ''
                collector_info += ' ' if card['set_code'] and card['collector_number'] else ''
                collector_info += card['collector_number'] if card['set_code'] else ''
                collector_info += ']'

            text += str(card['count']) + ' ' + card['name'] + collector_info + '\n'

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
                    'set_code': card['set_code'],
                    'collector_number': card['collector_number'],
                    'count': card['count']
                })

        self.clear()
        self.extend(new_cards)

    def consolidate_cards(self):
        new_cards = []
        done = []
        for card in self:
            if (card['name'], card['set_code']) not in done:
                dups = [x for x in self if x['name'] == card['name'] and x['set_code'] == card['set_code']]
                new_cards.append({
                        'name': card['name'],
                        'set_code': card['set_code'],
                        'count': sum([x['count'] for x in dups])
                    })
                done.append((card['name'], card['set_code']))
        self.clear()
        self.extend(new_cards)

    def search(self, name:str, set_code:None|str='*', collector_number:None|str='*', threshold:float=0.6):
        results = [x for x in self if name.lower() in x['name'].lower()]
        if len(results) < 5:
            results.extend([x for x in self if x not in results and fuzzy_compare(name, x['name']) > threshold][0:(5-len(results))])
        if set_code != '*':
            results = [x for x in results if x['set_code'] == set_code]
        if collector_number != '*':
            results = [x for x in results if x['collector_number'] == collector_number]
        results.sort(key=lambda x: fuzzy_compare(x['name'], name), reverse=True)
        return CardList.from_list(results)

    def add(self, name:str, set_code:str|None=None, collector_number:str|None=None, count=1):
        results = self.search(name, set_code, collector_number)
        if results:
            results[0]['count'] += count
        else:
            self.append({'name': name, 'set_code': set_code, 'collector_number': collector_number, 'count': count})

    def sub(self, name:str, set_code:str|None=None, collector_number:str|None=None, count=1):
        results = self.search(name, set_code, collector_number)
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
