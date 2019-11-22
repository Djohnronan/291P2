import os

def main():

    files = ["emails.txt", "dates.txt", "terms.txt", "recs.txt"]
    sortFiles(files)
    makeIndexes(files)

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
            pair = line.split(':')
            i.write(pair[0] + "\n" + pair[1])
            
                
if __name__ == "__main__":
    main()