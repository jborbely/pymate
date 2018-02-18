import codecs
from pymate import GrammarRegistry

registry = GrammarRegistry()

grammar = registry.loadGrammarSync('MagicPython.cson')

filename = 'builtins3'

source = None
with codecs.open(r'D:\code\git\MagicPython\test\atom-spec\python-spec.js', encoding='utf-8') as fp:
    for line in fp:
        if filename in line:
            fp.readline()
            source = fp.readline().split('tokenizeLines("')[1][:-3].replace('\\n', '\n')
            break

results = []
with codecs.open(r'D:\code\git\MagicPython\test\builtins\%s.py' % filename , encoding='utf-8') as fp:
    found_it = False
    for line in fp:
        if not line.strip():
            while not line.strip():
                line = fp.readline()
            value, scopes = line.split(':')
            results.append({'value': value, 'scopes': [s.strip() for s in scopes.split(',')]})
            for line2 in fp:
                value, scopes = line2.split(':')
                results.append({'value': value.strip(), 'scopes': [s.strip() for s in scopes.split(',')]})

if source:
    tokens = grammar.tokenizeLines(source)
    k = 0
    for token in tokens:
        for item in token:
            assert item['value'].strip() == results[k]['value'].strip(), item['value'].strip() + ' || ' + results[k]['value'].strip()
            assert len(item['scopes']) == len(results[k]['scopes'])
            for scope in results[k]['scopes']:
                assert scope in item['scopes']
            print('{:25s} : {}'.format(item['value'].strip(), ', '.join(item['scopes'])))
            k += 1
