import os
with open('my_files.txt') as f:
    for line in f.readlines():
#        print('mv '+line[:-1]+' ~/bucket')
        os.system('mv '+line[:-1]+' ~/bucket')
