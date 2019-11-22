from bsddb3 import db
import re

def main():

    keyWords = ["subj", "body", "from",  "to",  "cc", "bcc", "date"]

    command = input("> ")

    commandStrip  ="".join(command.split())
    commandClean = re.split(r'[^-%/\w]+', command)

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
  
            


    
if __name__ == "__main__":
    main()