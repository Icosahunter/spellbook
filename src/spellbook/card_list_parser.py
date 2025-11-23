from lark import Lark
from pathlib import Path

ebnf_path = Path(__file__).parent / 'card_list.ebnf'
ebnf_text = ''
with open(ebnf_path) as f:
    ebnf_text = f.read()

parser = Lark(ebnf_text, start='lines')
text = """
#my comment!
Maybeboard #for maybe boards
1 Assassin [squib 33]
"""
print(parser.parse(text).pretty())
