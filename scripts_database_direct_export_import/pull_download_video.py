import os
import numpy as np
import shutil
import hashlib
import time

def md5_value(path):
    with open(path, 'rb') as file_pointer:
        data = file_pointer.read()
    file_md5 = hashlib.md5(data).hexdigest()
    file_pointer.close()
    return file_md5

if __name__ == "__main__":
    video_path = "/Users/meitu/Documents/midlife_crisis/采集素材/" #一定要以/结尾
    save_dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data/素材库/download_video"

    count = 0
    for dir_path, _, filenames in os.walk(video_path):
        for filename in filenames:
            if (not filename.endswith(".mp4") and not filename.endswith(".txt")) or filename.startswith('.'):
                continue

            if filename == "日志.txt" or filename == "在线授权卡密信息.txt":
                continue
            file_path = os.path.join(dir_path, filename)
            file_size = os.path.getsize(file_path)

            if filename.endswith(".mp4") and file_size < 1024:
                continue


            relative_path = file_path.replace(video_path, "")
            dst_path = os.path.join(save_dir, relative_path)

            if filename.endswith(".txt") and os.path.exists(dst_path) and md5_value(file_path) != md5_value(dst_path):
                shutil.copy(dst_path, dst_path + "_" + str(time.time()))
                os.remove(dst_path)


            # if relative_path in exist_filenames:
            #     continue

            if not os.path.exists(os.path.dirname(dst_path)):
                print(dst_path)
                os.makedirs(os.path.dirname(dst_path))

            shutil.move(file_path, dst_path)
            print(f"pull {file_path}")
            # shutil.copy(file_path, dst_path)
            count += 1
            # exist_filenames.add(relative_path)

    print(f"pull video number:{count}")
    # np.savez(npz_path, exist_filenames)


