import os
import cv2
from tqdm import tqdm

if __name__ == "__main__":
    dir = "/Users/meitu/Downloads/test_bug/"
    save_dir = "/Users/meitu/Downloads/test_bug_small/"

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    max_size = 800
    for filename in os.listdir(dir):
        if str.lower(os.path.splitext(filename)[-1]) not in ['.jpg', '.jpeg', '.png', '.heic']:
            continue

        image = cv2.imread(os.path.join(dir, filename))
        if image is None:
            print(filename)
            continue
        if image.shape[0] > image.shape[1]:
            image_width = max_size * image.shape[1] / image.shape[0]
            image_height = max_size

        else:
            image_height = image.shape[0] / (image.shape[1] / max_size)
            image_width = max_size

        resize_image = cv2.resize(image, (int(image_width), int(image_height)))
        # resize_image = cv2.resize(image, (0, 0), fx=1.5, fy=1.2, interpolation=cv2.INTER_CUBIC)

        cv2.imwrite(os.path.join(save_dir, filename+".jpg"), resize_image)

