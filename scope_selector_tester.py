import plistlib
from pymate import GrammarRegistry


with open('Chromodynamics.tmTheme', 'rb') as fp:
    data = plistlib.load(fp)

for item in data:
    if isinstance(data[item], str):
        print(item, data[item])
    else:
        for subitem in data[item]:
            print(item, subitem)

print()

root_path = '../MagicPython/test/'
registry = GrammarRegistry()
grammar = registry.loadGrammarSync('MagicPython.cson')

with open('example.py', 'r') as fp:
    source = fp.read()

tokens = grammar.tokenizeLines(source)
for token in tokens:
    for item in token:
        print('{:25s} : {}'.format(item['value'].strip(), ', '.join(item['scopes'])))
