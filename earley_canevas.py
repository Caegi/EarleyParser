# authors: Rahim & Jean Thomas
#! /usr/bin/python
# -*- encoding: utf8 -*-

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

    # returns a Bolean value if the symbol as input is a non-terminal symbol
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
        T[i] = TableCell() # key: indice, value: TableCell

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
        # if the first symbol after the dot is on the left hand side of the rule r
        if r.lhs.name == fs_ad.name:
            # add an item with the rule r to the cell
            T[j].cAppend( Item (j, r.lhs, [], r.rhs), "pred" )

# Insert in the table any new items resulting from the scan operation for the item it
def scan(it,T,j):
    # it: Item
    # T: table
    # j: index

    # copy the item to avoid modifying the original item
    # it2add: Item
    it2add = it

    # fs_ad: Symbol (store the first symbol after the dot)
    fs_ad = it2add.ad[0]
    it2add.bd.append(fs_ad)
    it2add.ad = it2add.ad[1:]

    # add the new item to the chart
    T[j + 1].cAppend(it2add, "scan")

# Insert in the table any possible new items resulting from the comp operation for the item it
def comp(it,T,j):
    # it: Item
    # T: table
    # j: index

    k = 0
    # iterate over items in the cell of the indice of the current item it in T
    # T[it.i].c: list[Item]
    while k < len(T[it.i].c):
        # compItem: Item (item that is being analysed in the comp operation)
        compItem = T[it.i].c[k]

        # if the item expects the current non-terminal symbol (it.lhs) after the dot
        if ( (len(compItem.ad) > 0) and (compItem.ad[0].name == it.lhs.name) ):
            # create a new item by moving the dot to the right
            newItem = Item(compItem.i, compItem.lhs, compItem.bd + [it.lhs], compItem.ad[1:])
            # add the new item to the chart
            T[j].cAppend(newItem, "comp")

        k += 1

# Return True if the analysis is successful, otherwise False 
def table_complete(g, w, T):
    # g: Grammar
    # w: word
    # T: table

    # final_cell: TableCell
    final_cell = T[len(w)]  # Get the final cell in the parsing table

    # Check if there is an item in the final cell indicating successful parsing
    for item in final_cell.c:
        if item.lhs == g.axiom and item.ad == [] and item.i == 0:
            return True

    return False

# Parse the word w for the grammar g return the parsing table at the end of the algorithm
def parse_earley(g, w):
    # g: Grammar
    # w: word

    # Initialisation
    T = init(g, w)

    # Top-down analysis
    # iterate over cells in the chart T (j: index of the cell)
    for j in range(len(w) + 1):
        k = 0
        # iterate over items in the j-th cell in the chart T
        # T[i_c].c: list[item]
        while k < len(T[j].c):
            # currentItem: Item (item that is being analysed in the main loop)
            currentItem = T[j].c[k]

            # COMP
            if len(currentItem.ad) == 0:
                comp(currentItem, T, j)

            # PRED
            # check if first symbol after the dot is a non-terminal symbol
            # currentItem.ad[0]: Symbol
            elif g.isNonTerminal(currentItem.ad[0]):
                pred(g, currentItem, T, j)

            # SCAN
            elif j < len(w):  # to make sure to not trigger the scan operation in the last cell
                # We know the first symbol after the dot is a terminal symbol since it is the last option left
                # (either nothing after dot, or a non-terminal or a terminal symbol)
                # Check if it corresponds to the character of the word to parse w at index j
                if (w[j] == currentItem.ad[0].name):
                    scan(currentItem, T, j)

            k += 1

    if table_complete(g, w, T):
        print("Success")
    else:
        print("Failed parsing\n")

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
    print(f"\nWord: {word}")
    parse_earley(g1,word)


print("GRAMMAR 2:")
print(g2)
print()
for word in words:
    print(f"\nWord: {word}")
    parse_earley(g2,word)


print("GRAMMAR 3:")
print(g3)
print()
for word in words:
    print(f"\nWord: {word}")
    parse_earley(g3,word)



