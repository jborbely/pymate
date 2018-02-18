from .scope_selector_parser import parse


class ScopeSelector(object):

    def __init__(self, source):
        # Create a new scope selector.
        #
        # source - A {String} to parse as a scope selector.
        self.matcher = parse(source)

    def matches(self, scopes):
        # Check if this scope selector matches the scopes.
        #
        # scopes - An {Array} of {String}s or a single {String}.
        #
        # Returns a {Boolean}.
        if isinstance(scopes, str):
            scopes = [scopes]
        return self.matcher.matches(scopes)

    def getPrefix(self, scopes):
        # Gets the prefix of this scope selector.
        #
        # scopes - An {Array} of {String}s or a single {String}.
        #
        # Returns a {String} if there is a prefix or undefined otherwise.
        if isinstance(scopes, str):
            scopes = [scopes]
        return self.matcher.getPrefix(scopes)

    def toCssSelector(self):
        # Convert this TextMate scope selector to a CSS selector.
        #
        # Returns a {String}.
        return self.matcher.toCssSelector()

    def toCssSyntaxSelector(self):
        # Convert this TextMate scope selector to a CSS selector, prefixing scopes with `syntax--`.
        #
        # Returns a {String}.
        return self.matcher.toCssSyntaxSelector()
