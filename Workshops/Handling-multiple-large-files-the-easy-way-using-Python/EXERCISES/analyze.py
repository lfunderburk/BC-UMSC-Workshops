#### Handling multiple large files the easy way using Python
#### Workshop facilitator: Laura Gutierrez Funderburk | Department of Mathematics | Simon Fraser University
#### Script Author: Laura Gutierrez Funderburk | Department of Mathematics | Simon Fraser University
#### Workshop date: April 24 2018


"""IMPORTING LIBRARIES"""

import glob
from matplotlib import pyplot as plt
import pandas as pd

"""LOAD LOCATION"""



"""FUNCTION DEFINITION"""

# This function extracts the lines containing the number of sequences in each family, for a given file
# Input is an output-file obtained after running MACSE and QSCORE on the families found on the synteny files
# Output is an array containing only those lines that contain the word 'sequence(s)' in it
def get_seq_len(file):
    """This function extracts all those entries in the output files containing the words 'sequence(s)'"""
    
    # open file and use comprehension list to store the desired entires
    with open(file, 'r') as inF:
        seq_lines = [line for line in inF if "sequence(s)" in line]
    inF.close()
    
    # return array with desired entries
    return seq_lines

# This function will take the 
def get_num_seq_in_family(file):
    
    lines = get_seq_len(file)
    
    len_seq_in_fam = [lines[i].split("\t")[0] for i in range(2)]
    
    return len_seq_in_fam

def get_family_info(file):
    
    with open(file,'r') as inF:
        families = [line for line in inF if "MZ" in line]
    inF.close()
    
    fam_data = families[10:]
    
    return fam_data


## This function takes as input a file with output from MACSE and QSCORE, and a family_number F_i which can be either 1,2
## The function outputs a table for either F1 or F2 which contains all the entries where family names were identified

def extract_family_length_scores(file,family_number):
    
    """This function extracts family length and scores"""
    
    # call get_num_seq_in_family to get the number of sequences in each family
    len_of_fam = get_num_seq_in_family(file)
    
    # get all those entries in output-file that contain family names of the form MZ...
    datum = get_family_info(file)

    # identify F1 and F2 with the appropriate family name
    F1, F2 = datum[-4],datum[-2]
     
    # get Q, Cline, TCscores for both F1,F2
    F1_F2_scores = [[datum[-j].split(";")[-i].split("=")[1] for i in range(1,4)]\
         for j in(1,3)]
    
    # store family name, length and scores for F1
    if family_number==1:
        table = F1_F2_scores[1]
        table.append(len_of_fam[0])
        table.append(F1)
        table = table[::-1]
        
    # store family name, length and scores for F2
    elif family_number ==2:
        table = F1_F2_scores[0]
        table.append(len_of_fam[1])
        table.append(F2)
        table = table[::-1]
    
    # return array called table with family name, number of sequences, and Q, Cline and TC for either F1 or F2
    return table

# This function will identify all those files which contain no ***ERROR*** entries, and save the indeces
# It takes as input an array containing output-file names and it outputs the indeces whose files contain an error. 
def select_index(file_array):
    """This function identifies those tables that contain an error, as produced by QSCORE"""
    
    # Store indeces here
    file_index = []
    size = len(file_array)
    # Iterate
    for i in range(size):
        # Store desired data for each i
        data  = get_family_info(file_array[i])
        # Perform test: We observe that those files with an error have length 10 or 11 depending on the number of errors
        # "Healthy" files are of length 9
        # We want to access healthy files and, for now, skip files with errors in them
        test = len(data)
        if test==9:
            file_index.append(i)
        else:
            continue
    return file_index

# This function takes as input an array containing all output file names
# It outputs a pair of dataframes for F1,F2
def data_to_dataframe(file_array):
    
    """This function will turn all data stored in tables for F1,F2 into dataframes"""
    
    # Store indeces for files which are free from error
    file_index = select_index(file_array)
    
    # Turn data in F1 into dataframe, attach column names
    A_df = pd.DataFrame([extract_family_length_scores(file_array[i],1) for i in file_index],\
                      columns = ["Cluster", "Size", "Score_A", "Score_B","Score_C"])
    
    # Turn data in F2 into dataframe, attach column names
    B_df = pd.DataFrame([extract_family_length_scores(file_array[i],2) for i in file_index],\
                      columns = ["Cluster", "Size", "Score_A", "Score_B","Score_C"])
    
    # Return both datafrains as a 2-tuple
    return (A_df,B_df)


# This function takes as input a dataframe with either info from both F1 and F2 and "cleans" it
# It removes characters such as '\n' which appear in the first and last columns, and turns all numerical values from str into float
def clean_data_frame(data_frame_pair):
    
    """This function cleans our dataframes"""
    # empty array: save cleaned dataframes
    clean_family_dataframes = []
    
    # Loop through both family dataframes
    for i in range(2):
        # dataframe on variable clean_Fi_df
        clean_Fi_df = data_frame_pair[i]
        # remove '/n' from columns Cline_Score and Family
        clean_Fi_df['Score_C'] = clean_Fi_df['Score_C'].map(lambda x: x.rstrip('\n'))
        clean_Fi_df['Cluster'] = clean_Fi_df['Cluster'].map(lambda x: x.rstrip('\n'))
        # Turn Cline, Q and TC scores into float (originally they are coded as strings)
        clean_Fi_df['Score_C'] = clean_Fi_df['Score_C'].apply(lambda x:float(x))
        clean_Fi_df['Score_A'] = clean_Fi_df['Score_A'].apply(lambda x:float(x))
        clean_Fi_df['Score_B'] = clean_Fi_df['Score_B'].apply(lambda x:float(x))
        clean_Fi_df['Size'] = clean_Fi_df['Size'].apply(lambda x:int(x))
        # store clean_Fi_df into array
        clean_family_dataframes.append(clean_Fi_df)
        
    # return array with clean versions of F1, F2
    return clean_family_dataframes

def scatter_plot_scores_F1_vs_F2(clean_Data):
    F1_Data_Frame = clean_Data[0]
    F2_Data_Frame = clean_Data[1]
    
    fig = plt.figure()
    plt.subplots_adjust(left=None, bottom=None, right=None, top=0.9,
                wspace=0.6, hspace=0.5)
    
    ax1 = fig.add_subplot(1, 3, 1)
    ax2 = fig.add_subplot(1, 3, 2)
    ax3 = fig.add_subplot(1,3,3)
    
    ax1.scatter(F1_Data_Frame.Q_Score, F2_Data_Frame.Q_Score,s=30,c='Blue')
    ax2.scatter(F1_Data_Frame.Cline_Score, F2_Data_Frame.Cline_Score,s=30,c='Red')
    ax3.scatter(F1_Data_Frame.TC_Score, F2_Data_Frame.TC_Score,s=30,c='Green')
    
    ax1.set_xlabel("Score_A Cluster A vs Cluster A'")
    ax1.set_ylabel("Score_A Cluster B vs Cluster B'")
    #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    #ax1.title('Scores F1 vs F2')
    
    ax2.set_xlabel("Score_C Cluster A vs Cluster A'")
    ax2.set_ylabel("Score_C Cluster B vs Cluster B'")
    #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    ax2.set_title('Scores Cluster A vs Cluster B')
    
    ax3.set_xlabel("Score_B Cluster A vs Cluster A'")
    ax3.set_ylabel("Score_B Cluster B vs Cluster B'")
    
    plt.show()

def plot_frequency(Fi_Data_Frame,family):

    fig = plt.figure()
    plt.subplots_adjust(left=None, bottom=None, right=None, top=0.9,
                wspace=0.6, hspace=0.5)
    ax1 = fig.add_subplot(1, 3, 1)
    ax2 = fig.add_subplot(1, 3, 2)
    ax3 = fig.add_subplot(1,3,3)
    ax1.hist(Fi_Data_Frame['Score_A'],color='Blue') #label='Q Score F1'
    ax3.hist(Fi_Data_Frame['Score_C'],color='Green') #label='Cline Score F1')
    ax2.hist(Fi_Data_Frame['Score_B'],color='Red')  #label='TC Score F1')
    ax1.set_xlabel('Score_A')
    ax1.set_ylabel('Frequency')
    #ax1.legend()
    ax3.set_xlabel('Score_C')
    ax3.set_ylabel('Frequency')
    ax2.set_title('Distribution for Cluster ' + str(family))
    #ax2.legend()
    ax2.set_xlabel('Score_B')
    ax2.set_ylabel('Frequency')
    #ax3.legend()
    plt.show()
    
def plot_number_seq_vs_scores(Fi_Data_Frame,family):
    
    fig = plt.figure()
    plt.subplots_adjust(left=9, bottom=None, right=10, top=0.9,
                wspace=0.8, hspace=0.5)
    ax1 = fig.add_subplot(1, 3, 1)
    ax2 = fig.add_subplot(1, 3, 2)
    ax3 = fig.add_subplot(1,3,3)
    ax1.scatter(Fi_Data_Frame.Score_A, Fi_Data_Frame.Size,s=30,c='Blue')
    ax3.scatter(Fi_Data_Frame.Score_C, Fi_Data_Frame.Size,s=30,c='Green')
    ax2.scatter(Fi_Data_Frame.Score_B, Fi_Data_Frame.Size,s=30,c='Red')
    ax1.set_xlabel('Score_A')
    ax1.set_ylabel('Size')
    ax3.set_xlabel('Score_C')
    ax3.set_ylabel('Size')
    ax2.set_title('Scores vs Size  ' + str(family))
    ax2.set_xlabel('Score_B')
    ax2.set_ylabel('Size')
    plt.show()
