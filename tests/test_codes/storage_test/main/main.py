import cli
directory = cli.get_bucket()
with open(directory+'test.txt','w+') as f:
    f.write('Test write')

