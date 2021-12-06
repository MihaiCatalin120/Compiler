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
        self.configuration = {
            "state": "",
            "position": 0,
            "workingStack": [],
            "inputStack": []
        }

    def CFGCheck(self):
        for key in self.productions:
            counter = 0
            for nonTerminal in self.nonTerminals:
                if key == nonTerminal:
                    counter += 1
            if counter != 1:
                return False
        return True

    def _expand(self):
        nonTerminal = self.configuration["inputStack"].pop()
        self.configuration["workingStack"].append((nonTerminal, 0))
        productionResult = self.productions[nonTerminal][0]
        for result in reversed(productionResult):
            self.configuration["inputStack"].append(result)

    def _advance(self):
        self.configuration["position"] += 1
        self.configuration["workingStack"].append(self.configuration["inputStack"].pop())

    def _momentaryInsuccess(self):
        self.configuration["state"] = "b"

    def _back(self):
        self.configuration["position"] -= 1
        self.configuration["inputStack"].append(self.configuration["workingStack"].pop())

    def _anotherTry(self):
        nonTerminal, index = self.configuration["workingStack"].pop()
        popLen = len(self.productions[nonTerminal][index])
        for i in range(popLen):
            self.configuration["inputStack"].pop()

        if self.configuration["position"] == 1 and nonTerminal == self.start:
            self.configuration["state"] = "e"

        elif index + 1 < len(self.productions[nonTerminal]):
            self.configuration["state"] = "q"
            index += 1
            self.configuration["workingStack"].append((nonTerminal, index))
            productionResult = self.productions[nonTerminal][index]
            for result in reversed(productionResult):
                self.configuration["inputStack"].append(result)

        else:
            self.configuration["inputStack"].append(nonTerminal)

    def _success(self):
        self.configuration["state"] = "f"

    def parse(self, sequence):
        self.configuration = {
            "state": "q",
            "position": 0,
            "workingStack": [],
            "inputStack": self.start
        }
        while self.configuration["state"] not in ["f", "e"]:
            if self.configuration["state"] == "q":
                if self.configuration["position"] == len(sequence) and len(self.configuration["inputStack"]) == 0:
                    self._success()
                elif self.configuration["inputStack"][-1] in self.nonTerminals:
                    self._expand()
                elif self.configuration["position"] < len(sequence):
                    if self.configuration["inputStack"][-1] == sequence[self.configuration["position"]]:
                        self._advance()
                    else:
                        self._momentaryInsuccess()
                else:
                    self._momentaryInsuccess()
            elif self.configuration["state"] == "b":
                if self.configuration["workingStack"][-1] in self.terminals:
                    self._back()
                else:
                    self._anotherTry()

        if self.configuration["state"] == "e":
            return "Error"

        return "Success"






