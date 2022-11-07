import os
import cv2
import json
import math
import datetime
import slugify
import numpy as np
from data_util import *
import scripts.image_aug as image_op


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


def instantiate_op(name, image, **kwargs):
    names = name.strip().split('.')
    for n in names:
        classname = image_op.__dict__[n]
    return classname(image, **kwargs)


def image_process(image, operate_list):
    for op, param in operate_list.items():
        image = instantiate_op(op, image, **param)

    return image



def boxes_add(image_compose, current_image_list, boxes):
    for box in boxes:
        x1 = box['box'][0]
        y1 = box['box'][1]
        x2 = box['box'][2] + 1
        y2 = box['box'][3] + 1

        # 图像短边按照边框长边缩放
        box_max = math.ceil(max(x2 - x1, y2 - y1))
        image = read_resize(current_image_list[box['image_index']], box_max)

        if "operate" in box:
            image = image_process(image, box['operate'])

        # 按照box大小中心裁剪 贴图
        image_compose[y1:y2, x1:x2, :] = center_crop_image(image, x1, y1, x2, y2)
    return image_compose


def transparent_add(image_compose, template_image, opacity):
    # cv2.imshow("image_compose", image_compose)
    # cv2.imshow("template_image", template_image[..., 0:3])
    # compose_mask = np.ones_like(image_compose)
    # aa = np.concatenate((image_compose, compose_mask))
    mask = template_image[:, :, 3]
    mask[mask > 0] = 255
    mask[mask <= 0] = 0
    mask = np.uint8(mask)
    mask = mask / 255.0

    blend_image = cv2.addWeighted(image_compose, 1- opacity, template_image[..., 0:3], opacity, 1)
    output = blend_image * (mask[:, :, None]) + image_compose * (1.0 - mask[:, :, None])
    output = output.astype(np.uint8)

    return output

def compose_mask_image(template_image, current_image_list, boxes):
    image_compose = np.zeros_like(template_image)
    image_compose = image_compose[:, :, 0:3]

    image_compose = boxes_add(image_compose, current_image_list, boxes)


    mask = template_image[:, :, 3]
    mask[mask > 0] = 255
    mask[mask <= 0] = 0
    mask = np.uint8(mask)
    mask = mask / 255.0

    output = template_image[:, :, 0:3] * (mask[:, :, None]) + image_compose * (1.0 - mask[:, :, None])
    output = output.astype(np.uint8)
    return output


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


        for current_image_list in split_image_list:
            output = compose_mask_image(template_image, current_image_list, boxes)
            # print(os.path.join(save_dir, "zzzzzzz_" + slugify.slugify(str(datetime.datetime.now())) + ".jpg"))
            cv2.imwrite(os.path.join(save_dir, "zzzzzzz_" + slugify.slugify(str(datetime.datetime.now())) + ".jpg"), output)
            # cv2.imshow("mask", mask)
            # # cv2.imshow("image_compose", image_compose)
            # # cv2.imshow("template_image", template_image)
            # # cv2.imshow("template_mask", template_mask)
            # cv2.imshow("output_im", output)
            # cv2.waitKey(-1)


# def with_bg_generate(template_list, image_list, save_dir):
#     for template_path in template_list:
#         template_image = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
#         # template_mask = cv2.imread(template_path.replace(".png", "_mask.jpg"), cv2.IMREAD_UNCHANGED)
#         config_path = template_path.replace(".png", ".config")
#         with open(config_path) as f:
#             data = json.load(f)
#
#         image_num = data['img_num']
#         split_image_list = chunk_list(image_list, image_num)
#
#         for current_image_list in split_image_list:
#             blend_list = data['blend']
#
#             image_compose = np.zeros_like(template_image)
#             image_compose = image_compose[:, :, 0:3]
#
#             for blend in blend_list:
#                 blend_mode = blend['blend_mode']
#
#                 if blend_mode == "normal":
#                     image_compose = boxes_add(image_compose, current_image_list, blend["boxes"])
#
#                 if blend_mode == "transparent_add":
#                     image_compose = transparent_add(image_compose, template_image, blend['opacity'])
#                     show = cv2.resize(image_compose, (600, 600))
#                     cv2.imshow("transparent_add", image_compose)
#                     cv2.waitKey(-1)




if __name__ == "__main__":
    image_dir = "/Users/meitu/Downloads/save3"
    save_dir = "/Users/meitu/Downloads/save3"

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    image_list = []
    for name in os.listdir(image_dir):
        print(str(os.path.splitext(name)[-1]).lower())
        if str(os.path.splitext(name)[-1]).lower() in [".jpg", ".jpeg", ".png"]:
            image_list.append(os.path.join(image_dir, name))

    image_list.sort()
    print(image_list)

    data_utils = DYDataUtils()
    common_generate(data_utils.common_template_list, image_list, save_dir)
    # with_bg_generate(data_utils.with_bg_template_list, image_list, save_dir)
