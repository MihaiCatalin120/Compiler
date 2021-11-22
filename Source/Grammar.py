import json


def readGrammarFromFile(filePath):
    grammarInput = json.load(open(filePath, "r"))
    return Grammar(grammarInput["nonTerminals"], grammarInput["terminals"], grammarInput["start"], grammarInput["productions"])


class Grammar:
    def __init__(self, nonTerminals, terminals, start, productions):
        self.nonTerminals = nonTerminals
        self.terminals = terminals
        self.start = start
        self.productions = productions

    def CFGCheck(self):
        for key in self.productions:
            counter = 0
            for nonTerminal in self.nonTerminals:
                if key == nonTerminal:
                    counter += 1
            if counter != 1:
                return False
        return True

