import time
import requests

def download_file(source_url, local_file, speed_text, progress_bar, window):
    
    time_start = time.time()
    with requests.get(source_url, stream=True) as r:
        content_length = int(r.headers['content-length'])
        down_size = 0
        with open(local_file, 'wb') as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
                
                # Content to display.
                down_size += len(chunk)
                down_speed = down_size/1024/(time.time()-time_start)
                pred_time = (time.time()-time_start)*(content_length - down_size)/down_size
                pred_min = pred_time / 60
                pred_sec = pred_time % 60

                down_percent = down_size/content_length
                line = '{}KB/s - {.2f}MB/{.2f}MB ({:.0%}) - {}:{}'.format(
                    down_speed, down_size/1024/1024, content_length/1024/1024, down_percent, pred_min, pred_sec)
                speed_text.set(line)
                progress_bar["value"] = down_size/content_length*100
                window.update()

                if down_size >= content_length:
                    break
        time_cost = time.time() - time_start
        line = 'Total time: %.2f s, average speed: %.2f KB/s'
        line = line % (time_cost, down_size/1024/time_cost)
        print(line)

if __name__ == '__main__':
    source_url = r'http://cachefly.cachefly.net/100mb.test'
    local_file = r'/Users/ak/Downloads/out.test'
    download_file(source_url, local_file)