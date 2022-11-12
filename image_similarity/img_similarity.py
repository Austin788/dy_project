import sys
import os
import cv2
import shutil
from image_similarity.main_multi import ImageSimilarity, DeepModel
import glob

"""
用户文件夹中图片相似性，防止图片重复，按左右删除，会删除整个文件夹
"""


class NewImageSimilarity(ImageSimilarity):
    @staticmethod
    def _sub_process(para):
        # Override the method from the base class
        path, fields = para['path'], para['fields']
        try:
            feature = DeepModel.preprocess_image(path)
            return feature, fields

        except Exception as e:
            print('Error file %s: %s' % (fields[0], e))

        return None, None

# def get_csv(foler_name_list, save_path):
#     path_list = []
#     with open(save_path, "w") as f:
#         f.write("id,path\n")
#         count = 1
#         for foler_name in foler_name_list:
#             for dir_path, _, filenames in os.walk(foler_name):
#                 for filename in filenames:
#                     if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
#                         path = os.path.join(dir_path, filename)
#                         f.write(f"{count},{path}\n")
#                         path_list.append(path)
#                         count += 1
#     return path_list


def get_csv(filenames, save_path):
    path_list = []
    with open(save_path, "w") as f:
        f.write("id,path\n")
        count = 1

        for path in filenames:
            if str.lower(os.path.splitext(path)[-1]) in [".jpg", ".png", ".jpeg"]:
                f.write(f"{count},{path}\n")
                path_list.append(path)
                count += 1

    return path_list


def get_comment(path):
    if not os.path.isdir(path):
        path = os.path.dirname(path)

    txt_path = os.path.join(path, path.split("/")[-1]+".txt")
    if os.path.exists(txt_path):
        with open(txt_path) as f:
            line = f.readline()
            return line
    else:
        txt_path = os.path.join(path, "首次评价.txt")
        if os.path.exists(txt_path):
            with open(txt_path) as f:
                line = f.readline()
                return line
        else:
            return ""


def similarity_remove(path, threadhold = 0.845):
    # datapath
    img_path_list = []
    for filename in os.listdir(path):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            img_path_list.append(os.path.join(path, filename))


    csv_path = './test2.csv'

    path_list = get_csv(img_path_list, csv_path)

    similarity = NewImageSimilarity()

    '''Setup'''
    similarity.batch_size = 16
    similarity.num_processes = 2

    '''Load source data'''
    test1 = similarity.load_data_csv(csv_path, delimiter=',', cols=['id', 'path'])
    test2 = similarity.load_data_csv(csv_path, delimiter=',', cols=['id', 'path'])

    '''Save features and fields'''
    similarity.save_data('test1', test1)
    similarity.save_data('test2', test2)

    '''Calculate similarities'''
    result = similarity.iteration(['test1_id', 'test1_url', 'test2_id', 'test2_url'], thresh=0.845)
    print('Row for source file 1, and column for source file 2.')
    print(result)

    for i, path in enumerate(path_list):
        sim_rows = result[i]
        for j, value in enumerate(sim_rows):
            if j > i and value > threadhold:


                print(f"{path_list[i]} and {path_list[j]} similarity > threadhold")
                # try:
                if os.path.exists(path_list[i]) and os.path.exists(path_list[j]):
                    image1 = cv2.imread(path_list[i])
                    image2 = cv2.imread(path_list[j])
                    image1 = cv2.resize(image1, (600, 600))
                    image2 = cv2.resize(image2, (600, 600))
                    cv2.imshow("image1", image1)
                    cv2.imshow("image2", image2)
                    key = cv2.waitKey()
                    print(key)

                    if key == 2 and os.path.exists(path_list[i]):
                        # shutil.rmtree(os.path.dirname(path_list[i]))
                        # 删除图片
                        print("os remove:", path_list[i])
                        os.remove(path_list[i])

                    elif key == 3 and os.path.exists(path_list[j]):
                        # shutil.rmtree(os.path.dirname(path_list[j]))
                        # 删除图片
                        print("os remove:", path_list[j])
                        os.remove(path_list[j])

                # except:
                #     print("happen except!!", path_list[i], path_list[j])



def group_by_similarity(path, save_dir, threadhold = 0.9):
    # datapath
    img_path_list = []
    for filename in os.listdir(path):
        if str.lower(os.path.splitext(filename)[-1]) in [".jpg", ".png", ".jpeg"]:
            img_path_list.append(os.path.join(path, filename))


    csv_path = './test2.csv'

    path_list = get_csv(img_path_list, csv_path)

    similarity = NewImageSimilarity()

    '''Setup'''
    similarity.batch_size = 16
    similarity.num_processes = 2

    '''Load source data'''
    test1 = similarity.load_data_csv(csv_path, delimiter=',', cols=['id', 'path'])
    test2 = similarity.load_data_csv(csv_path, delimiter=',', cols=['id', 'path'])

    '''Save features and fields'''
    similarity.save_data('test1', test1)
    similarity.save_data('test2', test2)

    '''Calculate similarities'''
    result = similarity.iteration(['test1_id', 'test1_url', 'test2_id', 'test2_url'], thresh=0.845)
    print('Row for source file 1, and column for source file 2.')
    print(result)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    group = 0

    for i, path in enumerate(path_list):
        sim_rows = result[i]
        group += 1
        group_internal = 0
        if os.path.exists(path_list[i]):
            shutil.move(path_list[i], os.path.join(save_dir, f"{group}_{group_internal}.jpg"))
            group_internal += 1

        sim_rows_dict = {}
        for j, value in enumerate(sim_rows):
            sim_rows_dict[j] = value

        sim_rows_dict = sorted(sim_rows_dict.items(), key=lambda x: x[1], reverse=True)
        for j, value in sim_rows_dict:
            if value > threadhold:
                if os.path.exists(path_list[j]):
                    print(f"{path_list[i]} and {path_list[j]} similarity > threadhold")
                    shutil.move(path_list[j], os.path.join(save_dir, f"{group}_{group_internal}.jpg"))
                    group_internal += 1


if __name__ == "__main__":
    group_by_similarity("/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/素材库/亲子头像",
                        "/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/素材库/亲子头像_分组")
    # similarity_remove("/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/素材库/亲子头像", threadhold=0.95)
