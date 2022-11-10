import os
import json
import wget
import time
import datetime

if __name__ == "__main__":
    date = datetime.datetime.fromtimestamp(int("1667801091")).strftime('%Y_%m_%d_%H_%M_%S')

    save_dir = f'/Users/meitu/Documents/midlife_crisis/project/dy_project/data/鲤鱼取图素材/{date}'

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    with open("/Users/meitu/Downloads/qqxcx_wallpaper (1).json") as f:
        data = json.load(f)

    print(len(data))

    for raw_data in data:
        filename = os.path.basename(raw_data['img'])
        if os.path.exists(os.path.join(save_dir, filename)):
            print("exist")
            continue
        try:
            wget.download(raw_data['img'], save_dir)
            time.sleep(3)
        except:
            continue
    print("Done")