import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import glob
import os
import sys

def main():
    #caiso
    li = []
    path = "caiso_2019"
    all_files = glob.glob(os.path.join(path, "*2019*.csv"))
    for filename in all_files:
        with open(filename) as csvfile:
            df = csv.DictReader(csvfile)
            lmps = []
            for row in df:
                if row["LMP_TYPE"]=="LMP":
                    lmps.append(float(row["VALUE"]))
            print(filename)
            print(sum(lmps)/len(lmps))        
if __name__ == "__main__":
    main()

