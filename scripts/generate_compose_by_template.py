import os
import cv2
import json
import math
import datetime
import numpy as np
from data_util import *


def chunk_list(list_array, chunk_num):
    split_array = []
    current_array = []

    for i in range(len(list_array)):
        current_array.append(list_array[i])
        if len(current_array) == chunk_num:
            split_array.append(current_array)
            current_array = []
    return split_array


def read_resize(path, min_edge):
    image = cv2.imread(path)
    height, width, _ = image.shape
    if width > height:
        width = math.ceil(width / height * min_edge)
        image = cv2.resize(image, (width, min_edge))
    else:
        height = math.ceil(height / width * min_edge)
        image = cv2.resize(image, (min_edge, height))
    return image


def center_crop_image(image, x1, y1, x2, y2):
    height, width, _ = image.shape

    box_width = x2 - x1
    box_height = y2 - y1

    start_x = max(math.floor(image.shape[1] / 2 - box_width / 2), 0)
    start_y = max(math.floor(image.shape[0] / 2 - box_height / 2), 0)
    return image[start_y: start_y + box_height, start_x: start_x + box_width, :]


def common_generate(template_list, image_list, save_dir):
    for template_path in template_list:
        template_image = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
        # template_mask = cv2.imread(template_path.replace(".png", "_mask.jpg"), cv2.IMREAD_UNCHANGED)
        config_path = template_path.replace(".png", ".config")
        with open(config_path) as f:
            data = json.load(f)

        image_num = data['img_num']
        boxes = data['boxes']
        split_image_list = chunk_list(image_list, image_num)

        image_compose = np.zeros_like(template_image)
        image_compose = image_compose[:, :, 0:3]

        for current_image_list in split_image_list:
            for box in boxes:
                x1 = box['box'][0] - 1
                y1 = box['box'][1] - 1
                x2 = box['box'][2] + 2
                y2 = box['box'][3] + 2

                # 图像短边按照边框长边缩放
                box_max = math.ceil(max(x2 - x1, y2 - y1))
                image = read_resize(current_image_list[box['image_index']], box_max)

                # 按照box大小中心裁剪 贴图
                image_compose[y1:y2, x1:x2, :] = center_crop_image(image, x1, y1, x2, y2)


            mask = template_image[:, :, 3]
            mask[mask > 0] = 255
            mask[mask <= 0] = 0
            mask = np.uint8(mask)
            mask = mask / 255.0


            output = template_image[:, :, 0:3] * (mask[:, :, None]) + image_compose * (1.0 - mask[:, :, None])
            output = output.astype(np.uint8)
            cv2.imwrite(os.path.join(save_dir, str(datetime.datetime.now()) + ".jpg"), output)
            # cv2.imshow("mask", mask)
            # # cv2.imshow("image_compose", image_compose)
            # # cv2.imshow("template_image", template_image)
            # # cv2.imshow("template_mask", template_mask)
            # cv2.imshow("output_im", output)
            # cv2.waitKey(-1)






if __name__ == "__main__":
    image_dir = "/Users/meitu/Downloads/image/用所选项目新建的文件夹"
    image_list = []
    for name in os.listdir(image_dir):
        if name.endswith(".jpg") or name.endswith(".jpeg") or name.endswith(".png"):
            image_list.append(os.path.join(image_dir, name))

    image_list.sort()

    data_utils = DYDataUtils()
    common_generate(data_utils.common_template_list, image_list, image_dir)
