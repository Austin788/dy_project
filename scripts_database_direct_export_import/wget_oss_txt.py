import os
import json
import wget
import time
import datetime
import hashlib


def get_sites(filename):
    index = filename.find("/", 9)
    filename = filename[:index]
    return filename


def get_bussiness_site(lines):
    sites = {}
    for i, filename in enumerate(lines):
        filename = get_sites(filename)
        if filename not in sites:
            sites[filename] = 0
        sites[filename] = sites[filename] + 1
    return sites


include_sites = ['https://cdn-ali-img-shdiy.shanhutech.cn',
                 'https://dingyue.ws.126.net',
                 'https://dimg04.c-ctrip.com',
                 'https://cdn3.codesign.qq.com']

if __name__ == "__main__":


    txt_path = "/Users/meitu/Documents/midlife_crisis/素材列表/甜七.txt"

    with open(txt_path) as f:
        lines = f.readlines()

    image_list = [line.strip('\n') for line in lines]

    sites = get_bussiness_site(lines)
    for key, value in sites.items():
        print(key, value)
    exit(0)


    save_dir = f'/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/素材库/神图君0234/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    kouling = "0234"
    filename_url = {}
    count = 0
    url_set = set()
    for url in image_list:
        try:
            if get_sites(url) in include_sites:
                md5_url = hashlib.md5(url.encode("utf-8")).hexdigest()
                if md5_url in url_set:
                    continue
                else:
                    url_set.add(md5_url)
                download_image_name = f"{kouling}_{count}_{md5_url}.jpg"
                # wget.download(url, os.path.join(save_dir, download_image_name))
                filename_url[download_image_name] = url
                count += 1
                # time.sleep(1)

        except:
            continue

    with open(os.path.join(save_dir, "filename_url.json"), "w") as f:
        json.dump(filename_url, f, indent=4)

    print("Done")