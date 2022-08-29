import os
import functools
from scripts.batch_split_mp4 import cmp

if __name__ == "__main__":
    batch_image = "/Users/meitu/Downloads/用所选项目新建的文件夹 10"
    image_dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data/image/职业头像"

    dst_filenames = os.listdir(image_dir)
    if os.path.exists(os.path.join(image_dir, ".DS_Store")):
        dst_filenames.remove(".DS_Store")
    dst_filenames.sort(key=functools.cmp_to_key(cmp), reverse=True)

    src_filenames = os.listdir(batch_image)

    if os.path.exists(os.path.join(batch_image, ".DS_Store")):
        src_filenames.remove(".DS_Store")
    src_filenames.sort()
    # print(src_filenames)

    for i, src_filename in enumerate(src_filenames):
        os.rename(os.path.join(batch_image, src_filename), os.path.join(batch_image, dst_filenames[i]))
