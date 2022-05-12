from tinydb import TinyDB, Query
db = TinyDB('db.json')

#labels = "timestamp, vehicle_size, count, direction" 
#keys = labels.split(", ")
#key is timestamp, given file, each time is a row 
def put_in_db(infile):
    table = db.table('table_name')
    text_file = open(infile, "r+")
    labels = text_file.readline()
    keys = labels.split(", ")
    Lines = text_file.readlines()[1:]
    for line in Lines:
        dictionary ={}
        line = line.strip()
        words = line.split(",")
        for i in range(len(keys)):
            dictionary[keys[i]] = words[i]
        table.insert(dictionary)
    pass

def get_from_db(keys,outfile):
    outfile = open(outfile, "a")
    for key in keys:
        entry = Query()
        diction = db.get(entry.timestamp == key)
        for row in diction:
            outfile.write("%s, "%diction[row])
        outfile.write("\n")
    pass

#put_in_db("smallchunk.txt")
#keyarr = ["1582184843665", "1575368979316", "1583819489199"]
#get_from_db(keyarr, "chunk.txt")
