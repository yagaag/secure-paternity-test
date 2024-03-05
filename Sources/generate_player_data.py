from data_loader import fetch_aligned_idash

def generate_player_data(i, j):

    ref, data, genome_additions_colated, addition_indices = fetch_aligned_idash()

    mp = {'A': '0', 'C': '1', 'G': '2', 'T': '3', '_': '4'}
    s1 = [mp[d] for d in data[i]]
    s2 = [mp[d] for d in data[j]]

    s1 = ' '.join(s1)
    with open('Data/Player-Data/Input-P0-0', 'w') as f:
        f.write(s1)

    s2 = ' '.join(s2)
    with open('Data/Player-Data/Input-P1-0', 'w') as f:
        f.write(s2)

generate_player_data(0,1)
