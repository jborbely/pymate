import pypeg2

def parse(input):

    return

# def parse(input):
#     var options = arguments.length > 1 ? arguments[1] : {},
#
#     peg$FAILED = {},
#
#     peg$startRuleFunctions = { start: peg$parsestart },
#     peg$startRuleFunction  = peg$parsestart,
#
#     peg$c0 = peg$FAILED,
#     peg$c1 = function(selector) {
#       return selector;
#     },
#     peg$c2 = [],
#     peg$c3 = /^[a-zA-Z0-9+_]/,
#     peg$c4 = { type: "class", value: "[a-zA-Z0-9+_]", description: "[a-zA-Z0-9+_]" },
#     peg$c5 = /^[a-zA-Z0-9\-+_]/,
#     peg$c6 = { type: "class", value: "[a-zA-Z0-9\\-+_]", description: "[a-zA-Z0-9\\-+_]" },
#     peg$c7 = function(segment) {
#         return new matchers.SegmentMatcher(segment);
#       },
#     peg$c8 = /^[*]/,
#     peg$c9 = { type: "class", value: "[*]", description: "[*]" },
#     peg$c10 = function(scopeName) {
#         return new matchers.TrueMatcher();
#       },
#     peg$c11 = ".",
#     peg$c12 = { type: "literal", value: ".", description: "\".\"" },
#     peg$c13 = function(first, others) {
#         return new matchers.ScopeMatcher(first, others);
#       },
#     peg$c14 = null,
#     peg$c15 = /^[LRB]/,
#     peg$c16 = { type: "class", value: "[LRB]", description: "[LRB]" },
#     peg$c17 = ":",
#     peg$c18 = { type: "literal", value: ":", description: "\":\"" },
#     peg$c19 = function(prefix, first, others) {
#         return new matchers.PathMatcher(prefix, first, others);
#       },
#     peg$c20 = "(",
#     peg$c21 = { type: "literal", value: "(", description: "\"(\"" },
#     peg$c22 = ")",
#     peg$c23 = { type: "literal", value: ")", description: "\")\"" },
#     peg$c24 = function(prefix, selector) {
#         return new matchers.GroupMatcher(prefix, selector);
#       },
#     peg$c25 = "-",
#     peg$c26 = { type: "literal", value: "-", description: "\"-\"" },
#     peg$c27 = function(group) {
#         return new matchers.NegateMatcher(group);
#       },
#     peg$c28 = function(path) {
#         return new matchers.NegateMatcher(path);
#       },
#     peg$c29 = /^[|&\-]/,
#     peg$c30 = { type: "class", value: "[|&\\-]", description: "[|&\\-]" },
#     peg$c31 = function(left, operator, right) {
#         return new matchers.CompositeMatcher(left, operator, right);
#       },
#     peg$c32 = ",",
#     peg$c33 = { type: "literal", value: ",", description: "\",\"" },
#     peg$c34 = function(left, right) {
#         if (right)
#           return new matchers.OrMatcher(left, right);
#         else
#           return left;
#       },
#     peg$c35 = /^[ \t]/,
#     peg$c36 = { type: "class", value: "[ \\t]", description: "[ \\t]" },
#
#     peg$currPos          = 0,
#     peg$reportedPos      = 0,
#     peg$cachedPos        = 0,
#     peg$cachedPosDetails = { line: 1, column: 1, seenCR: false },
#     peg$maxFailPos       = 0,
#     peg$maxFailExpected  = [],
#     peg$silentFails      = 0,
#
#     peg$result;
#
#     if ("startRule" in options) {
#       if (!(options.startRule in peg$startRuleFunctions)) {
#         throw new Error("Can't start parsing from rule \"" + options.startRule + "\".");
#       }
#
#       peg$startRuleFunction = peg$startRuleFunctions[options.startRule];
#     }
