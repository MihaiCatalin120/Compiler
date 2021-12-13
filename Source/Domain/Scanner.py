from SymbolTable import SymbolTable
import re


class Scanner:
    def __init__(self, tokenFile, identifierFile, constantFile, pifFile):
        self._identifierTable = SymbolTable()
        self._constantTable = SymbolTable()
        self._tokens = []
        self._pif = []
        self.__readTokens(tokenFile)
        self._identifierFile = identifierFile
        self._constantFile = constantFile
        self._pifFile = pifFile
        self._NUMBERS_REGEX = "^[+-]?[1-9][0-9]+[^a-zA-Z]|0[^a-zA-Z]"
        self._CHAR_REGEX = "^\'([a-zA-Z]|\\n| |\.|!|\?|:|;|\||/|=|\+|\(|\)|&|\*|-|_|\[|]|{|}|<|>|\\t)\'"
        self._STRING_REGEX = "\"([a-zA-Z0-9]|\\n| |\.|!|\?|:|;|\||/|=|\+|\(|\)|&|\*|-|_|\[|]|{|}|<|>|\\t|\')*\""
        self._IDENTIFIER_REGEX = "^[A-Za-z][A-Za-z0-9_]*"
        self._RESERVED_WORD_REGEX = "^var|int|read|if|write|else|while|for|char|array|do|bool|float|and|or|of"
        self._SEPARATOR_REGEX = "^(\\n)(\\t)|\[|\]|[{};:\s]|\(|\)"
        self._OPERATOR_REGEX = "^\+|-|\*|/|<|>|<=|==|>=|=|!=|\+\+"

    def __readTokens(self, file):
        f = open(file, "r")
        lines = f.readlines()

        for line in lines:
            self._tokens.append(line.strip())
        f.close()

    def __addIfReservedWord(self, s):
        isReservedWord = re.compile(self._RESERVED_WORD_REGEX)
        matchReservedWord = isReservedWord.match(s)
        if matchReservedWord:
            self._pif.append((matchReservedWord.group(), -1))
            s = s[matchReservedWord.end():]
            return s, True
        else:
            return s, False

    def __addIfSeparator(self, s):
        isSeparator = re.compile(self._SEPARATOR_REGEX)
        matchSeparator = isSeparator.match(s)
        if matchSeparator:
            self._pif.append((matchSeparator.group(), -1))
            s = s[matchSeparator.end():]
            return s, True
        else:
            return s, False

    def __addIfOperator(self, s):
        isOperator = re.compile(self._OPERATOR_REGEX)
        matchOperator = isOperator.match(s)
        if matchOperator:
            self._pif.append((matchOperator.group(), -1))
            s = s[matchOperator.end():]
            return s, True
        else:
            return s, False
        
    def __addIfIdentifier(self, s):
        isIdentifier = re.compile(self._IDENTIFIER_REGEX)
        matchIdentifier = isIdentifier.match(s)
        if matchIdentifier:
            token = matchIdentifier.group()
            self._identifierTable.addEntry(token)
            self._pif.append(("identifier", self._identifierTable.find(token)))
            s = s[matchIdentifier.end():]
            return s, True
        else:
            return s, False
        
    def __addIfDigitConstant(self, s):
        isConstant = re.compile(self._NUMBERS_REGEX)
        matchConstant = isConstant.match(s)
        if matchConstant:
            token = matchConstant.group()
            self._constantTable.addEntry(token)
            self._pif.append(("constant", self._constantTable.find(token)))
            s = s[matchConstant.end():]
            return s, True
        else:
            return s, False

    def __addIfCharConstant(self, s):
        isConstant = re.compile(self._CHAR_REGEX)
        matchConstant = isConstant.match(s)
        if matchConstant:
            token = matchConstant.group()
            self._constantTable.addEntry(token)
            self._pif.append(("constant", self._constantTable.find(token)))
            s = s[matchConstant.end():]
            return s, True
        else:
            return s, False

    def __addIfStringConstant(self, s):
        isConstant = re.compile(self._STRING_REGEX)
        matchConstant = isConstant.match(s)
        if matchConstant:
            token = matchConstant.group()
            self._constantTable.addEntry(token)
            self._pif.append(("constant", self._constantTable.find(token)))
            s = s[matchConstant.end():]
            return s, True
        else:
            return s, False

    def __writePIF(self):
        f = open(self._pifFile, "w")
        for entry in self._pif:
            f.write(str(entry[0]) + " -> " + str(entry[1]) + "\n")
        f.close()

    def __writeIdentifiers(self):
        f = open(self._identifierFile, "w")
        for key, value in self._identifierTable.getContent():
            f.write(str(key) + " -> " + str(value) + "\n")
        f.close()

    def __writeConstants(self):
        f = open(self._constantFile, "w")
        for key, value in self._constantTable.getContent():
            f.write(str(key) + " -> " + str(value) + "\n")
        f.close()

    def scan(self, filePath):
        valid = True
        lineNumber = 1
        f = open(filePath, "r")
        lines = f.readlines()

        for line in lines:
            if line[:2] == "//" or line == '\n':
                lineNumber += 1
                continue
            line.strip(' ')
            while len(line) > 0:
                line = line.strip()

                line, result = self.__addIfReservedWord(line)
                if result:
                    continue

                line, result = self.__addIfSeparator(line)
                if result:
                    continue

                line, result = self.__addIfOperator(line)
                if result:
                    continue

                line, result = self.__addIfIdentifier(line)
                if result:
                    continue

                line, result = self.__addIfDigitConstant(line)
                if result:
                    continue

                line, result = self.__addIfStringConstant(line)
                if result:
                    continue

                line, result = self.__addIfCharConstant(line)
                if result:
                    continue

                print("Error on line: " + str(lineNumber) + " in program " + filePath + "!")
                valid = False
                break
            lineNumber += 1

        if valid:
            print("Program " + filePath + " is valid!")
            self.__writePIF()
            self.__writeIdentifiers()
            self.__writeConstants()









