import os
import json
import wget
import time
import datetime

if __name__ == "__main__":

    save_dir = f'/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/素材库/亲子头像2/'

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    with open("/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/素材库/亲子头像/DownLoadUrl.txt") as f:
        lines = f.readlines()

    for i, filename in enumerate(lines):
        filename = filename.strip("\n")
        try:
            wget.download(filename, os.path.join(save_dir, f"{i}.jpg"))
            time.sleep(3)
        except:
            continue
    print("Done")