import os.path

def main():
    
    valid_fname = False
    while not valid_fname:
        fname = input("Enter .xml file name: ")
        if not os.path.exists(fname) or not fname.endswith(".xml"):
            print("\n" +fname + " not found or invalid extension type. Please enter a valid .xml file.\n")
        else:
            valid_fname = True
    f = open(fname, "r")
    flines = f.readlines()

    datafiles = ["terms", "emails", "dates", "recs"]
    for dfile in datafiles:
        if os.path.exists(dfile + ".txt"):
            print(dfile + ".txt already exists. Overwriting data...")

    terms = open("terms.txt", "w")
    emails = open("emails.txt", "w")
    dates = open("dates.txt", "w")
    recs = open("recs.txt", "w")

    for line in flines:
        rowID = getRow(line)
        if rowID != -1:
            getTerms(line, terms, rowID)
            getEmails(line, emails, rowID)
            getDates(line, dates, rowID)
            getRecs(line, recs, rowID)
        
    f.close()
    terms.close()
    emails.close()
    dates.close()
    recs.close()

def getTerms(line, terms, rowID):
    pass

def getEmails(line, emails, rowID):
    f_startTag = "<from>"
    f_endTag = "</from>"
    s = line.find(f_startTag)
    if s != -1:
        e = line.find(f_endTag)
        if (e-s) > len(f_startTag):
            email = line[s + len(f_startTag):e].lower()
            emails.write('from-' + email + ":" + rowID + "\n")

    t_startTag = "<to>"
    t_endTag = "</to>"
    s = line.find(t_startTag)
    if s != -1:
        e = line.find(t_endTag)
        if (e-s) > len(t_startTag):
            email = line[s + len(t_startTag):e].lower()
            emails.write('to-' + email + ":" + rowID + "\n")

    c_startTag = "<cc>"
    c_endTag = "</cc>"
    s = line.find(c_startTag)
    if s != -1:
        e = line.find(c_endTag)
        if (e-s) > len(c_startTag):
            email = line[s + len(c_startTag):e].lower()
            emails.write('cc-' + email + ":" + rowID + "\n")

    b_startTag = "<bcc>"
    b_endTag = "</bcc>"
    s = line.find(b_startTag)
    if s != -1:
        e = line.find(b_endTag)
        if (e-s) > len(b_startTag):
            email = line[s + len(b_startTag):e].lower()
            emails.write('bcc-' + email + ":" + rowID + "\n")

def getDates(line, dates, rowID):
    startTag = "<date>"
    endTag = "</date>"
    s = line.find(startTag)
    if s != -1:
        e = line.find(endTag)
        date = line[s + len(startTag):e]
        dates.write(date + ':' + rowID + '\n')
    return

def getRecs(line, recs, rowID):
    recs.write(rowID + ":" + line)
    return

def getRow(line):
    startTag = "<row>"
    endTag = "</row>"
    s = line.find(startTag)
    if s != -1:
        e = line.find(endTag)
        return line[s+len(startTag):e]
    else:
        return -1

if __name__ == "__main__":
    main()