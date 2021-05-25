import sys
import os
import pydicom
import glob
from tqdm import tqdm
import concurrent.futures
import time


def mr_number(subj):
    files_lst = []
    for i in os.listdir(subj):
	    if i.startswith('MR') is True:
	        files_lst.append(i)
	        if len(files_lst) > 0: break
    return "MR Number is: " + pydicom.filereader.dcmread(subj + files_lst[0]).PatientID
    # print(mr_number(sys.argv[2]))


    
seq_dict = {}

def file_org(file):
    if file.startswith('MR' or 'SC'):
        seq_name = pydicom.filereader.dcmread(file).SeriesDescription
        seq_num = pydicom.filereader.dcmread(file).SeriesNumber
        if seq_num not in seq_dict.keys():
            seq_dict[seq_num] = seq_name

def seq_listr(subj):
    start = time.time()
    os.chdir(subj) 
    with concurrent.futures.ThreadPoolExecutor() as executor:
	    list(tqdm(executor.map(file_org, os.listdir()), total=len(os.listdir())))
    end = time.time()
    print('\nThis subject had these runs done:\n\n')
    print(*(' '.join(map(str, x)) for x in sorted(seq_dict.items())), sep='\n')
    print('\n')
    return 'Time taken to complete: ' + str(end - start)


if sys.argv[1].lower() == "sequences":
    print(seq_listr(sys.argv[2]))
elif sys.argv[1].lower() == "mr_number":
    print(mr_number(sys.argv[2]))