
GENOME_LIST=["FNA", "GGA", "LAG", "VUR"]

import os
from glob import glob
import re


def parse_ssw(file_path):
    output = []
    with open(file_path) as f:
        data = f.read().split("\n")
        data = [a.split("\t") for a in data]
    for l in data:
        output.append((l[0], int(l[3])))
    return output

def parse_perf(file_path):
    output = []
    with open(file_path) as f:
        data = f.read().split("\n")
        data = [a.split("\t") for a in data]
        data = [a for a in data if len(a) > 1]
    for l in data:
        output.append((l[3], int(l[1])+1))
    return output

def parse_kmer(file_path):
    output = []
    with open(file_path) as f:
        data = f.read().split("\n")
        data = [a.split("\t") for a in data]
        data = [a for a in data if len(a) > 1]
        data = data[1:]
    for l in data:
        output.append((l[1], int(l[3])+1))
    return output

def parse_misa(file_path):
    output = []
    with open(file_path) as f:
        data = f.read().split("\n")
        data = data[5:]
        data = [a.split("\t") for a in data]
        data = [a for a in data if len(a)>1]
    for l in data:
        if l[2] == "microsatellite":
            search_res = re.findall("\([ACTG]+\)\d+", l[8])
            if len(search_res) > 0:
                seq = re.findall("[ACTG]+", search_res[0])
                output.append((seq[0], int(l[3])))
    return output

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
    final_accuracy_value = {a: {b: {} for b in GENOME_LIST} for a in software_list}

    # Measuring accuracy
    for genome in GENOME_LIST:
        chromosome_list = [os.path.basename(a).split(".")[0] for a in glob(f"../data/misa/misa-output/{genome}/*.tsv")]
        for chromosome in chromosome_list:
            print(f"Calculating accuracy value for {chromosome}")
            res={}
            res["ssw"] = parse_ssw(f"../data/ssw/ssw-output/{genome}/{chromosome}.tsv")
            res["perf"] = parse_perf(f"../data/perf/perf-output/{genome}/{chromosome}.tsv")
            res["kmer"] = parse_kmer(f"../data/kmer/kmer-output/{genome}/{chromosome}.tsv")
            res["misa"] = parse_misa(f"../data/misa/misa-output/{genome}/{chromosome}.tsv")

            for software in software_list:
                other_softwares = [s for s in software_list if s != software]
                others_list = []
                for _s in other_softwares:
                    for item in res[_s]:
                        others_list.append(item)

                total_count = len(res[software])
                exceptional_finding = 0
                for item in res[software]:
                    if item not in others_list:
                        exceptional_finding+=1
                exceptionnal_finding_rate = exceptional_finding/total_count
                final_accuracy_value[software][genome][chromosome] = (exceptionnal_finding_rate)
                continue
                exceptionnal_miss = 0
                for item in others_list:
                    if item not in res[software] and all([item in res[s] for s in other_softwares]):
                        exceptionnal_miss+= 1
                exceptionnal_miss_rate = exceptionnal_miss/total_count
                final_accuracy_value[software][genome][chromosome] = (exceptionnal_finding_rate, exceptionnal_miss_rate)

    tsv_data=[[[(a, b, c, (final_accuracy_value[a][b][c])) for c in final_accuracy_value[a][b]] for b in final_accuracy_value[a].keys()] for a in final_accuracy_value.keys()]
    final_output = [k for sub in tsv_data for j in sub for k in j]