import json
import tkinter
import requests
from multiprocessing import Pool
from time import sleep
from pathlib import Path
from tkinter import ttk
from downloader import download_file

# Input the year and the day number of year to start with.
year = 2002
first_day = 1
last_day = 0  # default: 0
collection = '61'
product = 'MOD08_D3'

# Is it a leap year? And return the number of days.
if last_day == 0:
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        last_day = 366
    else:
        last_day = 365

# Pop a window to show the downloading progress bar.
window = tkinter.Tk()
window.title('HDF File Downloader')
file_text = tkinter.StringVar()
speed_text = tkinter.StringVar()
file_text.set('Reading url of HDF file...')
speed_text.set('0 KB/s - Empty yet (0%)')
tkinter.Label(window, textvariable=file_text, ).grid(row=1, column=1)
tkinter.Label(window, textvariable=speed_text, ).grid(row=2, column=1)
progress_bar = ttk.Progressbar(window, value=0, length=500)
progress_bar.grid(row=3, column=1)
window.update()

# Prepare parameters for the following loop.
url_list = []
fail_list = []
fail_count = 0
token = '9696F18A-18AD-11E9-99E8-CDB570C49BBF'
headers = {'Authorization': 'Bearer ' + token}

path_product = Path.cwd() / product
path_year = path_product / str(year)
if not path_year.exists():
    path_year.mkdir(parents=True)

pool = Pool()

for day_of_year in range(first_day, last_day + 1):
    url_product = 'https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/{}/{}'.format(
        collection, product)
    url_path = '{}/{}/{:0>3}'.format(url_product, year, day_of_year)
    url_json = url_path + '.json'
    is_get = True

    # Retry twice in case of a bad connection with NASA.
    try:
        day_json = requests.get(url_json, timeout=5).json()
    except:
        if not len(url_list):
            print('No data is found on the first day:')
            print(url_path)
            quit()
        fail_list.append(day_of_year)
        print('{}/{} [FAIL]'.format(day_of_year, last_day))
    else:
        print('{}/{}'.format(day_of_year, last_day))
        url_file = day_json[0]['name']
        url_full = url_path + '/' + url_file
        url_list.append(url_full)
        path_hdf = path_year / url_file

        # Launch the downloader.
        file_text.set('[{}/{}]{}'.format(day_of_year, last_day, url_file))
        download_file(url_full, path_hdf, speed_text, progress_bar, window)

# Export successful urls and a list of failure.
path_txt = path_product / ('{}({}).txt'.format(year, len(url_list)))

# Show the end of the whole task.
with open(path_txt, 'w') as f:
    for item in url_list:
        f.write('{}\n'.format(item))

# Tell the number of failure days.
if not len(fail_list):
    path_fail = path_product / ('{}_fail({}).txt'.format(year, len(fail_list)))
    with open(path_fail, 'w') as f:
        for item in fail_list:
            f.write('{}\n'.format(item))

print('Failure Time: {}'.format(len(fail_list)))
