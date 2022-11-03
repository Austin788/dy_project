import os
import json
import wget
import time

if __name__ == "__main__":
    with open("/Users/meitu/Downloads/qqxcx_wallpaper.json") as f:
        data = json.load(f)
    for raw_data in data:
        filename = os.path.basename(raw_data['img'])
        if os.path.exists(os.path.join('/Users/meitu/Downloads/image', filename)):
            print("exist")
            continue
        try:
            wget.download(raw_data['img'], '/Users/meitu/Downloads/image')
            time.sleep(3)
        except:
            continue
    print("Done")