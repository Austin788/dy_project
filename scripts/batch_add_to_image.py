import os
import shutil
from data_util import md5, DYDataUtils


if __name__ == "__main__":
    dir = "/Users/meitu/Documents/midlife_crisis/project/待添加素材/8.19男头原图"
    export_type = "男生头像"

    dy_data_utils = DYDataUtils()

    group_num = dy_data_utils.get_avilable_group_num(export_type)
    for count, filename in enumerate(os.listdir(dir)):
        file_path = os.path.join(dir, filename)

        image_md5 = md5(file_path)
        save_name = f"{group_num}_{count + 1}_{image_md5}"
        shutil.copy(file_path, os.path.join(dy_data_utils.image_dir, str(export_type), f"{save_name}.jpg"))