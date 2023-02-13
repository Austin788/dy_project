import os
from data_util import *
import cv2
import numpy as np
from generate_video import *


def image_to_group(image_dirs, each_group_img_num):
    filenames = []
    for filename in os.listdir(image_dirs):
        if is_image(filename):
            filenames.append(filename)

    filenames.sort()

    group_dict = {}

    for filename in filenames:
        group = filename.split("_")[0]
        if group not in group_dict:
            group_dict[group] = []
        group_dict[group].append(filename)

    image_group_list = []
    current_list = []

    while True:
        success = False
        for key, value in group_dict.items():
            if len(value) == 0:
                continue
            current_list.append(os.path.join(image_dirs, value[0]))
            group_dict[key].remove(value[0])
            if len(current_list) == each_group_img_num:
                image_group_list.append(current_list)
                current_list = []
                success = True

        if not success:
            break

    return image_group_list



def image_list_to_compose_list(image_list, compose_name):
    compose_list = []
    for image_path in image_list:
        compose_list.append(os.path.join(os.path.dirname(image_path.replace("/image/", "/image_compose/")), compose_name, os.path.basename(image_path)))
    return compose_list

if __name__ == "__main__":
    data_utils = DYDataUtils("/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/")
    image_dirs = data_utils.image_dir
    music_path = os.path.join(data_utils.music_dir, "2秒一张11张图.mp3")

    title_content = ['我的女儿 希望你善良中带点锋芒']
    font = os.path.join(data_utils.fonts_dir, '新青年体.ttf')
    text_color = (0, 0, 0)
    title_position = 'TOP'

    # title_content = None
    # font = None
    # text_color = (0, 255, 255)
    # title_position = 'TOP'

    image_groups = image_to_group(image_dirs, each_group_img_num=11)

    compose_lists = os.listdir(data_utils.compose_dir)

    device_list = data_utils.device_ids
    count = 0
    try:
        for image_list in image_groups:
            for compose_name in compose_lists:
                save_dir = os.path.join(data_utils.device_dir, device_list[count % len(device_list)], "未发送")
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                mp4_name = f"{list_md5(image_list)}_{compose_name}_{os.path.splitext(os.path.basename(music_path))[0]}.mp4"
                save_path = os.path.join(save_dir, mp4_name)
                if os.path.exists(save_path):
                    print(f"{save_path} exist! continue!")
                    continue
                compose_list = image_list_to_compose_list(image_list, compose_name)

                parmater = {'music_path': music_path, 'stuck_points_path': music_path.replace(".mp3", ".json"), 'image_paths': image_list, 'compose_paths': compose_list,
                        'save_path': save_path, 'title_content': title_content, 'text_font_path': font, 'text_color': text_color, 'title_position': title_position,
                            'video_type': 'slide'}

                print(parmater)
                generate_video_image_compose_compose(**parmater)
                exit(0)
                count += 1
    except KeyboardInterrupt:
        os.remove(save_path)
