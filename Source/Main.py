from domain.SymbolTable import SymbolTable


def main():
    table = SymbolTable()

    tokens = [
        "a",
        "b",
        "c",
        "\"Name\"",
        "\'f\'",
        "1234",
        "-22",
        "d"
    ]

    for token in tokens:
        table.addEntry(token)

    for token in tokens:
        print("Token " + token + " stored at index " + str(table.find(token)))


main()
