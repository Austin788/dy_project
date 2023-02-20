
from wcmatch import pathlib


def get_sites(filename):
    index = filename.find("/", 9)
    filename = filename[:index]
    return filename


def get_bussiness_site(lines, sites):
    for i, filename in enumerate(lines):
        filename = get_sites(filename)
        if filename not in sites:
            sites[filename] = 0
        sites[filename] = sites[filename] + 1
    return sites


include_sites = ['http://img-pushpic-creator.doutuimao.net',
'https://cdn-ali-img-shdiy.shanhutech.cn',
'https://dimg04.c-ctrip.com',
'https://p1.meituan.net',
'https://dingyue.ws.126.net',
'https://img-pushpic-creator.doutuimao.net',
'https://img10.360buyimg.com',
'https://img11.360buyimg.com',
'https://p7.qhimg.com',
'https://p0.qhimg.com',
'https://img12.360buyimg.com',
'https://p4.qhimg.com',
'https://img13.360buyimg.com',
'https://store.heytapimage.com',
'https://img14.360buyimg.com',
'https://p9.qhimg.com',
'https://p1.qhimg.com',
'https://p6.qhimg.com',
'https://p3.qhimg.com',
'https://p5.qhimg.com',
'https://p2.qhimg.com',
'https://p8.qhimg.com',]

if __name__ == "__main__":


    txt_dir = "/Users/meitu/Documents/midlife_crisis/素材列表/"

    sites = {}
    for txt_path in pathlib.Path(txt_dir).rglob("*.txt"):

        with open(txt_path) as f:
            lines = f.readlines()

        image_list = [line.strip('\n') for line in lines]

        get_bussiness_site(lines, sites)
    sites = sorted(sites.items(), key=lambda d: d[1], reverse=True)

    min_size = 25
    # print(sites)
    for value in sites:
        if value[1] >= min_size:
            print(f"'{value[0]}',")
    # exit(0)
