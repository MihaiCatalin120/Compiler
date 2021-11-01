from Scanner import Scanner


def main():
    tokenFile = "LanguageSpecs/token.in"
    identifierFile = "identifiers.out"
    constantFile = "constants.out"
    pifFile = "pif.out"
    scanner = Scanner(tokenFile, identifierFile, constantFile, pifFile)
    scanner.scan("ProgramExamples/p1.txt")
    scanner.scan("ProgramExamples/p1err.txt")
    scanner.scan("ProgramExamples/p2.txt")
    scanner.scan("ProgramExamples/p3.txt")


main()
