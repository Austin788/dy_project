import os
import cv2
import shutil

if __name__ == "__main__":
    dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/素材库/亲子头像_分组"

    min_size = 1000

    save_dir = os.path.join(dir, f"below_{min_size}")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for filename in os.listdir(dir):
        if str.lower(os.path.splitext(filename)[-1]) in ['.jpg']:
            image_path = os.path.join(dir, filename)
            image = cv2.imread(image_path)
            if image.shape[0] < min_size and image.shape[1] < min_size:
                shutil.move(image_path, os.path.join(save_dir, filename))
