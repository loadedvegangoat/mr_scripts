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
import pydicom
import glob
files_lst = []

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
	print('Cant find, error occured: ', e)

for i in os.listdir():
	if i.startswith('MR') is True:
		files_lst.append(i)
		if len(files_lst) > 0:
			break
print('MR Number is: ', pydicom.filereader.dcmread(files_lst[0]).PatientID)
