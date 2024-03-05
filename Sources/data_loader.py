from random import randrange
import csv
import itertools

def fetch_data_idash():
    data = []
    with open('data/idash.txt') as f:
        for line in f:
            if not line.startswith('>'):
                data.append(line.rstrip())
    print("No. of genomes:", len(data))
    return data

def fetch_aligned_idash():
    ref = ''
    data = []
    genome_additions = []
    with open('data/idash_ref.csv') as f:
        for line in f:
            ref = str(''.join(line.rstrip().split(',')))
    with open('data/idash_referenced22.csv', newline='') as f:
        for line in f:
            data.append(str(''.join(line.rstrip().split(','))))
    print("No. of genomes:", len(data))
    with open('data/idash_referenced_adds22.csv', newline='') as f:
        reader = csv.reader(f)
        genome_additions = list(reader)
    genome_additions_colated = [list(item[1]) for item in itertools.groupby(genome_additions, key=lambda x: x[0])]
    genome_additions_colated = [set(tuple(x[1:-1]) for x in y) for y in genome_additions_colated]
    addition_indices = [set(x[-1] for x in y) for y in genome_additions_colated]
    return ref, data, genome_additions_colated, addition_indices

def extract_pairs(data):
    r1 = randrange(0,len(data))
    r2 = randrange(0,len(data))
    while r1 == r2:
        r2 = randrange(0,len(data))
    print("Selected #:", r1, r2)
    return data[r1], data[r2]