import json


def readFromFile(filename):
    FAinput = json.load(open(filename, "r"))
    return FiniteAutomata(FAinput["States"], FAinput["Alphabet"], FAinput["InitialState"], FAinput["FinalStates"], FAinput["Transitions"])


def removeDuplicates(inputList):
    return list(dict.fromkeys(inputList))


class FiniteAutomata:
    def __init__(self, states, alphabet, initialState, finalStates, transitions):
        self._states = states
        self._alphabet = alphabet
        self._initialState = initialState
        self._finalStates = finalStates
        self._transitions = transitions

    def __str__(self):
        result = "Q: " + str(self._states)
        result += "\nΣ: " + str(self._alphabet)
        result += "\nq0: " + str(self._initialState)
        result += "\nF: " + str(self._finalStates)
        result += "\nδ: " + str(self._transitions)
        return result

    def getStates(self):
        return self._states

    def getAlphabet(self):
        return self._alphabet

    def getInitialState(self):
        return self._initialState

    def getFinalStates(self):
        return self._finalStates

    def getTransitions(self):
        return self._transitions

    def __getTransitionsOfState(self, state):
        return self._transitions[state]

    def validate(self):
        if self._initialState not in self._states:
            return "Initial state is not in the list of states!", False

        for finalState in self._finalStates:
            if finalState not in self._states:
                return "Final state is not in the list of states!", False

        for sourceState in self._transitions:
            if sourceState not in self._states:
                return "Source state of the transition is not in the list of states!", False
            for transition in self._transitions[sourceState]:
                if transition['ToState'] not in self._states:
                    return "Destination state of the transition is not in the list of states!", False
                if transition['Label'] not in self._alphabet:
                    return "Symbol not found in the alphabet!", False

        return "Valid", True

    def isDFA(self):
        for sourceState in self._transitions:
            labelTracker = {}
            for symbol in self._alphabet:
                labelTracker[symbol] = []
            for transition in self._transitions[sourceState]:
                labelTracker[transition['Label']].append(transition['ToState'])
            for symbol in labelTracker:
                labelTracker[symbol] = removeDuplicates(labelTracker[symbol])
            maxLen = 0
            for symbol in labelTracker:
                maxLen = max(maxLen, len(labelTracker[symbol]))
            if maxLen > 1:
                return False
        return True

    def isAccepted(self, sequence: str):
        if not self.isDFA():
            return False
        message, validateResult = self.validate()
        if not validateResult:
            print(message)
            return False
        currentState = self._initialState
        for symbol in sequence:
            validTransitions = self.__getTransitionsOfState(currentState)
            found = False
            for transition in validTransitions:
                if str(transition['Label']) == symbol:
                    found = True
                    currentState = transition['ToState']
            if not found:
                return False

        return currentState in self._finalStates


