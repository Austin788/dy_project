import os
import shutil
from data_util import md5, DYDataUtils


if __name__ == "__main__":
    dir = "/Users/meitu/Downloads/8.30/女原图"

    image_dir_name = "女生职业头像"
    compse_dir_name = "ZZ-1802@图片更换DZZS@7127585333067189534"
    effect_dir_name = "摇摆运镜"

    dy_data_utils = DYDataUtils()

    if not os.path.exists(os.path.join(dy_data_utils.image_dir, str(image_dir_name))):
        os.makedirs(os.path.join(dy_data_utils.image_dir, str(image_dir_name)))

    group_num = dy_data_utils.get_avilable_group_num(image_dir_name)

    deal_set = set()
    for count, filename in enumerate(os.listdir(dir)):

        id = filename.split("-")[0]
        if id in deal_set:
            continue
        else:
            deal_set.add(id)

        image_name = f"{id}-1.jpg"
        compose_name = f"{id}-2.jpg"
        effect_name = f"{id}-3.mp4"

        image_path = os.path.join(dir, image_name)
        compose_path = os.path.join(dir, compose_name)
        effect_path = os.path.join(dir, effect_name)

        image_md5 = md5(image_path)
        save_name = f"{group_num}_{count + 1}_{image_md5}"

        if os.path.exists(image_path) and os.path.exists(compose_path) and os.path.exists(effect_path):
            shutil.copy(image_path, os.path.join(dy_data_utils.image_dir, str(image_dir_name), f"{save_name}.jpg"))
            shutil.copy(compose_path, os.path.join(dy_data_utils.compose_dir, str(compse_dir_name), f"{save_name}.jpg"))
            shutil.copy(effect_path, os.path.join(dy_data_utils.effects_dir, str(effect_dir_name), f"{save_name}.mp4"))

            os.remove(image_path)
            os.remove(compose_path)
            os.remove(effect_path)