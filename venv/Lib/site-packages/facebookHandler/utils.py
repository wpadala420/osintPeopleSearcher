""" a file with a bunch of utility functions """


def getStringBetween(inString : str, startString : str, endString : str) -> str:
    indexFrom = inString.find(startString)+len(startString)
    indexTo = inString.find(endString, indexFrom)
    return inString[indexFrom:indexTo]	