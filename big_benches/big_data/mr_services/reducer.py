import storage_cli as sc
import sys
key = sys.argv[1]
db = sc.jyd_db()
n = len(db.get(key))
with open('output.txt','w+') as f:
    f.write(key+','+str(n))
f.close()
