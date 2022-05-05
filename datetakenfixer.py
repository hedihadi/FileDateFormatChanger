from os import walk
import datetime
import os

from pathlib import Path
import pathlib
print("\n\n\n")
'''change this to True if you ONLY want to edit dng files'''
ignore_non_dng_files=False
'''this string contains the user's provided folder'''
folder=None
'''this list will contain all the files that will be edited'''
files=[]

'''making sure folder path is correct and exists'''
while True:
    folder=input("folder: ")
    if os.path.exists(folder)==False:
        print("folder path is wrong,\n")
    else:
        break

'''walk through all the subfolders and collect all the files'''
for (path, dirnames, filenames) in walk(folder):
    for filename in filenames:
        if ignore_non_dng_files==True:
            if os.path.splitext(filename)[1] !=".dng":
                continue
        files.append((path+"\\"+filename))


'''run this code for each file'''
for file in files:
    file_name=Path(file).stem+Path(file).suffix
    '''the client's date format is 15 characters, and we get the first 15 characters'''
    date_string=file_name[:15]
    '''this string will contain the rest of the filename, including extension'''
    '''for example if the file_name is 20010501_010101aaaaaaa.dng,'''
    '''date_string=20010501_010101'''
    '''extension=aaaaaaa.dng'''
    extension=file_name[15:]
    '''this string contains the file's parent folder, we need it this infromation to rename the file later on'''
    dir_path = os.path.dirname(os.path.realpath(file))
    '''this string contains the python script's location, we need it to reference exiv2.exe later on'''
    main_directory = os.path.dirname(os.path.realpath(__file__))

    '''extract the date from the filename'''
    date=None
    try:
        date = datetime.datetime.strptime(date_string, "%Y%m%d_%H%M%S%f")
    except ValueError:
        '''if the date format is wrong, skip this file'''
        wrong_date_file=os.path.join(dir_path, date_string+extension)
        print(f"'{wrong_date_file}' has a wrong date format, ignoring...\n")
        continue
    
    '''convert the datetime to client's preffered datetime format'''
    datetime_string=date.strftime(f"%Y-%m-%d-%H-%M-%S-%f")[:-4]

    '''rename the files'''
    old_file = os.path.join(dir_path, date_string+extension)
    new_file = os.path.join(dir_path,datetime_string+extension)
    os.rename(old_file,new_file)

    '''fix the date-taken metadata'''
    '''using exiv2 library'''
    '''see https://www.exiv2.org/manpage.html'''
    os.system(f'{main_directory}\\exiv2.exe -M"set Exif.Photo.DateTimeOriginal {date.year}:{date.month}:{date.day} {date.hour}:{date.minute}:{date.second}" "{new_file}"')
    
print("done")