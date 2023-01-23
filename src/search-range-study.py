
import os
from glob import glob
import itertools
import re
from Bio.Seq import Seq

software_list=[os.path.basename(d) for d in glob("../data/*")]
genome_list = ["FNA", "GGA", "LAG", "VUR"]

def get_motif_standard(motif):
    options = []
    for i in range(len(motif)):
        ex = motif[i:] + motif[:i]
        options.append(ex)
        options.append(Seq(ex).complement())
    def cost(motif):
        output = 0
        for i in range(len(motif)):
            output += 2**(len(motif)-i-1) * "ACTGN".index(motif[i])
        return (motif, output)
    cost_list = [cost(m) for m in options]
    standard = min(cost_list)[0]
    return standard


# This is to study the search range of each algorithm
# This has been performed two by two
# This accuracy criteria hasn't been yet mentioned in any paper (I've read till now)
# It can POSSIBLY
# For the graphical representationl, only Two by two, or Three by Three can be done
# Four by four is not possible
# To be executed in a computer (for study and experimentation — not for production)
#  For production mode (for further studies and researches), a server (or Lab Supercomputer) can be used

# Genome by genome WITH summary
software_couples = list(itertools.combinations(software_list, 2))


def parse_ssw(file_path):
    output = []
    with open(file_path) as f:
        data = f.read().split("\n")
        data = [a.split("\t") for a in data]
    for l in data:
        if(len(data) >= 4):
            output.append((get_motif_standard(l[0]), int(l[3])))
    return output
def parse_perf(file_path):
    output = []
    with open(file_path) as f:
        data = f.read().split("\n")
        data = [a.split("\t") for a in data]
        data = [a for a in data if len(a) > 1]
    for l in data:
        output.append((get_motif_standard(l[3]), int(l[1])+1))
    return output
def parse_kmer(file_path):
    output = []
    with open(file_path) as f:
        data = f.read().split("\n")
        data = [a.split("\t") for a in data]
        data = [a for a in data if len(a) > 1]
        data = data[1:]
    for l in data:
        output.append((get_motif_standard(l[1]), int(l[3])+1))
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
                output.append((get_motif_standard(seq[0]), int(l[3])))
    return output

parse_func = {}
parse_func["ssw"] = parse_ssw
parse_func["perf"] = parse_perf
parse_func["kmer"] = parse_kmer
parse_func["misa"] = parse_misa

if __name__ == '__main__':
    output = [("SoftwareA", "SoftwareB", "Genome", "Chromosome", "Union", "Inter", "AOnly", "BOnly")]
    for software_a, software_b in software_couples:
        print()
        for genome in genome_list:
            chromosome_list = [os.path.basename(a).split(".")[0] for a in glob(f"../data/{software_a}/{software_a}-output/{genome}/*")]
            for chromosome in chromosome_list:
                print(f"Analyze {chromosome}")
                res_a = parse_func[software_a](f"../data/{software_a}/{software_a}-output/{genome}/{chromosome}.tsv")
                res_b = parse_func[software_b](f"../data/{software_b}/{software_b}-output/{genome}/{chromosome}.tsv")
                union = list(set(res_a + res_b))
                inter = list(set(res_a) & set(res_b))

                union_len=len(union)
                inter_len=len(inter)
                a_only=len(res_a)-inter_len
                b_only=len(res_b)-inter_len
                output.append((software_a, software_b, genome, chromosome, union_len, inter_len, a_only, b_only))

    tsv = "\n".join(["\t".join([str(b) for b in a]) for a in output])
    with open("../data/search-range-study.tsv", "w") as f:
        f.write(tsv)
