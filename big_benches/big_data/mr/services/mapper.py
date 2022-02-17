#map fxn
import storage_cli as sc
db = sc.jyd_db()
f = open('input.txt','r')
f2 = open('output.txt','w+')
lines = f.readlines()
for line in lines:
    db.put([(line[:-1],str(1))])
f2.close()
f.close()
