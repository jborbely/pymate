import os
import codecs
from pymate import GrammarRegistry

debug_folder = None  # 'regexp'
debug_filename = None  # 'escaping4.re'
source_spec = "[start\\a\\b\\c\\d\\f\\n\\r\\t\\v]"

#from PyQt5 import QtCore
#x = "(?x)\\s*(class)\\s+\\p{L}*(?=[[:alpha:]_]\\w*\\s*(:|\\())"
#regex = QtCore.QRegularExpression(x)
#match = regex.match(source_spec)
#print(match.hasMatch())
#print(match.capturedTexts())

root_path = '../MagicPython/test/'

paths = []
for root, _, files in os.walk(root_path):
    if root.endswith('atom-spec'):
        continue
    for file in files:
        paths.append(os.path.join(root, file))

registry = GrammarRegistry()
grammar_py = registry.loadGrammarSync('MagicPython.cson')
grammar_rx = registry.loadGrammarSync('MagicRegExp.cson')


def normalize_scopes(scopes):
    if isinstance(scopes, str):
        scp = [s.strip() for s in scopes.strip().split(',')]
    else:
        scp = scopes
    s = []
    for val in scp:
        s.extend(val.split())
    return s


for path in paths:
    source = None
    results = []
    filename = os.path.basename(path)
    folder = os.path.basename(os.path.dirname(path))

    if debug_filename and filename != debug_filename or debug_folder and debug_folder != folder:
        continue

    if folder == 'unicode':
        print(r'QtCore.QRegularExpression requires \p{L} to represent special unicode characters. Ignoring: %s/%s' % (folder, filename))
        continue

    print(path)

    if filename.endswith('.py'):
        spec = '../MagicPython/test/atom-spec/python-spec.js'
        grammar = grammar_py
    else:
        spec = '../MagicPython/test/atom-spec/python-re-spec.js'
        grammar = grammar_rx

    with codecs.open(spec, mode='r', encoding='utf-8') as fp:
        for line in fp:
            if line.startswith(f'  it("test/{folder}/{filename}",'):
                fp.readline()
                source = fp.readline().split('tokenizeLines("')[1].rstrip()[:-2]
                source = source.replace(r'\\\n', '4b0e4cac140a').replace('\\n', '\n').replace('4b0e4cac140a', '\\\n')
                source = source.replace('\\\"', '\"')
                source = source.replace("\\\'", "\'")
                source = source.replace("\\\\", "\\")
                source = source.replace('\\f \\\n \\r', '\\f \\n \\r')
                source = source.replace('\n"""\\\n>>>', '\n"""\\n>>>')
                source = source.replace('bar\\t', 'bar\t')
                source = source.replace('bar()\\t', 'bar()\t')
                source = source.replace("'''\\\n\n{%", "'''\\n\n{%")
                source = source.replace("\\\n {{ item }", "\\n {{ item }")
                source = source.replace('}} \\\n \\N', '}} \\n \\N')
                source = source.replace('\\\nÅ', '\\nÅ')
                source = source.replace('\\f\\\n\\r', '\\f\\n\\r')
                break

    with codecs.open(path, mode='r', encoding='utf-8') as fp:
        for line in source.splitlines():
            fp.readline()
        for line in fp:
            if not line.strip():
                while not line.strip():
                    line = fp.readline()
                value, _, scopes = line.rpartition(':')
                results.append({'value': value, 'scopes': normalize_scopes(scopes)})
                for line2 in fp:
                    value, _, scopes = line2.rpartition(':')
                    results.append({'value': value, 'scopes': normalize_scopes(scopes)})

    if debug_filename and filename == debug_filename and debug_folder and debug_folder == folder:
        print(repr(source))
        print(repr(source_spec))
        assert repr(source) == repr(source_spec)

    tokens = grammar.tokenizeLines(source)

    k = 0
    for token in tokens:
        for item in token:
            #print('{:25s} : {}'.format(item['value'].strip(), ', '.join(item['scopes'])))
            if item['value'].strip() != results[k]['value'].strip():
                raise ValueError(item['value'].strip() + ' IS NOT EQUAL TO ' + results[k]['value'].strip())
            scopes = normalize_scopes(set(item['scopes']))  # use a set to remove an scopes that are repeated
            if len(scopes) != len(results[k]['scopes']):
                raise ValueError('\n' + ' '.join(sorted(scopes)) + '\nDOES NOT HAVE THE SAME LENGTH AS\n' + ' '.join(sorted(results[k]['scopes'])))
            for scope in results[k]['scopes']:
                if scope not in scopes:
                    raise ValueError(scope + ' IS NOT IN ' + ' '.join(scopes))
            k += 1


def assert_scopes(expect, token_scope):
    assert len(token_scope) == len(expect), str(expect) + ' != ' + str(token_scope)
    for scope in token_scope:
        assert scope in expect


print('testing python-console.cson')
grammar_console = registry.loadGrammarSync('python-console.cson')
tokens = grammar_console.tokenizeLines(">>> print")
assert tokens[0][0]['value'] == '>>>'
assert_scopes(['text.python.console', 'punctuation.separator.prompt.python.console'], tokens[0][0]['scopes'])
assert tokens[0][1]['value'] == " "
assert_scopes(['text.python.console'], tokens[0][1]['scopes'])
assert tokens[0][2]['value'] == "print"
# for the next assertion, the expected result agrees with the result from first-mate
# MagicPython expected ['text.python.console', 'support.function.builtin.python']
assert_scopes(['text.python.console'], tokens[0][2]['scopes'])

print('testing python-traceback.cson')
grammar_tb = registry.loadGrammarSync('python-traceback.cson')
tokens = grammar_tb.tokenizeLines('  File "t.py", line 1, in <module>\n' +
                                  '    a = 1/0')

assert tokens[0][0]['value'] == "  File ", tokens[0][0]['value']
assert_scopes(['text.python.traceback'], tokens[0][0]['scopes'])
assert tokens[0][1]['value'] == '"t.py"'
assert_scopes(['text.python.traceback', 'string.python.traceback'], tokens[0][1]['scopes'])
assert tokens[0][2]['value'] == ", line "
assert_scopes(['text.python.traceback'], tokens[0][2]['scopes'])
assert tokens[0][3]['value'] == "1"
assert_scopes(['text.python.traceback', 'constant.numeric.python.traceback'], tokens[0][3]['scopes'])
assert tokens[0][4]['value'] == ", in "
assert_scopes(['text.python.traceback'], tokens[0][4]['scopes'])
assert tokens[0][5]['value'] == "<module>"
assert_scopes(['text.python.traceback', 'entity.name.function.python.traceback'], tokens[0][5]['scopes'])
# below agrees with first-mate's test but disagrees with MagicPython's test
assert tokens[1][0]['value'] == "    "
assert_scopes(['text.python.traceback'], tokens[1][0]['scopes'])
assert tokens[1][1]['value'] == "a = 1/0"
assert_scopes(['text.python.traceback'], tokens[1][1]['scopes'])
