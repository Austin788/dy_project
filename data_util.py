import os
import hashlib
import yaml

class DYDataUtils():
    def __init__(self, data_root=os.path.join(os.path.dirname(__file__), "data")):
        self.data_root = data_root

    @property
    def image_dir(self):
        return os.path.join(self.data_root, "image")

    @property
    def upload_dir(self):
        return os.path.join(self.data_root, "upload_images")

    @property
    def effects_dir(self):
        return os.path.join(self.data_root, "image_effects")

    @property
    def compose_dir(self):
        return os.path.join(self.data_root, "image_compose")

    @property
    def music_dir(self):
        return os.path.join(self.data_root, "music")

    @property
    def video_dir(self):
        return os.path.join(self.data_root, "video")

    @property
    def fonts_dir(self):
        return os.path.join(self.data_root, "fonts")

    @property
    def device_dir(self):
        return os.path.join(self.data_root, "device")

    @property
    def compose_template_dir(self):
        return os.path.join(self.data_root, "template")

    @property
    def common_template_list(self):
        common_list = [
            'cheer.png',
            '小象.png',
            '眠.png',
            '白底简约微信头像模板.png',
            '简约白底头像cheer.png',
            '普通白底模板.png',
            '白底头像框2.png',
            '白底简约立体头像模板(weeks).png'
        ]
        return [os.path.join(self.data_root, "template", name) for name in common_list]

    @property
    def couple_template_list(self):
        common_list = [
            '情侣6图.png',
        ]
        return [os.path.join(self.data_root, "template", name) for name in common_list]

    @property
    def with_bg_template_list(self):
        common_list = [
            '头像模板透明模板文字图片可改.png'
        ]
        return [os.path.join(self.data_root, "template", name) for name in common_list]


    @staticmethod
    def get_dir_names(path):
        dir_lists = []
        for dir_name in os.listdir(path):
            if os.path.isdir(os.path.join(path, dir_name)):
                dir_lists.append(dir_name)
        return dir_lists


    def get_image_type_list(self):
        image_dir = os.path.join(self.data_root, "image")
        return DYDataUtils.get_dir_names(image_dir)

    @property
    def effects_ids(self):
        image_dir = os.path.join(self.data_root, "image_effects")
        return DYDataUtils.get_dir_names(image_dir)

    @property
    def compose_ids(self):
        image_dir = os.path.join(self.data_root, "image_compose")
        return DYDataUtils.get_dir_names(image_dir)

    @property
    def device_ids(self):
        devices = []

        for dir in os.listdir(self.device_dir):
            if os.path.isdir(os.path.join(self.device_dir, dir)):
               devices.append(dir)
        return devices

    def get_compose_ids_pathes(self):
        image_dir = self.compose_dir
        id_pathes = {}

        for dir in os.listdir(image_dir):
            if os.path.isdir(os.path.join(image_dir, dir)):
                template_path = os.path.join(image_dir, dir, "模板示例.PNG")
                if os.path.exists(template_path):
                    id_pathes[dir] = template_path
                else:
                    raise ValueError(f"file 模板示例.PNG 在{dir}不存在，请进行添加！")
        return id_pathes

    def get_avilable_group_num(self, type, data_root=None):
        if data_root is None:
            data_root = self.data_root
        image_dir = os.path.join(data_root, "image", type)
        if not os.path.exists(image_dir):
            return 1
        group_list = []
        for image_name in os.listdir(image_dir):
            if image_name.startswith("."):
                continue
            if image_name.find("_") != -1:
                group_num = int(image_name.split("_")[0])
                group_list.append(group_num)
        if len(group_list) == 0:
            return 1
        return max(group_list) + 1


def md5(file_path):
    file = open(file_path, "rb")
    md = hashlib.md5()
    md.update(file.read())
    res1 = md.hexdigest()
    return res1


def list_md5(obj_list):
    md = hashlib.md5("".join(obj_list).encode("utf-8"))
    res1 = md.hexdigest()
    return res1


class InfiniteIterator():
    def __init__(self, iter_container):
        self.iter_container = iter_container
        self.index = -1

    def next(self):
        self.index += 1
        if self.index >= len(self.iter_container):
            self.index = 0
        return self.iter_container[self.index]

class UploadConfig():
    def __init__(self):
        self.data = yaml.load(open("config.yml", mode='r', encoding='utf-8'))

    def get_upload(self, device_name):
        upload_config = self.data["upload_config"]
        for key, value in upload_config.items():
            if device_name in value:
                return key
        return None


def chunks(l, n):
   """Yield successive n-sized chunks from l."""
   for i in range(0, len(l), n):
        yield l[i:i + n]


def is_image(filename):
    if str.lower(os.path.splitext(filename)[-1]) in ['.jpg', '.jpeg', '.png']:
        return True
    else:
        return False


if __name__ == "__main__":
    data_root = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data"
    data_utils = DYDataUtils(data_root)
    print(data_utils.get_fonts_dir)

    print(data_utils.get_avilable_group_num("女生头像"))

    print(md5("/Users/meitu/Downloads/8.13/1-1/1-1.jpg"))
    exit(0)

    from gui_add_data import ListImageSelector
    image_selector = ListImageSelector("/Users/meitu/Downloads/8.13/1-1/1-1.jpg", data_utils.get_compose_ids_pathes())
    image_selector.mainloop()