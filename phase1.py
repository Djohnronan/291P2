import os.path

def main():
    
    fname = input("Enter .xml file name: ")
    f = open(fname, "r")
    flines = f.readlines()

    for line in flines:
        terms = open("terms.txt", "a+")
        getTerms(line, terms)

        emails = open("emails.txt", "a+")
        getEmails(line, emails)

        dates = open("dates.txt", "a+")
        getDates(line, dates)

        recs = open("recs.txt", "a+")
        getRecs(line, recs)
        
    f.close()
    terms.close()
    emails.close()
    dates.close()
    recs.close()

def getTerms(line, terms):
    pass

def getEmails(line, emails):
    pass

def getDates(line, dates):
    rowID = getRow(line)
    startTag = "<date>"
    endTag = "</date>"
    s = line.find(startTag)
    if s != -1:
        e = line.find(endTag)
        date = line[s+len(startTag):e]
        dates.write(date+':'+rowID+'\n')
    return

def getRecs(line, recs):
    pass

def getRow(line):
    startTag = "<row>"
    endTag = "</row>"
    s = line.find(startTag)
    if s != -1:
        e = line.find(endTag)
        return line[s+len(startTag):e]
    

if __name__ == "__main__":
    main()