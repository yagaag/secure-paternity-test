from data_loader import *
from sequence_aligner import *
from edit_dist import edit_distance_D

def align_idash(data):
    ref = ''
    with open('data/idash_ref.csv') as f:
        for line in f:
            ref = str(''.join(line.rstrip().split(',')))
    
    aligned_genomes = []
    genome_additions = []
    genome_additions2 = []

    for i in range(len(data)):
        v, D = edit_distance_D(ref, data[i])
        ref2, val = sequence_aligner(ref, data[i], D)
        aligned = ''
        adds = []
        prev_idx = -1
        for j in range(len(ref2)):
            if ref2[j] != '_':
                aligned+=val[j]
            else:
                idx = j-len(adds)
                # print(idx, prev_idx)
                if idx <= prev_idx:
                    idx = round(prev_idx+0.001,3)
                adds.append([val[j], idx, j])
                genome_additions2.append([i, val[j], idx, j])
                prev_idx = idx
        aligned_genomes.append(aligned)
        genome_additions.append(adds)
        print("Completed:", i+1)

    with open('data/idash_referenced.txt', 'w') as f:
        for i in range(len(data)):
            f.write(">" + str(i) + '\n')
            f.write(aligned_genomes[i] + '\n')
            f.write(str(genome_additions[i]) + '\n')

    with open('data/idash_referenced.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows(aligned_genomes)

    with open('data/idash_referenced_adds.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows(genome_additions2)


data = fetch_data_idash()
align_idash(data)