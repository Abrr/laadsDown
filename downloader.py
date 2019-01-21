import time
import requests


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
        print('#{} finished'.format(day_of_year))


if __name__ == '__main__':
    source_url = r'http://cachefly.cachefly.net/100mb.test'
    local_file = r'/Users/ak/Downloads/out.test'
    download_file(source_url, local_file, 200,)
