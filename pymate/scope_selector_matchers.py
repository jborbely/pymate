class SegmentMatcher(object):

    def __init__(self, segments):
        self.segment = ''.join(segments[0]) + ''.join(segments[1])

    def matches(self, scope):
        return scope == self.segment

    def getPrefix(self, scope):
        pass

    def toCssSelector(self):
        df = []
        for dotFragment in self.segment.split('.'):
            df.append('.' + dotFragment.replace('/\+/g', '\\+'))
        return ''.join(df)

    def toCssSyntaxSelector(self):
        df = []
        for dotFragment in self.segment.split('.'):
            df.append('.syntax--' + dotFragment.replace('/\+/g', '\\+'))
        return ''.join(df)


class TrueMatcher(object):

    def matches(self):
        return True

    def getPrefix(self, scopes):
        pass

    def toCssSelector(self):
        return '*'

    def toCssSyntaxSelector(self):
        return '*'


class ScopeMatcher:

    def __init__(self, first, others):
        self.segments = [first]
        for segment in others:
            self.segments.append(segment[1])

    def matches(self, scope):
        lastDotIndex = 0
        for matcherSegmentIndex, matcherSegment in enumerate(self.segments):
            if lastDotIndex > len(scope):
                break

            nextDotIndex = scope.index('.', lastDotIndex)
            if nextDotIndex == -1:
                nextDotIndex = len(scope)

            scopeSegment = scope[lastDotIndex: nextDotIndex]
            if not matcherSegment.matches(scopeSegment):
                return False

            lastDotIndex = nextDotIndex + 1

        return matcherSegmentIndex == len(self.segments)

    def getPrefix(self, scope):
        scopeSegments = scope.split('.')
        if len(scopeSegments) < len(self.segments):
            return False

        for index, segment in enumerate(self.segments):
            if segment.matches(scopeSegments[index]):
                if segment.prefix:
                    return segment.prefix

    def toCssSelector(self):
        return ''.join([matcher.toCssSelector() for matcher in self.segments])

    def toCssSyntaxSelector(self):
        return ''.join([matcher.toCssSyntaxSelector() for matcher in self.segments])


class GroupMatcher(object):

    def __init__(self, prefix, selector):
        self.prefix = prefix[0] if prefix else None
        self.selector = selector

    def matches(self, scopes):
        return self.selector.matches(scopes)

    def getPrefix(self, scopes):
        if self.selector.matches(scopes):
            return self.prefix

    def toCssSelector(self):
        return self.selector.toCssSelector()

    def toCssSyntaxSelector(self):
        return self.selector.toCssSyntaxSelector()


class PathMatcher(object):

    def __init__(self, prefix, first, others):
        self.prefix = prefix[0] if prefix else None
        self.matchers = [first]
        for matcher in others:
            self.matchers.append(matcher[1])

    def matches(self, scopes):
        index = 0
        matcher = self.matchers[index]
        for scope in scopes:
            if matcher.matches(scope):
                index += 1
                matcher = self.matchers[index]
            if not matcher:
                return True
        return False

    def getPrefix(self, scopes):
        if self.matches(scopes):
            return self.prefix

    def toCssSelector(self):
         return ' '.join(matcher.toCssSelector() for matcher in self.matchers)

    def toCssSyntaxSelector(self):
        return ' '.join(matcher.toCssSyntaxSelector() for matcher in self.matchers)


class OrMatcher(object):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def matches(self, scopes):
        return self.left.matches(scopes) or self.right.matches(scopes)

    def getPrefix(self, scopes):
        return self.left.getPrefix(scopes) or self.right.getPrefix(scopes)

    def toCssSelector(self):
        return '' + self.left.toCssSelector() + ', ' + self.right.toCssSelector()

    def toCssSyntaxSelector(self):
        return '' + self.left.toCssSyntaxSelector() + ', ' + self.right.toCssSyntaxSelector()


class AndMatcher(object):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def matches(self, scopes):
        return self.left.matches(scopes) and self.right.matches(scopes)

    def getPrefix(self, scopes):
        if self.left.matches(scopes) and self.right.matches(scopes):
            return self.left.getPrefix(scopes)

    def toCssSelector(self):
        if isinstance(self.right, NegateMatcher):
            return '' + self.left.toCssSelector() + self.right.toCssSelector()
        else:
            return '' + self.left.toCssSelector() + ' ' + self.right.toCssSelector()

    def toCssSyntaxSelector(self):
        if isinstance(self.right, NegateMatcher):
            return '' + self.left.toCssSyntaxSelector() + self.right.toCssSyntaxSelector()
        else:
            return '' + self.left.toCssSyntaxSelector() + ' ' + self.right.toCssSyntaxSelector()


class NegateMatcher(object):

    def __init__(self, matcher):
        self.matcher = matcher

    def matches(self, scopes):
        return not self.matcher.matches(scopes)

    def getPrefix(scopes):
        pass

    def toCssSelector(self):
        return ':not(' + self.matcher.toCssSelector() + ')'

    def toCssSyntaxSelector(self):
        return ':not(' + self.matcher.toCssSyntaxSelector() + ')'


class CompositeMatcher(object):

    def __init__(self, left, operator, right):
        if operator == '|':
            self.matcher = OrMatcher(left, right)
        elif operator == '&':
            self.matcher = AndMatcher(left, right)
        else:
            self.matcher = AndMatcher(left, NegateMatcher(right))

    def matches(self, scopes):
        return self.matcher.matches(scopes)

    def getPrefix(self, scopes):
        return self.matcher.getPrefix(scopes)

    def toCssSelector(self):
        return self.matcher.toCssSelector()

    def toCssSyntaxSelector(self):
        return self.matcher.toCssSyntaxSelector()

