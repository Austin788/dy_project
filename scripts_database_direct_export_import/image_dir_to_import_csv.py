import os
import json

'''
1=>'壁纸',
        2=>'动态壁纸',
        3=>'背景图',
        4=>'头像',
        5=>'表情包',
        
user_id 
80 18396185253
81 15880650619
82 13771417931
'''
def prepare_dict(image_dir, url_json):
    with open(url_json) as f:
        data = json.load(f)

    data_list = []
    for filename in os.listdir(image_dir):
        data_list.append(data[filename])

    return data_list


def export_csv(data_list, name, author_id):
    for data in data_list:
        data['name'] = name
        data['id'] = ''
        data['author_id'] = author_id


if __name__ == "__main__":
    dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data/素材库/llqt/2023_02_06_14_43_55/御姐头像"
    json_path = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data/素材库/llqt/2023_02_06_14_43_55/filename_url.json"

    data_list = prepare_dict(dir, )