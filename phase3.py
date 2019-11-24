from bsddb3 import db
import re

def main():
    
    output = "brief"
    keyWords = ["subj", "body", "from",  "to",  "cc", "bcc", "date"]
    run = True

    while run:
        rowIDs = []
        queries = []
        command = input("> ")
        command = command.lower()

        commandStrip = "".join(command.split())
        commandClean = re.split(r'[^-%/.@\w]+', command)

        if command == "output=full" or command == "output=brief":
            output = commandStrip[1]
        else:
            queries = getQueries(commandClean, commandStrip, keyWords)
            # print(queries)
            for query in queries:
                rowIDs.append(executeQuery(query))

        masterSet = rowIDs[0]
        for i in range(1, len(rowIDs)):
            masterSet.intersection(rowIDs[i])
        masterList = list(masterSet)
        masterList.sort()
        # masterList contains (in order) the intersection of all query rowIDs
        recs = getRecs(masterList)
        displayRecs(recs, output)


def displayRecs(recs, output):
    
    rowID = recs[0].decode()
    rec = recs[1].decode()

    if output == "brief":

        s_startTag = "<subj>"
        s_endTag = "</subj>"
        s = rec.find(s_startTag)
        if s != -1:
            e = rec.find(s_endTag)
            if (e-s) > len(s_startTag):
                subject = rec[s + len(s_startTag):e]
        print(rowID, subject)

    else:
        pass


def getRecs(masterList):
    DB_FILE = 'recs.db'
    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open(DB_FILE, None, db.DB_HASH, db.DB_CREATE)
    cursor = database.cursor()

    for rowID in masterList:
        rec = cursor.set(str.encode(rowID))
    
    return rec


def executeQuery(query):
    operators = [':','<=','<','>=','>']
    prefix = ''
    suffix = ''
    op = ''
    for operator in operators:
        if query.find(operator) != -1:
            prefix, suffix = query.split(operator)
            op = operator
            # print(op)
            break
    if op != '':
        emailPrefix = ['to', 'from', 'cc', 'bcc']
        if prefix in emailPrefix:
            rowIDs = emailQuery(prefix, suffix)
        elif prefix == 'date':
            rowIDs = dateQuery(suffix, op)
        else:
            rowIDs = termQuery(prefix = prefix, term = suffix)
    else:
        rowIDs = termQuery(prefix = None, term = query)
    return rowIDs


def emailQuery(prefix, email):
    key = prefix + '-' + email
    DB_File = 'email.db'
    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
    cursor = database.cursor()
    rowIDs = set()

    result = cursor.set(str.encode(key))
    while result is not None:
        result = result[1].decode()
        rowIDs.add(result)
        result = cursor.next_dup()
    cursor.close()
    database.close()
    return rowIDs

def dateQuery(date, operator):
    rowIDs = set()
    DB_FILE = 'date.db'
    if operator == ":":
        database = db.DB()
        database.set_flags(db.DB_DUP)
        database.open(DB_FILE, None, db.DB_BTREE, db.DB_CREATE)
        cursor = database.cursor()
        result = cursor.set(str.encode(date))
        while result is not None:
            result = result[1].decode()
            rowIDs.add(result)
            result = cursor.next_dup()
        cursor.close()
        database.close()
    elif operator == ">":
        rowIDs = gtRangeSearch(date, False, DB_FILE)
    elif operator == ">=":
        rowIDs = gtRangeSearch(date, True, DB_FILE)
    elif operator == "<":
        rowIDs = ltRangeSearch(date, False, DB_FILE)
    else: #operator == "<="
        rowIDs = ltRangeSearch(date, True, DB_FILE)

    return rowIDs

def gtRangeSearch(key, equal, dbName):
    DB_File = dbName
    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
    cursor = database.cursor()
    rowIDs = set()

    result = cursor.set(str.encode(key))
    if not equal:
        while result[0].decode() == key:
            result = cursor.next()
    while result is not None:
        while result is not None:
            print(result[0].decode())
            result = result[1].decode()
            rowIDs.add(result)
            result = cursor.next_dup()
        result = cursor.next()
    
    cursor.close()
    database.close()

    return rowIDs


def ltRangeSearch(key, equal, dbName):
    DB_File = dbName
    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
    cursor = database.cursor()
    rowIDs = set()

    result = cursor.first()
    while True:
        if equal:
            if result[0].decode() > key:
                break
        else:
            if result[0].decode() >= key:
                break
        while result is not None:
            result = result[1].decode()
            rowIDs.add(result)
            result = cursor.next_dup()
        result = cursor.next()
    
    cursor.close()
    database.close()

    return rowIDs


def termQuery(prefix, term):
    DB_File = 'terms.db'
    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
    cursor = database.cursor()
    rowIDs = set()
    prefixes = []
    wildcard = False
    if term.find("%") > -1:
        term = term.replace("%", "")
        wildcard = True
    if prefix is not None:
        prefixes.append(prefix[0])
    else:
        prefixes = ['s', 'b']

    for pfix in prefixes:
        key = pfix + '-' + term
        if wildcard:
            result = cursor.first()
            foundAll = False
            foundFirst = False
            while not foundAll:
                if result == None:
                    foundAll = True
                elif result[0].decode().startswith(key):
                    if not foundFirst:
                        foundFirst = True
                    while result is not None:
                        result = result[1].decode()
                        rowIDs.add(result)
                        result = cursor.next_dup()
                elif foundFirst: # we passed the interval of where the prefix is in the string
                    foundAll = True
                result = cursor.next()
        else:
            result = cursor.set(str.encode(key))
            while result is not None:
                result = result[1].decode()
                rowIDs.add(result)
                result = cursor.next_dup()

    cursor.close()
    database.close()
    
    return rowIDs
    

def getQueries(commandClean, commandStrip, keyWords):

    queries = []
    added = []

    for i in range(len(commandClean)):
        if commandClean[i] in keyWords:
            prefix = commandClean[i]
            operator = commandStrip[commandStrip.find(commandClean[i]) + len(prefix)]
            if commandStrip.find("=") != -1:
                operator+= "="
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
