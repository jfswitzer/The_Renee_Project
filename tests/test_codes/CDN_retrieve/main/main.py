import cli
directory = cli.get_bucket()
with open(directory+'test.txt','r+') as f:
    for line in f:
            print(line) 
