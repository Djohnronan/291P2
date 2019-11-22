import os

def main():

    files = ["emails.txt", "dates.txt", "terms.txt", "recs.txt"]

    sortFiles(files)
    makeIndexes(files)
    load()

def sortFiles(files):

    for f in files:
        if f == "recs.txt":
            print("Sorting file " + f + "...")
            os.system("sort -u -n <" + f + " -o " + f)   
        else:      
            print("Sorting file " + f + "...")     
            os.system("sort -u <" + f + " -o " + f)

def makeIndexes(files):

    index_files = {
        "emails.txt": "em.idx",
        "dates.txt": "da.idx",
        "terms.txt": "te.idx",
        "recs.txt": "re.idx"
    }
    
    for fname in files:
        f = open(fname, "r")
        i = open(index_files[fname],"w")
        print("Creating " + index_files[fname] + "...")
        for line in f:
            splitIndex = line.find(":")
            pair = [line[0:splitIndex], line[splitIndex + 1:]]
            i.write(pair[0].replace("\\", "") + "\n" + pair[1].replace("\\", ""))  
        f.close()
        i.close()

def load():
    os.system("db_load -T -f em.idx -t btree email.db")
    os.system("db_load -T -f da.idx -t btree date.db")
    os.system("db_load -T -f te.idx -t btree terms.db")
    os.system("db_load -T -f re.idx -t hash recs.db")
        
if __name__ == "__main__":
    main()