from Domain.Grammar import readGrammarFromFile

def printFAMenu():
    print("-----------------------------")
    print("For the loaded FA:")
    print("1. See the set of states")
    print("2. See the alphabet")
    print("3. See the final states")
    print("4. See the transitions")
    print("5. Check if a string is accepted")
    print("6. Check validity")
    print("7. Deterministic?")
    print("0. Exit")

def printGrammarMenu():
    print("-----------------------------")
    print("For the loaded grammar:")
    print("1. See non terminals")
    print("2. See terminals")
    print("3. See start non terminal")
    print("4. See productions")
    print("5. See productions for a given non terminal")
    print("6. CFG Check")
    print("7. Parse a sequence")
    print("0. Exit")

def main():
    '''
    tokenFile = "LanguageSpecs/token.in"

    identifierFile1 = "out/identifiers1.out"
    constantFile1 = "out/constants1.out"
    identifierFile1err = "out/identifiers1err.out"
    constantFile1err = "out/constants1err.out"
    identifierFile2 = "out/identifiers2.out"
    constantFile2 = "out/constants2.out"
    identifierFile3 = "out/identifiers3.out"
    constantFile3 = "out/constants3.out"
    pifFile1 = "out/pif1.out"
    pifFile2 = "out/pif2.out"
    pifFile3 = "out/pif3.out"
    pifFile1err = "out/pif1err.out"

    scanner1 = Scanner(tokenFile, identifierFile1, constantFile1, pifFile1)
    scanner1err = Scanner(tokenFile, identifierFile1err, constantFile1err, pifFile1err)
    scanner2 = Scanner(tokenFile, identifierFile2, constantFile2, pifFile2)
    scanner3 = Scanner(tokenFile, identifierFile3, constantFile3, pifFile3)

    scanner1.scan("ProgramExamples/p1.txt")
    scanner1err.scan("ProgramExamples/p3.txt")
    scanner2.scan("ProgramExamples/p1err.txt")
    scanner3.scan("ProgramExamples/p2.txt")
    '''

    '''
    FA = readFromFile("FA.json")
    while True:
        printFAMenu()
        command = str(input("Enter a command: ")).strip()
        if command == "0":
            break
        elif command == "1":
            print(FA.getStates())
        elif command == "2":
            print(FA.getAlphabet())
        elif command == "3":
            print(FA.getFinalStates())
        elif command == "4":
            result = FA.getTransitions()
            for sourceState in result:
                for transition in result[sourceState]:
                    print(sourceState + " -> " + transition['ToState'] + " if the symbol is " + str(transition['Label']))
        elif command == "5":
            sequence = input("Enter the desired sequence: ")
            print(FA.isAccepted(sequence))
        elif command == "6":
            message, result = FA.validate()
            print(message)
        elif command == "7":
            if FA.isDFA():
                print("Yes")
            else:
                print("No")
        else:
            print("Invalid command!")
    '''

    grammar = readGrammarFromFile("input/G1.json")
    while True:
        printGrammarMenu()
        command = str(input("Enter a command: ")).strip()
        if command == "0":
            break
        elif command == "1":
            print(grammar.nonTerminals)
        elif command == "2":
            print(grammar.terminals)
        elif command == "3":
            print(grammar.start)
        elif command == "4":
            for nonTerminal in grammar.productions:
                print(nonTerminal + " -> " + str(grammar.productions[nonTerminal]))
        elif command == "5":
            inputNonTerminal = str(input("Enter the desired non terminal:"))
            if inputNonTerminal not in grammar.productions:
                print("This non terminal is not in the grammar!")
                continue
            print(inputNonTerminal + " -> " + str(grammar.productions[inputNonTerminal]))
        elif command == "6":
            print(grammar.CFGCheck())
        elif command == "7":
            sequence = input("Enter the desired sequence: ")
            print(grammar.parse(sequence))
            print(grammar.configWorkingStack)
        else:
            print("Invalid command!")


main()
