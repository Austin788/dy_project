import os
import json
import wget
import time
import datetime


def load_last_filename(dir, format):
    timestamp = 0
    for dirname in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, dirname)):
            value = time.strptime(dirname, format)
            value = int(time.mktime(value))
            if value > timestamp:
                timestamp = value
    return timestamp


def load_max_timestamp(path):
    with open(path) as f:
        data = json.load(f)
        if 'RECORDS' in data:
            data = data['RECORDS']

    timestamp = 0
    for raw_data in data:
        created_at = int(raw_data['created_at'])
        if created_at > timestamp:
            timestamp = created_at
    return timestamp


if __name__ == "__main__":
    export_path = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data/素材库/export_wallpaper/230206.json"
    base_dir = '/Users/meitu/Documents/midlife_crisis/project/dy_project/data/素材库/llqt/'
    format = '%Y_%m_%d_%H_%M_%S'

    # 方式1 直接读取最后时间
    # last_timestamp = load_last_filename(base_dir, format)

    # 方式2 自定义文件夹时间
    last_timestamp = time.strptime('2023_02_01_23_07_18', format)
    last_timestamp = int(time.mktime(last_timestamp))
    print(last_timestamp)

    save_timestamp = load_max_timestamp(export_path)
    save_date_str = datetime.datetime.fromtimestamp(save_timestamp).strftime(format)
    save_dir = os.path.join(base_dir, save_date_str)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)


    with open(export_path) as f:
        data = json.load(f)
        if 'RECORDS' in data:
            data = data['RECORDS']

    filename_url_dict = {}

    for raw_data in data:
        try:
            url = raw_data['img']
            filename = os.path.basename(url)
            created_at = int(raw_data['created_at'])
            download_count = int(raw_data['download_count'])
            type_name = raw_data['self_name']

            if created_at < last_timestamp:
                continue

            save_name = f"{'%05d'%download_count}_{type_name}_{filename}"

            save_path = os.path.join(save_dir, save_name)

            filename_url_dict[save_name] = raw_data

            if os.path.exists(save_path):
                print("exist")
                continue

            wget.download(url, out=save_path)
            time.sleep(1)
            print(f"downlaod {url} complete!")
        except:
            continue
    with open(os.path.join(save_dir, 'filename_url.json'), 'w') as f:
        json.dump(filename_url_dict, f, indent=4, ensure_ascii=False)
    print("Done")