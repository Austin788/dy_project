import os
import hashlib

class DYDataUtils():
    def __init__(self, data_root):
        self.data_root = data_root

    @property
    def image_dir(self):
        return os.path.join(self.data_root, "image")

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

    def get_avilable_group_num(self, type):
        image_dir = os.path.join(self.data_root, "image", type)
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


class InfiniteIterator():
    def __init__(self, iter_container):
        self.iter_container = iter_container
        self.index = -1

    def next(self):
        self.index += 1
        if self.index >= len(self.iter_container):
            self.index = 0
        return self.iter_container[self.index]


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