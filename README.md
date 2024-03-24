# Secure Paternity Test

A framework to perform secure paternity tests between two parties with privately known genomes without the need for an honest third party, to demonstrate the use of secret sharing and multiparty computation frameworks in the field of secure data processing in healthcare.

### Usage

The framework uses the [MP-SPDZ library](https://github.com/data61/MP-SPDZ) for secret shares.

For demonstration purposes, we've selected the toy dataset from iDash. 
To use the framework, first use `generate_player_data` to choose the two patients out of the dataset. We use [Edit Distance](https://en.wikipedia.org/wiki/Edit_distance) as the evaluation metric for finding similar patients as established in relevant research. 

For the paternity test, we look into the edit distance in 25 sections of the genome that are told to be relevant indicators as reference [here](https://dl.acm.org/doi/10.1145/2046707.2046785). 

To run secure edit distance, clone MP-SPDZ and use it's compiler like this-

`Scripts\compile-run.py -E semi2k <path_to_Sources_folder>/paternity_test`

Semi2k is the chosen Secret Sharing scheme as it supports semi-honest adversaries which is in line with our two parties.

### Author

Yagaagowtham Palanikumar