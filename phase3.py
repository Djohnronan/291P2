from bsddb3 import db
import re
import os

def main():
    
    output = "brief"
    keyWords = ["subj", "body", "from",  "to",  "cc", "bcc", "date"]
    run = True
    print("\n[output = " + output + "]\n")
    while run:
        rowIDs = []
        queries = []
        command = input("> ")
        command = command.lower()

        commandStrip = "".join(command.split())
        commandClean = re.split(r'[^-%/.@\w]+', command)

        if commandStrip == "output=full" or commandStrip == "output=brief":
            output = commandClean[1]
            os.system('clear')
            print("\n[output = " + output + "]\n")
            continue
        else:
            queries = getQueries(commandClean, commandStrip, keyWords)
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
    for record in recs:
        rowID = record[0].decode()
        email = record[1].decode()

        if output == "brief":
            subject = getField(email, 'subj')
            print("\nrow: " + rowID)
            print("subject: " + subject)

        else:
            date = getField(email, 'date')
            frm = getField(email, 'from')
            to = getField(email, 'to')
            subject = getField(email, 'subj')
            cc = getField(email, 'cc')
            bcc = getField(email, 'bcc')
            body = getField(email, 'body')
            print("\nrow: " + rowID)
            print("date: " + date)
            print("from: " + frm)
            print("to: " + to)
            print("subject: " + subject)
            print("cc: " + cc)
            print("bcc: ", bcc)
            print("body: " + body)



def getField(email, field):

    fieldTags = {
        "date": ["<date>" , "</date>"],
        "from": ["<from>" , "</from>"],
        "to": ["<to>" , "</to>"],
        "subj": ["<subj>" , "</subj>"],
        "cc": ["<cc>" , "</cc>"],
        "bcc": ["<bcc>" , "</bcc>"],
        "body": ["<body>" , "</body>"], 
    }

    startTag = fieldTags[field][0]
    endTag = fieldTags[field][1]
    s = email.find(startTag)
    if s!= -1:
        e = email.find(endTag)
        if (e-s) > len(startTag):
            field = email[s + len(startTag):e]
        else:
            field = "[EMPTY]"
    
    return field


def getRecs(masterList):
    DB_File = 'recs.db'
    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open(DB_File, None, db.DB_HASH, db.DB_CREATE)
    cursor = database.cursor()
    recs = []

    for rowID in masterList:
        result = cursor.set(str.encode(rowID))
        while result is not None:
            recs.append(result)
            result = cursor.next_dup()

    cursor.close()
    database.close()
    return recs


def executeQuery(query):
    operators = [':','<=','<','>=','>']
    prefix = ''
    suffix = ''
    op = ''
    for operator in operators:
        if query.find(operator) != -1:
            prefix, suffix = query.split(operator)
            op = operator
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
    DB_File = 'date.db'
    if operator == ":":
        rowIDs = set()
        database = db.DB()
        database.set_flags(db.DB_DUP)
        database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
        cursor = database.cursor()
        result = cursor.set(str.encode(date))
        while result is not None:
            result = result[1].decode()
            rowIDs.add(result)
            result = cursor.next_dup()
        cursor.close()
        database.close()
    elif operator == ">":
        rowIDs = gtRangeSearch(date, False, DB_File)
    elif operator == ">=":
        rowIDs = gtRangeSearch(date, True, DB_File)
    elif operator == "<":
        rowIDs = ltRangeSearch(date, False, DB_File)
    else: #operator == "<="
        rowIDs = ltRangeSearch(date, True, DB_File)

    return rowIDs

def gtRangeSearch(key, equal, DB_File):
    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
    cursor = database.cursor()
    rowIDs = set()

    result = cursor.set(str.encode(key))
    if not equal: 
        while result[0].decode() == key:
            result = cursor.next() # iterate through to the end of the database
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


def ltRangeSearch(key, equal, DB_File):
    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
    cursor = database.cursor()
    rowIDs = set()

    result = cursor.first()
    while True: # iterate through database until end condition is encountered
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
                elif result[0].decode().startswith(key): # check if term is part of the prefix
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
            rowIDs = equalitySearch(key, 'terms.db')

    cursor.close()
    database.close()
    
    return rowIDs

def equalitySearch(key, DB_File):
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
