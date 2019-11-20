import os.path
import re

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

    special_chars = ['&lt;', '&gt;', '&amp;', '&apos;', '&quot']
    replace = ['<', '>', '&', "'", '"']
    for line in flines:
        rowID = getRow(line)
        if rowID != -1:
            getRecs(line, recs, rowID)
            i = 0
            newLine = line
            for char in special_chars:
                newLine = newLine.replace(char, replace[i])
                i += 1

            getTerms(newLine, terms, rowID)
            getEmails(newLine, emails, rowID)
            getDates(newLine, dates, rowID)
        
    f.close()
    terms.close()
    emails.close()
    dates.close()
    recs.close()

def getTerms(line, terms, rowID):
    s_startTag = "<subj>"
    s_endTag = "</subj>"
    s = line.find(s_startTag)
    if s != -1:
        e = line.find(s_endTag)
        if (e-s) > len(s_startTag):
            subjTerms = filter(None, re.split(r'[^-\w]+', line[s + len(s_startTag):e]))
            for term in subjTerms:
                if len(term) > 2:
                    terms.write("s-" + term.lower() + ":" + rowID + "\n")

    b_startTag = "<body>"
    b_endTag = "</body>"
    b = line.find(b_startTag)
    if b != -1:
        e = line.find(b_endTag)
        if (e-b) > len(b_startTag):
            bodyTerms = filter(None, re.split(r'[^-\w]+', line[b + len(b_startTag):e]))
            for term in bodyTerms:
                if len(term) > 2:
                    terms.write("b-" + term.lower() + ":" + rowID + "\n")

def getEmails(line, emails, rowID):
    f_startTag = "<from>"
    f_endTag = "</from>"
    s = line.find(f_startTag)
    if s != -1:
        e = line.find(f_endTag)
        if (e-s) > len(f_startTag):
            emailList = line[s + len(f_startTag):e].split(',')
            for email in emailList:
                emails.write('from-' + email.lower() + ":" + rowID + "\n")

    t_startTag = "<to>"
    t_endTag = "</to>"
    s = line.find(t_startTag)
    if s != -1:
        e = line.find(t_endTag)
        if (e-s) > len(t_startTag):
            emailList = line[s + len(t_startTag):e].split(',')
            for email in emailList:
                emails.write('to-' + email.lower() + ":" + rowID + "\n")

    c_startTag = "<cc>"
    c_endTag = "</cc>"
    s = line.find(c_startTag)
    if s != -1:
        e = line.find(c_endTag)
        if (e-s) > len(c_startTag):
            emailList = line[s + len(c_startTag):e].split(',')
            for email in emailList:
                emails.write('cc-' + email.lower() + ":" + rowID + "\n")

    b_startTag = "<bcc>"
    b_endTag = "</bcc>"
    s = line.find(b_startTag)
    if s != -1:
        e = line.find(b_endTag)
        if (e-s) > len(b_startTag):
            emailList = line[s + len(b_startTag):e].split(',')
            for email in emailList:
                emails.write('bcc-' + email.lower() + ":" + rowID + "\n")

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