# Rahim & Jean Thomas
#! /usr/bin/python
# -*- encoding: utf8 -*-

# -----
# TP Implementation of the Earley algorithm (with pred function)
#
# 1) Familiarize yourself with the code.
# 2) Implement the incomplete functions (those containing the keyword "pass").
#
# You are of course allowed to define auxiliary functions or add methods to classes,
# but all your code must be carefully commented:
# - the role or return value of each function must be specified, as well as how it works
# - any variable creation must be accompanied by a comment on its role/meaning.

class Symbol:
    # field name: String
    # (no methods)

    def __init__(self, name):
        # name: String

        self.name = name

    def __str__(self):
        return self.name


class Rule:
    # field lhs: Symbol
    # field rhs: list of Symbol
    # (no methods)

    def __init__(self, lhs, rhs):
        # lhs: Symbol
        # rhs: list of Symbol

        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return str(self.lhs) + " --> [" + ",".join([str(s) for s in self.rhs]) + "]"


class Grammar:
    # field symbols: list of Symbol
    # field axiom: Symbol
    # field rules: list of Rule
    # field nonTerminals: set of Symbol
    # field name: String
    # method createNewSymbol: String -> Symbol
    # method isNonTerminal: Symbol -> Boolean

    def __init__(self, symbols, axiom, rules, name):
        # symbols: list of Symbol
        # axiom: Symbol
        # rules: list of Rule
        # name: String

        self.symbols = symbols
        self.axiom = axiom
        self.rules = rules
        self.name = name

        self.nonTerminals = set()
        for rule in rules:
            self.nonTerminals.add(rule.lhs)

    # Returns a new symbol (with a new name build from the argument)
    def createNewSymbol(self, symbolName):
        # symbolName: String

        name = symbolName

        ok = False
        while (ok == False):
            ok = True
            for s in self.symbols:
                if s.name == name:
                    ok = False
                    continue

            if ok == False:
                name = name + "'"

        return Symbol(name)

    def isNonTerminal(self, symbol):
        # symbol: Symbol

        return symbol in self.nonTerminals

    def __str__(self):
        return "{" + \
               "symbols = [" + ",".join([str(s) for s in self.symbols]) + "] " + \
               "axiom = " + str(self.axiom) + " " + \
               "rules = [" + ", ".join(str(r) for r in self.rules) + "]" + \
               "}"


class Item:
    # field lhs: Symbol
    # field bd: list of Symbol
    # field ad: list of Symbol
    # field i: Integer

    def __init__(self, i,lhs, bd, ad):  # [i,lhs --> bd•ad]
        self.lhs = lhs
        self.bd = bd
        self.ad = ad
        self.i = i

    def __str__(self):
        return "[%d,%s --> %s • %s]" % \
               (self.i, str(self.lhs), ",".join([str(s) for s in self.bd]), ",".join([str(s) for s in self.ad]))

    def __eq__(self, other):
        return self.i == other.i and \
               self.lhs == other.lhs and self.bd == other.bd and self.ad == other.ad

class TableCell:
    # field c: list of Item
    # method cAppend: add Item to table cell


    c = []  # cell

    def __init__(self):
        self.c = []


    # Adds an item at the end of the t (+ prints some log), argument reason indicates the name of operations:"init","pred","scan","comp"
    def cAppend(self, item, reason=None):
        if reason is not None:
            reasonStr =  reason + ": "
        else:
            reasonStr = ""

        if item not in self.c:
            self.c.append(item)
            print(reasonStr+ str(item) )


# ------------------------

# Creation and initialisation of the table T for the word w and the grammar gr
def init(g, w):
    # g: Grammar
    # w: word

    T = {}

    for i in range(len(w) + 1):
        T[i] = TableCell() # key: indice, value: TableCell (list of Item)

    for rule in g.rules:
        if (rule.lhs.name == "S"):
            item = Item(0, rule.lhs, [], rule.rhs) # rule lhs has to be the axiom
            T[0].cAppend(item, "init")

    return T

# Insert in the table any new items resulting from the pred operation for the item it
def pred(g, it, T, j):
    # g: Grammar
    # it: Item
    # T: table
    # j : index

    # fs_ad: Symbol (first symbol after the dot, it is a non-terminal symbol)
    fs_ad = it.ad[0]
    # iterate over rules
    for r in g.rules:
        # add an item with the rule r to the cell if the first symbol after the dot is on the left hand side of the rule
        if r.lhs.name == fs_ad.name:
            T[j].cAppend( Item (j, r.lhs, [], r.rhs), "pred" )

# Insert in the table any new items resulting from the scan operation for the item it
def scan(it,T,j):
    # it: Item
    # T: table
    # j: index

    pass

# Insert in the table any possible new items resulting from the comp operation for the item it
def comp(it,T,j):
    # it: Item
    # T: table
    # j: index

    pass



# Return True if the analysis is successful, otherwise False 
def table_complete(g, w, T):
    # g: Grammar
    # w: word
    # T: table

    pass

    return False

# Parse the word w for the grammar g return the parsing table at the end of the algorithm
def parse_earley(g, w):
    # g: Grammar
    # w: word


    # Initialisation
    T = init(g,w)

    # Top-down analysis
    # iterate over cells in the chart T
    for i_c in range(len(w) + 1):
        i_it = 0
        # iterate over items in the i_c-th cell in T
        while ( i_it < len(T[i_c].c) ):
            # PRED ?
            # fs_ad: Symbol (first symbol after the dot)
            # T[i_c].c[i_it]: Item (i_it-th item in the i_c-th cell in T)
            if len(T[i_c].c[i_it].ad) > 0: # check if there is a symbol after the dot to solve index out of bounds problem next line
                fs_ad = T[i_c].c[i_it].ad[0]
                if g.isNonTerminal(fs_ad):
                    pred(g, T[i_c].c[i_it], T, i_c)
            i_it += 1

    if table_complete(g, w, T):
        print("Success")
    else:
        print("Failed parsing")

    return T

# --------------
# Definition of the symbols
symS = Symbol("S")
symA = Symbol("A")
symTerminalA = Symbol("a")
symTerminalB = Symbol("b")

# Definition of a grammar
g1 = Grammar(
    # All symbols
    [symS, symA, symTerminalA, symTerminalB],

    # Axiom
    symS,

    # List of rules
    [
        Rule(symS, [symA, symS]),  # S --> AS
        Rule(symS, [symTerminalB]),  # S --> b
        Rule(symA, [symTerminalA]),  # A --> a
    ],

    # name
    "g1"
)

# Definition of a grammar
g2 = Grammar(
    # All symbols
    [symS, symA, symTerminalA, symTerminalB],

    # Axiom
    symS,

    # List of rules
    [
        Rule(symS, [symA, symS]),  # S --> AS
        Rule(symS, [symTerminalB]),  # S --> b
        Rule(symA, [symA]),  # A --> A
        Rule(symA, [symTerminalA]),  # A --> a
    ],

    # name
    "g2"
)

# for w in words:
#	execute(w, g2)

# Definition of a grammar
g3 = Grammar(
    # All symbols
    [symS, symA, symTerminalA, symTerminalB],

    # Axiom
    symS,

    # List of rules
    [
        Rule(symS, [symA, symS]),  # S --> AS
        Rule(symS, [symA]),  # S --> A
        Rule(symA, [symS]),  # A --> S
        Rule(symS, [symTerminalB]),  # S --> b
        Rule(symS, [symTerminalB, symTerminalB]),  # S --> bb
        Rule(symA, []),  # A --> [epsilon]
        Rule(symA, [symTerminalA]),  # A --> a
    ],

    # name
    "g3"
)

# --------------
words = ["aab", "b", "aaaaab", "abab"]

print("GRAMMAR 1:")
print(g1)
print()
for word in words:
    print(f"Word: {word}")
    parse_earley(g1,word)


print("GRAMMAR 2:")
print(g2)
print()
for word in words:
    print(f"Word: {word}")
    parse_earley(g2,word)


print("GRAMMAR 3:")
print(g3)
print()
for word in words:
    parse_earley(g3,word)

