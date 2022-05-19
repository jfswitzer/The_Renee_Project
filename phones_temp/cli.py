import os
def get_bucket():
    return os.getenv('HOME')+'/bucket/'

def clear_bucket():
    os.system('rm -rf '+get_bucket()+'*')

clear_bucket()
