"""
Author: Ryan Cool
Version: 1.0.3
Updates
        Edited: 2021-04-20
        - Added line of code to look for 3d_dicom_orig folder for some subjects
        whose mr folder was trimmed

"""

import sys
import os
import re
import pydicom
import glob

seq_lst = []

if len(sys.argv) == 1:
    subj = input('enter date_petid: ')
else:
    subj = sys.argv[1]

try:
    # May need to change tmp_pth to directory where mr is
    tmp_pth = (glob.glob('/data8/data/*_mr/' + subj))
    os.chdir(str(tmp_pth[0]))
    if '3d_dicom_orig' in os.listdir():
        os.chdir('3d_dicom_orig')
    else:
        os.chdir('3d_dicom')
except Exception as e:
    print('Cant complete, error occured: ', e)

while True:
    param = input('enter parameter (can leave blank for all info or type help for parameter names): ')
    if param == 'help':
        print(pydicom.filereader.dcmread(os.listdir()[0]).dir())
    elif len(param) == 0:
        break
    elif param in pydicom.filereader.dcmread(os.listdir()[0]).dir():
        break

seq = input('enter name of sequence, i.e. Sag or rest: ')

for i in os.listdir():
    data = pydicom.filereader.dcmread(i).ProtocolName
    if re.search(seq, str(data)):
        seq_lst.append(i)
        if len(seq_lst) > 1:
            break

if len(param) == 0:
    print(pydicom.filereader.dcmread(seq_lst[0]))
else:
    value = getattr(pydicom.filereader.dcmread(seq_lst[0]), param)
    print(param, "is:", value)
