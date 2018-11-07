#### Handling multiple large files the easy way using Python
#### Workshop facilitator: Laura Gutierrez Funderburk | Department of Mathematics | Simon Fraser University
#### Script Author: Laura Gutierrez Funderburk | Department of Mathematics | Simon Fraser University
#### Workshop date: April 24 2018

"""Importing Libraries"""
import glob

"""Directories"""
ALL_GENE_FILE_DIRECTORY = "./DATA/ALL_GENE_file"

"""Function Definition Area"""

def remove_repetitions(family_pair):
    uniq_array = []
    for x in family_pair:
        if x not in uniq_array:
            uniq_array.append(x)
    return uniq_array

def store_data_in_table(input_data_directory,ext):
    data_files = glob.glob(input_data_directory + "*." + str(ext))
    data = data_files[0]
    
    with open(data,'r') as f:
        data_table = [line for line in f]
    f.close()
    
    return data_table

def disect_table(data_table):
    size = len(data_table)
    disected_arr = [data_table[i].split(",") for i in range(size)]
    
    return disected_arr

def get_families(disected_table):
    size = len(disected_table)
    fam_pair = [[disected_table[i][0],disected_table[i][3]] for i in range(1,size)]
    
    unique_pairs = remove_repetitions(fam_pair)
    
    return unique_pairs


def output_entries_in_ALL_GENE_FILE(family_name):
    with open(ALL_GENE_FILE_DIRECTORY,'r') as inF:
        found_fam_in = [line for line in inF if family_name in line]
    return found_fam_in


