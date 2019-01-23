import json
import ssl
import time
import requests
from urllib.request import Request, urlopen
from multiprocessing import Manager, Pool
from pathlib import Path


# Input the year and the day number of year to start with.
year = 2018
first_day = 1
last_day = 0  # default: 0
collection = '61'
product = 'MYD08_D3'
tiktok = time.time()


def is_leap_year(year):
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        return 366
    else:
        return 365


# Is it a leap year? And return the number of days.
if last_day == 0:
    last_day = is_leap_year(year)

# Prepare parameters for the following loop.
token = '9696F18A-18AD-11E9-99E8-CDB570C49BBF'
headers = {'Authorization': 'Bearer ' + token}
url_product = 'https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/{}/{}'
url_product = url_product.format(collection, product)
CTX = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
path_product = Path.cwd() / product
path_year = path_product / str(year)
if not path_year.exists():
    path_year.mkdir(parents=True)


def try_down(day_of_year, url_list, fail_list):
    url_path = '{}/{}/{:0>3}'.format(url_product, year, day_of_year)
    url_json = url_path + '.json'
    try:
        read_json = urlopen(Request(url_json, headers=headers), context=CTX)
        read_json = json.loads(read_json.read())
        # read_json = requests.get(url_json, headers=headers, timeout=5).json()
    except:
        # if not len(url_list):
            # print('No data is found on the first day:')
            # print(url_path)
            # quit()
        fail_list.append(day_of_year)
        print('{}/{} [FAIL]'.format(day_of_year, last_day))
    else:
        print('{}/{}...'.format(day_of_year, last_day))
        url_file = read_json[0]['name']
        url_full = url_path + '/' + url_file
        url_list.append(url_full)
        path_hdf = path_year / url_file
        download_file(url_full, path_hdf, day_of_year)


def download_file(source_url, local_file, day_of_year):
    with requests.get(source_url, stream=True) as r:
        content_length = int(r.headers['content-length'])
        down_size = 0
        with open(local_file, 'wb') as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
                if down_size >= content_length:
                    break
        print('#{} finished '.format(day_of_year))


if __name__ == '__main__':
    url_list = Manager().list()
    fail_list = Manager().list()
    pool = Pool(10)
    range_snpp = list(range(1, 90)) + list(range(274, 365))
    # for i in range(first_day, last_day + 1):
    for i in range_snpp:
        pool.apply_async(try_down, (i, url_list, fail_list))
    pool.close()
    pool.join()

    # Export successful urls and a list of failure.
    path_txt = path_product / ('{}.txt'.format(year))

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

    print('Failure of {}: {}'.format(year, len(fail_list)))
    print(fail_list)
    tiktok = time.time() - tiktok
    print('Total Time: {:0>2.0f}:{:0>2.0f}:{:0>2.0f}'.format(
        tiktok / 60 / 60, tiktok / 60 % 60, tiktok % 60))
