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
        self.configInputStack = start

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


class Node:
    def __init__(self, info, parent, rightSibling):
        self.info = info
        self.parent = parent
        self.rightSibling = rightSibling

    def __str__(self):
        return str(self.info) + ", " + str(self.parent) + ", " + str(self.rightSibling)


class ParserOutput:
    def __init__(self, nonTerminals: list, finalWorkingStack: list, productions):
        self.nonTerminals = nonTerminals
        self.finalWorkingStack = finalWorkingStack
        self.parsingTree = []
        self.productions = productions
        self.parentsQueue = []
        self.getRepresentation()

    def printToFile(self, filename):
        pass

    def getRepresentation(self):
        self.finalWorkingStack = list(filter(lambda x: (type(x) is tuple), self.finalWorkingStack))
        nonTerminal, productionIndex = self.finalWorkingStack.pop(0)
        self.parsingTree.append(Node(nonTerminal, 0, 0))
        self._addToParsingTree(1, self.productions[nonTerminal][productionIndex])

        for element in self.finalWorkingStack:
            parentIndex = self.parentsQueue.pop(0)
            nonTerminal, productionIndex = element
            productionResult = self.productions[nonTerminal][productionIndex]
            self._addToParsingTree(parentIndex, productionResult)

    def _addToParsingTree(self, parent, production):
        siblingIndex = 0
        for element in production:
            self.parsingTree.append(Node(element, parent, siblingIndex))
            siblingIndex = len(self.parsingTree)
            if element in self.nonTerminals:
                self.parentsQueue.append(siblingIndex)

    def showParsingTree(self):
        for i in range(len(self.parsingTree)):
            print(str(i+1) + ", " + str(self.parsingTree[i]))







