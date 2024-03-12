import pandas as pd
import os
import csv
import re

def process_sections(reference_genome, chr_id):
    
    section_filename = 'data/ref/sections/' + reference_genome + '_chr' + str(chr_id) + '.csv'
   
    # Check if done already
    if os.path.isfile(section_filename):
        print('File exists; Using it')
        with open(section_filename, newline='') as f:
            reader = csv.reader(f)
            sections = list(reader)
        return [[int(x) for x in y] for y in sections]
        
    chr_ct = 0
    sections = []
    ref_filename = 'data/ref/' + reference_genome + '_chr' + str(chr_id) + '.fa'
    if not os.path.isfile(ref_filename):
        print('No such reference file!')
        return []
    with open(ref_filename) as f:
        section_started = False
        section_start, section_end = 0, 0
        for line in f:
            test = re.split('N+', line.rstrip())
            if not section_started and test[-1] != '':
                section_start = chr_ct + 50-len(test[-1])
                section_started = True
            if section_started and test[-1] == '':
                section_end = chr_ct + len(test[0])
                sections.append([section_start, section_end])
                section_started = False
            chr_ct+=50

    # Write for future use
    with open(section_filename, 'w') as f:
        write = csv.writer(f)
        write.writerows(sections)

    return sections

def section_wise_edits(vcf_reader, sections, chr_id):
        '''Finds edits for each section'''
        
        all_pos = []
        all_ref = []
        all_alt = []
        pos, ref, alt = [], [], []
        section_idx = 0
        for i, dc in enumerate(vcf_reader):
            for cr, p, r, a in zip(dc['#CHROM'], dc['POS'], dc['REF'], dc['ALT']):
                if cr != 'chr'+str(chr_id):
                    all_pos.append(pos)
                    all_ref.append(ref)
                    all_alt.append(alt)
                    section_edit_ct = [len(a) for a in all_pos]
                    print("Section-wise edit count:", section_edit_ct)
                    print("Total edits for chromosome", chr_id, 'is', sum(section_edit_ct))
                    return all_pos, all_ref, all_alt
                if int(p) > sections[section_idx][1]:
                    all_pos.append(pos)
                    all_ref.append(ref)
                    all_alt.append(alt)
                    pos, ref, alt = [], [], []
                    section_idx+=1
                pos.append(int(p))
                ref.append(r)
                alt.append(a)
            if i == 3000:
                print("Too many reads; Breaking..")
                break
        
        all_pos.append(pos)
        all_ref.append(ref)
        all_alt.append(alt)
        section_edit_ct = [len(a) for a in all_pos]
        print("Section-wise edit count:", section_edit_ct)
        print("Total edits for chromosome", chr_id, 'is', sum(section_edit_ct))
        return all_pos, all_ref, all_alt

def fetch_ref_subsequences(ref_filename, sections, seq_len, ct):
    chr_ct = 0
    section_id = 0
    section_wise_references = []
    data = []
    current = ''
    sec_start, sec_end = sections[section_id][0], sections[section_id][1]
    with open(ref_filename) as f:
        for line in f:
            if chr_ct+50 >= sec_start and chr_ct <= sec_end:
                l = line.rstrip()
                start_char = max(sec_start - chr_ct, 0)
                end_char = min(sec_end - chr_ct, 50)
                current += l[start_char:end_char].capitalize()
                if len(current) >= seq_len:
                    data.append(current[:seq_len])
                    if len(data) == ct:
                        break
                    current = current[seq_len:]
                if chr_ct+50 >= sec_end:
                    print("Crossed section:", section_id)
                    section_id+=1
                    sec_start, sec_end = sections[section_id][0], sections[section_id][1]
            chr_ct+=50
    return data

# def apply_edits(ref, )

def fetch_subsequences(filename, chr_id, seq_len, ct):

    vcf_names = []
    start_row = 0
    reference_genome = ''
    with open(filename, "rt") as f:
        for line in f:
            if line.startswith('##reference'):
                reference_genome = line.rstrip().split('/')[-1].split('.')[0]
            if line.startswith('#CHROM'):
                vcf_names = [x for x in line.rstrip().split('\t')]
            if line.startswith('chr' + str(chr_id) + '\t'):
                break
            start_row+=1
   
    print("Reference Genome:", reference_genome)
    ref_filename = 'data/ref/' + reference_genome + '_chr' + str(chr_id) + '.fa'
    sections = process_sections(reference_genome, chr_id)
    print("No. of Sections:", len(sections))
    print("VCF Headers:",vcf_names)
    vcf_reader = pd.read_csv(filename, 
                             chunksize=3000, 
                             skiprows=[i for i in range(0, start_row)], 
                             delim_whitespace=True, 
                             header=None, 
                             names=vcf_names)
    
    all_pos, all_ref, all_alt = section_wise_edits(vcf_reader, sections, chr_id)

    ref_subsequences = fetch_ref_subsequences(ref_filename, sections, seq_len, ct)
    print([len(r) for r in ref_subsequences])




filename = 'data/U654E5F.vcf'
fetch_subsequences(filename, 1, 1000, 10)