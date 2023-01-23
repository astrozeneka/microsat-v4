
import os
from glob import glob

GENOME_LIST=["FNA", "GGA", "LAG", "VUR"]
software_list = [os.path.basename(a).split(".")[0] for a in glob("../data/*")]

if __name__ == '__main__':
    for software in software_list:
        with open(f"../data/{software}/{software}-log.txt") as f:
            log = f.read().split("\n")
            log = [a.split(" ") for a in log]
            log = [a for a in log if len(a) > 1]

        print()