
class SymbolTable:
    def __init__(self, capacity=211, loadFactor=0.8):
        self._capacity = capacity
        self._loadFactor = loadFactor
        self._map = self.__initMap()
        self._size = 0

    def __initMap(self):
        newMap = {}
        for i in range(0, self._capacity):
            newMap[i] = []
        return newMap

    def __resizeIfCapacityExceeded(self):
        if float(self._size) / self._capacity > self._loadFactor:
            oldMap = self._map
            self._capacity *= 2
            self._map = self.__initMap()
            for key, value in oldMap:
                for token in value:
                    self.addEntry(token)

    def addEntry(self, token):
        index1, index2 = self.find(token)
        if index1 != -1 and index2 != -1:
            return index1, index2
        self.__resizeIfCapacityExceeded()
        self._size += 1
        key = self.__hash(token)
        self._map[key].append(token)
        return key, self._map[key].index(token)

    def find(self, token):
        key = self.__hash(token)
        try:
            return key, self._map[key].index(token)
        except:
            return -1, -1

    def __hash(self, token: str):
        return token.__hash__() % self._capacity

    def getContent(self):
        result = []
        for key in self._map:
            for item in self._map[key]:
                result.append((key, item))
        return result
