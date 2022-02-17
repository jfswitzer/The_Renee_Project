import os
with open('my_files.txt') as f:
    for line in f.readlines():
        os.system('mv '+'~/bucket/'+line[:-1]+' .')
