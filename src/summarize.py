
GENOME_LIST=["FNA", "GGA", "LAG", "VUR"]

import os
from glob import glob

if __name__ == '__main__':
    # Get those Tree Evaluation Critera
    # 1. Time complexity (how much time it takes)
    # 2. Space complexity (how much memory it uses)
    # 3. Accuracy : Is the result similar or different to the other
    #   * 4 softwares are used here
    #   Calculation is as follow
    #   Given an algorithm
    #   If all of its value are in the Three other, its accuracy will be 1
    #   If have value that are not in the three others, its accuracy decrease
    #   Percentage of its items which are included in the three other [REF!!!]

    # software_list
    software_list = [os.path.basename(a).split(".")[0] for a in glob("../data/*")]

    software = "ssw"
    print()