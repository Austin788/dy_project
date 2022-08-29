import os
import functools
from scripts.batch_split_mp4 import cmp

if __name__ == "__main__":
    batch_image = "/Users/meitu/Downloads/ff"
    image_dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data/image/男生头像"

    dst_filenames = os.listdir(image_dir)
    dst_filenames.remove(".DS_Store")
    dst_filenames.sort(key=functools.cmp_to_key(cmp), reverse=True)

    src_filenames = os.listdir(batch_image)
    src_filenames.remove(".DS_Store")
    src_filenames.sort()
    # print(src_filenames)

    for i, src_filename in enumerate(src_filenames):
        os.rename(os.path.join(batch_image, src_filename), os.path.join(batch_image, dst_filenames[i]))
