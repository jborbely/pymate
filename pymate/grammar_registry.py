import plistlib

import cson

from . import Infinity
from . import Grammar
from .null_grammar import NullGrammar


class GrammarRegistry(object):

    def __init__(self, options=None):
        if options is None:
            self.maxTokensPerLine = Infinity
            self.maxLineLength = Infinity
        else:
            self.maxTokensPerLine = options.maxTokensPerLine
            self.maxLineLength = options.maxLineLength
        self.nullGrammar = NullGrammar(self)
        self.clear()

    def __repr__(self):
        space = ' '
        s = [self.__class__.__name__ + ' {']
        for item in sorted(vars(self)):
            obj = getattr(self, item)
            if item  == 'nullGrammar':
                continue
            elif item == 'grammarsByScopeName':
                s.append(space*2 + item + ': {')
                for i, grammar in enumerate(obj):
                    s.append(space * 4 + grammar + ':')
                    s.extend([space*6 + a for a in str(obj[grammar]).splitlines()])
                s.append(space*2 + '}')
            elif item == 'grammars':
                s.append(space*2 + item + ': [')
                for grammar in obj:
                    for a in str(grammar).splitlines():
                        s.append(space*4 + a)
                s.append(space*2 + ']')
            else:
                s.append(space*2 + item + ': ' + str(obj))
        s.append('}')
        return '\n'.join(s)

    def clear(self):
        self.grammars = []
        self.grammarsByScopeName = {}
        self.injectionGrammars = []
        self.grammarOverridesByPath = {}
        self.scopeIdCounter = -1
        self.idsByScope = {}
        self.scopesById = {}
        self.addGrammar(self.nullGrammar)

    def getGrammars(self):
        return self.grammars

    def grammarForScopeName(self, scopeName):
        try:
            return self.grammarsByScopeName[scopeName]
        except KeyError:
            return None

    def addGrammar(self, grammar):
        self.grammars.append(grammar)
        self.grammarsByScopeName[grammar.scopeName] = grammar
        if grammar.injectionSelector:
            self.injectionGrammars.append(grammar)
        self.grammarUpdated(grammar.scopeName)

    def removeGrammar(self, grammar):
        self.grammars.remove(grammar)
        del self.grammarsByScopeName[grammar.scopeName]
        if grammar.injectionSelector:
            self.injectionGrammars.remove(grammar)
        self.grammarUpdated(grammar.scopeName)

    def removeGrammarForScopeName(self, scopeName):
      grammar = self.grammarForScopeName(scopeName)
      if grammar:
        self.removeGrammar(grammar)
      return grammar

    def readGrammarSync(self, grammarPath):
        grammar = None
        with open(grammarPath, 'rb') as fp:
            if grammarPath.endswith('.cson'):
                print('loaded ' + grammarPath + ' using cson')
                grammar = cson.load(fp)
            elif grammarPath.endswith('.tmLanguage'):
                print('loaded ' + grammarPath + ' using plistlib')
                grammar = plistlib.load(fp)
            else:
                raise ValueError('Cannot read ' + grammarPath)

        if isinstance(grammar['scopeName'], str) and grammar['scopeName']:
            return self.createGrammar(grammarPath, **grammar)
        else:
          raise ValueError('Grammar missing required scopeName property: ' + grammarPath)

    def loadGrammarSync(self, grammarPath):
        grammar = self.readGrammarSync(grammarPath)
        self.addGrammar(grammar)
        return grammar

    def startIdForScope(self, scope):
        id_ = self.idsByScope.get(scope)
        if id_:
            return id_
        id_ = self.scopeIdCounter
        self.scopeIdCounter -= 2
        self.idsByScope[scope] = id_
        self.scopesById[id_] = scope
        return id_

    def endIdForScope(self, scope):
        return self.startIdForScope(scope) - 1

    def scopeForId(self, id_):
        if (id_%2) * id_//abs(id_) == -1:
            return self.scopesById[id_]
        else:
            return self.scopesById[id_ + 1]

    def grammarUpdated(self, scopeName):
        pass  # just emits signals

    def createGrammar(self, grammarPath, **options):
        grammar = Grammar(self, **options)
        grammar.path = grammarPath
        return grammar

    def decodeTokens(self, lineText, tags, scopeTags=None, fn=None):

        if not scopeTags:
          scopeTags = []

        offset = 0
        scopeNames = [self.scopeForId(tag) for tag in scopeTags]

        tokens = []
        for index, tag in enumerate(tags):
            if tag >= 0:
                token = {
                    'value': lineText[offset:offset + tag],
                    'scopes': scopeNames[:]
                }
                if fn is not None:
                    token = fn(token, index)
                tokens.append(token)
                offset += tag
            elif (tag % 2) * tag//abs(tag) == -1:
                scopeTags.append(tag)
                scopeNames.append(self.scopeForId(tag))
            else:
                scopeTags.pop()
                expectedScopeName = self.scopeForId(tag + 1)
                poppedScopeName = scopeNames.pop()
                if poppedScopeName != expectedScopeName:
                    raise ValueError("Expected popped scope to be " + expectedScopeName + ", but it was " + poppedScopeName)
        return tokens
