import os
import hashlib

class DYDataUtils():
    def __init__(self, data_root):
        self.data_root = data_root

    def get_image_dir(self):
        return os.path.join(self.data_root, "image")

    def get_effects_dir(self):
        return os.path.join(self.data_root, "image_effects")

    def get_compose_dir(self):
        return os.path.join(self.data_root, "image_compose")


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


    def get_effects_ids(self):
        image_dir = os.path.join(self.data_root, "image_effects")
        return DYDataUtils.get_dir_names(image_dir)


    def get_compose_ids_pathes(self):
        image_dir = os.path.join(self.data_root, "image_compose")
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


if __name__ == "__main__":
    data_root = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data"
    data_utils = DYDataUtils(data_root)
    print(data_utils.get_avilable_group_num("女生头像"))

    print(md5("/Users/meitu/Downloads/8.13/1-1/1-1.jpg"))
    exit(0)

    from gui_add_data import ListImageSelector
    image_selector = ListImageSelector("/Users/meitu/Downloads/8.13/1-1/1-1.jpg", data_utils.get_compose_ids_pathes())
    image_selector.mainloop()