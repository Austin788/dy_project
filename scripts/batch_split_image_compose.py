import os
import cv2
import shutil
import numpy as np

from data_util import md5, DYDataUtils
from generate_video import TextWriter


if __name__ == "__main__":
    dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/素材库/亲子头像_分组"
    image_dir_name = "亲子头像"
    compose_name = "合成"
    image_num = 186
    use_image_group_num = True

    filenames = []
    for filename in os.listdir(dir):
        if os.path.splitext(filename)[-1] in ['.jpg', '.png', '.jpeg']:
            filenames.append(filename)
    filenames.sort()

    dy_data_utils = DYDataUtils(data_root="/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast")
    group_num = dy_data_utils.get_avilable_group_num(type=image_dir_name,
                                                     data_root="/Users/meitu/Documents/midlife_crisis/project/dy_project/data")

    for i in range(image_num):
        image_path = os.path.join(dir, filenames[i])
        image_md5 = md5(image_path)
        image_save_dir = os.path.join(dy_data_utils.image_dir, str(image_dir_name))
        if not os.path.exists(image_save_dir):
            os.makedirs(image_save_dir)

        if use_image_group_num:
            filename = os.path.splitext(os.path.basename(image_path))[0]
            save_name = f"{filename.split('_')[0]}_{filename.split('_')[1]}_{image_md5}"
        else:
            save_name = f"{group_num}_{i + 1}_{image_md5}"

        shutil.copy(image_path, os.path.join(image_save_dir, f"{save_name}.jpg"))
        for j in range(1, len(filenames) // image_num):
            compose_save_dir = os.path.join(dy_data_utils.compose_dir, f"{compose_name}_{j}")
            if not os.path.exists(compose_save_dir):
                os.makedirs(compose_save_dir)

            compose_save_path = os.path.join(compose_save_dir, f"{save_name}.jpg")
            shutil.copy(os.path.join(dir, filenames[j*image_num + i]), compose_save_path)

    # 生成模板png
    for compose_dir in os.listdir(dy_data_utils.compose_dir):
        if str(compose_dir).startswith(compose_name):
            empty_image = np.ones((256, 256, 3), dtype=np.uint8) * 255
            text_writer = TextWriter(title_content=str(compose_dir), text_font_path=os.path.join(dy_data_utils.fonts_dir, "1.ttf"), text_color=(0, 0, 255))
            empty_image = text_writer.add_title_text(empty_image, "CENTER")
            cv2.imwrite(os.path.join(dy_data_utils.compose_dir, compose_dir, "模板示例.PNG"), empty_image)

