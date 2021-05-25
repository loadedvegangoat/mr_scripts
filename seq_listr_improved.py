"""
Author: Ryan Cool
Version: 1.0.3

Updates
    Edited: 2021-04-20
    - Added line of code to look for 3d_dicom_orig folder for some subjects
    whose mr folder was trimmed

	Edited: 2021-04-07
	- Added Sequence number in with Sequence Name
"""

import sys
import concurrent.futures
import time
import os
import pydicom
from tqdm import tqdm
import glob

if len(sys.argv) == 1:
    subj = input('enter date_petid: ')
else:
    subj = sys.argv[1]


try:
	# May need to change tmp_pth to directory where mr is
    tmp_pth = (glob.glob(subj))
    os.chdir(str(tmp_pth[0]))
    if '3d_dicom_orig' in os.listdir():
        os.chdir('3d_dicom_orig')
    else:
        os.chdir('3d_dicom')

except Exception as e:
	print('Error occured: ', e)


def file_org(file):
	if file.startswith('MR' or 'SC') is True:
		seq_name = pydicom.filereader.dcmread(file).SeriesDescription
		seq_num = pydicom.filereader.dcmread(file).SeriesNumber
		if seq_num not in seq_dict.keys():
			seq_dict[seq_num] = seq_name


start = time.time()
seq_dict = {}
with concurrent.futures.ThreadPoolExecutor() as executor:
	list(tqdm(executor.map(file_org, os.listdir()), total=len(os.listdir())))

print('This subject had these runs done:\n\n')
for (x, y) in sorted(seq_dict.items()):
	print(x, y)
end = time.time()

print(f'\nTime taken to complete: {end - start:.2f}s\n')
