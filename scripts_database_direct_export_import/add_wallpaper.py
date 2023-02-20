import cv2
import os
import time
from scripts_database_direct_export_import.count_include_cdn_sites import get_sites, include_sites
from scripts_database_direct_export_import.mysql_helper import MysqlHelper
from colorama import Fore


def get_urls(txt):
    with open(txt) as f:
        lines = f.readlines()

    urls = []
    for line in lines:
        url = line.strip("\n")
        urls.append(url)
    return urls

def load_already_save(txt_path):
    if not os.path.exists(txt_path):
        return set()
    with open(txt_path) as f:
        lines = f.readlines()
    urls = set()
    for line in lines:
        urls.add(line.strip('\n'))
    return urls

if __name__ == "__main__":
    base_dir = "/Users/meitu/Documents/midlife_crisis/素材列表/"


    # txt = f"{base_dir}/小野啊表情包.txt"
    # expert_id = "628" # hua5ban 631 甜七 630 梓萱 629 小野啊表情包 628
    # tag_name = '超火表情包'
    # type = 5 # 资源类型 1-手机壁纸 2-动态壁纸 3-背景图 4-头像 5-表情包

    # txt = f"{base_dir}/甜七.txt"
    # expert_id = "630"  # hua5ban 631 甜七 630 梓萱 629 小野啊表情包 628
    # tag_name = '可爱头像'
    # type = 4  # 资源类型 1-手机壁纸 2-动态壁纸 3-背景图 4-头像 5-表情包

    # txt = f"{base_dir}/hua5ban.txt"
    # expert_id = "631"  # hua5ban 631 甜七 630 梓萱 629 小野啊表情包 628
    # tag_name = '超火头像'
    # type = 4  # 资源类型 1-手机壁纸 2-动态壁纸 3-背景图 4-头像 5-表情包

    # txt = f"{base_dir}/蓁蓁和菁菁头像.txt"
    # expert_id = "631"  # hua5ban 631 甜七 630 梓萱 629 小野啊表情包 628
    # tag_name = '超火头像'
    # type = 4  # 资源类型 1-手机壁纸 2-动态壁纸 3-背景图 4-头像 5-表情包
    #
    txt = f"{base_dir}/梓萱壁纸.txt"
    expert_id = "629"  # hua5ban 631 甜七 630 梓萱 629 小野啊表情包 628
    tag_name = '超火壁纸'
    type = 1  # 资源类型 1-手机壁纸 2-动态壁纸 3-背景图 4-头像 5-表情包

    print(txt)

    cztk_mysqlhelper = MysqlHelper(MysqlHelper.cztk_conn_params)

    already_save_urls = load_already_save(os.path.join(base_dir, str(expert_id)+".txt"))
    urls = get_urls(txt)
    with open(os.path.join(base_dir, str(expert_id)+".txt"), "a+") as f:
        for url in urls:
            if url in already_save_urls:
                print(Fore.RED + f"{url} already save!")
                continue

            if get_sites(url) not in include_sites:
                print(Fore.RED + f"{url} not in include site!")
                continue

            data = {}
            data['cate_id'] = 0  # 不知道是什么
            data['name'] = "sc2022111233372042"
            data['img'] = url
            data['type'] = type
            data['author_id'] = expert_id
            # data['show_index'] = "0"
            # data['is_deleted'] = "0"
            # data['created_at'] = 0
            # data['updated_at'] = 0
            # data['is_recommend'] = 0
            # data['download_count'] = 0
            data['source'] = 2 # 1后台上传显示不了 2 达人上传
            data['status'] = 1 # 状态 1-已通过 2-审核中 3-未通过 4-下架
            data['video_url'] = url
            # data['tag_ids'] = ""
            data['thumb_img'] = url
            data['weight'] = 0
            # data['expression_video_url'] = ""
            # data['expression_show_video'] = 0
            data['self_name'] = tag_name

            cztk_mysqlhelper.insert('qqxcx_wallpaper', data)
            print(Fore.BLACK + f"insert {url}")

            f.write(url)
            f.write('\n')
