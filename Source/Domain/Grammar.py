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
        #configuration
        self.configState = ""
        self.configPosition = 0
        self.configWorkingStack = []
        self.configInputStack = []

    def CFGCheck(self):
        for key in self.productions:
            counter = 0
            for nonTerminal in self.nonTerminals:
                if key == nonTerminal:
                    counter += 1
            if counter != 1:
                return False
        return True

    def _appendProductions(self, nonTerminal, index):
        self.configWorkingStack.append((nonTerminal, index))
        productionResult = self.productions[nonTerminal][index]
        for result in reversed(productionResult):
            self.configInputStack.append(result)

    def _expand(self):
        nonTerminal = self.configInputStack.pop()
        self._appendProductions(nonTerminal, 0)

    def _advance(self):
        self.configPosition += 1
        self.configWorkingStack.append(self.configInputStack.pop())

    def _momentaryInsuccess(self):
        self.configState = "b"

    def _back(self):
        self.configPosition -= 1
        self.configInputStack.append(self.configWorkingStack.pop())

    def _anotherTry(self):
        nonTerminal, index = self.configWorkingStack.pop()
        popLen = len(self.productions[nonTerminal][index])
        for i in range(popLen):
            self.configInputStack.pop()

        if self.configPosition == 1 and nonTerminal == self.start:
            self.configState = "e"

        elif index + 1 < len(self.productions[nonTerminal]):
            self.configState = "q"
            index += 1
            self._appendProductions(nonTerminal, index)

        else:
            self.configInputStack.append(nonTerminal)

    def _success(self):
        self.configState = "f"

    def parse(self, sequence):
        #init config
        self.configState = "q"
        self.configPosition = 0
        self.configWorkingStack = []
        self.configInputStack = self.start

        while self.configState not in ["f", "e"]:
            if self.configState == "q":
                if self.configPosition == len(sequence) and len(self.configInputStack) == 0:
                    self._success()
                elif self.configInputStack[-1] in self.nonTerminals:
                    self._expand()
                elif self.configPosition < len(sequence):
                    if self.configInputStack[-1] == sequence[self.configPosition]:
                        self._advance()
                    else:
                        self._momentaryInsuccess()
                else:
                    self._momentaryInsuccess()
            elif self.configState == "b":
                if self.configWorkingStack[-1] in self.terminals:
                    self._back()
                else:
                    self._anotherTry()

        if self.configState == "e":
            return "Error"

        return "Success"






