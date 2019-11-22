from bsddb3 import db
import re

def main():
    
    output = "full"
    keyWords = ["subj", "body", "from",  "to",  "cc", "bcc", "date"]
    run = True

    while run:
        queries = []
        command = input("> ")
        command = command.lower()

        commandStrip = "".join(command.split())
        commandClean = re.split(r'[^-%/\w]+', command)

        if command == "output=full" or command == "output=brief":
            output = commandStrip[1]
        else:
            queries = getQueries(commandClean, commandStrip, keyWords)


def getQueries(commandClean, commandStrip, keyWords):

    queries = []
    added = []

    for i in range(len(commandClean)):
        if commandClean[i] in keyWords:
            prefix = commandClean[i]
            operator = commandStrip[commandStrip.find(commandClean[i]) + len(prefix)]
            data = commandClean[i+1]
            queries.append(prefix+operator+data)
            added.append(commandClean[i])
            added.append(commandClean[i+1])

    for term in commandClean:
        if term not in added:
            queries.append(term)
    
    return queries

if __name__ == "__main__":
    main()