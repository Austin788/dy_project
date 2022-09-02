# -*- encoding=utf-8 -*-
import random
from tkinter import filedialog
from tkinter import *
from gui_util import *
from data_util import *
from tkinter import messagebox as msg
import itertools
import shutil
from generate_video import generate_single_video
from wcmatch import pathlib
from itertools_util import permutations, combinations


class ComposeVideo(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        # win = tk.Tk()  # 窗口
        self.title('')  # 标题
        screenwidth = self.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.winfo_screenheight()  # 屏幕高度
        width = screenwidth
        height = screenheight
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)

        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

        self.data_dir = os.path.join(os.path.dirname(__file__), "data_fast")
        self.default_source = "/Users/meitu/Downloads/8.13/1-1/"
        self.dy_data_utils = DYDataUtils(self.data_dir)
        types = self.dy_data_utils.get_image_type_list()

        self.group_num = tk.IntVar()
        self.type_value = tk.StringVar(self)
        self.export_type_value = tk.StringVar(self)

        button_width = 15
        tk.Label(self, text="操作:").grid(row=0, column=0, padx=10, pady=10)
        self.exchange_checkbtn_num = tk.IntVar(value=0)
        self.exchange_checkbtn = tk.Checkbutton(self, text="是否交换图片顺序", variable=self.exchange_checkbtn_num, onvalue=1, offvalue=0, width=button_width)
        self.exchange_checkbtn.grid(row=0, column=1)

        self.keep_first_image = tk.IntVar(value=0)
        tk.Checkbutton(self, text="是否保持首图不变", variable=self.keep_first_image, onvalue=1,
                                                offvalue=0, width=button_width).grid(row=1, column=1)

        self.img_num_per_video = tk.IntVar(value=3)
        tk.Label(self, text="视频图片数:").grid(row=0, column=2, padx=10, pady=10)
        tk.Entry(self, textvariable=self.img_num_per_video, width=5).grid(row=0, column=3)

        self.export_video_num = tk.IntVar(value=9999)
        tk.Label(self, text="导出视频数:").grid(row=0, column=4, padx=10, pady=10)
        tk.Entry(self, textvariable=self.export_video_num, width=5).grid(row=0, column=5)

        self.skip_export_exists = tk.IntVar(value=1)
        tk.Checkbutton(self, text="已经存在不导出", variable=self.skip_export_exists, onvalue=1,
                                                offvalue=0, width=button_width).grid(row=0, column=6)

        self.max_image_num_total_video = tk.IntVar(value=1)
        tk.Label(self, text="每张图片最多使用次数:").grid(row=0, column=7)
        tk.Entry(self, textvariable=self.max_image_num_total_video, width=5).grid(row=0, column=8)

        self.export_btn = tk.Button(self, text="导出", command=self.export, width=button_width)
        self.export_btn.grid(row=0, column=9, pady=10)

        self.add_image_btn = tk.Button(self, text="选择音乐", command=self.select_music, width=int(button_width/2))
        self.add_image_btn.grid(row=3, column=0, padx=10, pady=10)
        self.add_image_btn = tk.Button(self, text="删除音乐", command=self.delete_music, width=int(button_width/2))
        self.add_image_btn.grid(row=3, column=1)
        self.add_effect_btn = tk.Button(self, text="选择视频", command=self.select_video, width=button_width)
        self.add_effect_btn.grid(row=3, column=2, columnspan=2)
        self.add_compose_btn = tk.Button(self, text="选择图片", command=self.select_image, width=button_width)
        self.add_compose_btn.grid(row=3, column=4, columnspan=2)
        self.complete_current_btn = tk.Button(self, text="选择特效", command=self.select_effects, width=10)
        self.complete_current_btn.grid(row=3, column=6)
        self.complete_all_btn = tk.Button(self, text="选择合成", command=self.select_compose, width=button_width)
        self.complete_all_btn.grid(row=3, column=7, columnspan=2)
        self.complete_all_btn = tk.Button(self, text="选择导出设备", command=None, width=button_width)
        self.complete_all_btn.grid(row=3, column=9)

        # 音乐列表
        self.music_list_box = tk.Listbox(self, cursor='arrow', selectborderwidth=2, selectmode=MULTIPLE)
        self.music_list_box.grid(row=4, column=0, columnspan=2, sticky=NSEW, padx=10)
        self.music_list_box.configure(exportselection=False)

        # 热点视频列表
        self.video_list = ListImageManager(self)
        self.video_list.grid(row=4, column=2, columnspan=2, sticky=NSEW, padx=10)

        # 图片列表
        self.image_list = ListImageManager(self)
        self.image_list.grid(row=4, column=4, columnspan=2, sticky=NSEW, padx=10)

        # 效果列表
        self.effects_items = tk.StringVar(value=self.dy_data_utils.effects_ids)
        self.effect_list_box = tk.Listbox(self, cursor='arrow', selectborderwidth=2, listvariable=self.effects_items, selectmode=MULTIPLE, width=10)
        self.effect_list_box.grid(row=4, column=6, sticky=NSEW, padx=10)
        self.effect_list_box.configure(exportselection=False)
        self.effect_list_box.select_set(0, END)

        # 合成列表
        self.compose_list = ListImageManager(self)
        self.compose_list.grid(row=4, column=7, columnspan=2, sticky=NSEW, padx=10)
        for key, value in self.dy_data_utils.get_compose_ids_pathes().items():
            self.compose_list.add_by_path(value)

        # 设备列表
        self.devices_items = tk.StringVar(value=self.dy_data_utils.device_ids)
        self.device_list_box = tk.Listbox(self, cursor='arrow', selectborderwidth=2, listvariable=self.devices_items,
                                           selectmode=MULTIPLE)
        self.device_list_box.grid(row=4, column=9, sticky=NSEW, padx=10)
        self.device_list_box.configure(exportselection=False)


    def select_music(self):
        music_pathes = tk.filedialog.askopenfiles(filetypes=[("Configuration file", "*.mp3")],
                                               initialdir=self.dy_data_utils.music_dir)

        for path in music_pathes:
            self.music_list_box.insert(END, os.path.basename(path.name))

    def delete_music(self):
        music_select_index = self.music_list_box.curselection()
        print(music_select_index)
        music_select_index = list(music_select_index)
        music_select_index.sort(reverse=True)
        for index in music_select_index:
            self.music_list_box.delete(index)

    def select_effects(self):
        pass

    def select_compose(self):
        pass

    def select_video(self):
        image_pathes = tk.filedialog.askopenfiles(filetypes=[("Configuration file", "*.mp4")],
                                                  initialdir=self.dy_data_utils.video_dir)

        for path in image_pathes:
            cap = cv2.VideoCapture(path.name)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret is not True:
                    msg.showinfo("警告", "打开视频失败！")
                    return

            self.video_list.add_by_cv_frame(frame, path.name)

    def select_image(self):
        image_pathes = tk.filedialog.askopenfiles(filetypes=[("Configuration file", "*.jpg")],
                                                  initialdir=self.dy_data_utils.image_dir)

        for path in image_pathes:
            self.image_list.add_by_path(str(path.name))

    def get_select_music_list(self):
        music_list = list(self.music_list_box.get(0, END))
        if music_list is None or len(music_list) == 0:
            msg.showerror("警告", "请选择音乐文件")
            return []

        for i in range(len(music_list)):
            music_list[i] = os.path.join(self.dy_data_utils.music_dir, music_list[i])

        return music_list

    def get_select_device_list(self):
        select_indexes = self.device_list_box.curselection()
        device_list = []
        for index in select_indexes:
            device_list.append(self.device_list_box.get(index))

        if device_list is None or len(device_list) == 0:
            msg.showerror("警告", "请至少选择一个导出设备")
            return []
        return list(device_list)

    def get_select_video_list(self):
        video_list = self.video_list.image_list
        if len(video_list) == 0:
            video_list = ['None']
        return video_list

    def get_select_image_list(self):
        img_num_per_video = self.img_num_per_video.get()
        max_image_num_total_video = self.max_image_num_total_video.get()
        keep_first_image = self.keep_first_image
        if img_num_per_video is None:
            msg.showerror("警告", "请选择需要添加的类别")
            return
        image_list = self.image_list.image_list

        if len(image_list) < 3:
            msg.showerror("警告", "请至少选择三张图片")
            return []


        if keep_first_image == 1:
            first_image_path = image_list[0]
            image_list = image_list[1:]
            img_num_per_video = img_num_per_video - 1

        if max_image_num_total_video == 1:
            image_list = list(chunks(image_list, img_num_per_video))
            if len(image_list) > 0:
                if len(image_list[len(image_list) - 1]) != max_image_num_total_video:
                    image_list = image_list[:-1]
        else:
            if self.exchange_checkbtn_num.get() == 1:
                image_list = list(permutations(image_list, img_num_per_video, max_image_num_total_video, max_num=100))  # 无序
            else:
                image_list = list(combinations(image_list, img_num_per_video, max_image_num_total_video, max_num=100))  # 有序

            if len(image_list) >= 100:
                random.shuffle(image_list)

        if keep_first_image == 1:
            for i in range(len(image_list)):
                image_list[i] = [first_image_path] + image_list[i]

        return image_list

    def get_select_effect_list(self):
        selects = self.effect_list_box.curselection()
        effect_names = []
        for index in selects:
            effect_names.append(self.effect_list_box.get(index))
        return effect_names


    def get_select_compose_list(self):
        compose_list = self.compose_list.image_list
        if len(compose_list) == 0:
            compose_list = ['None']
        return compose_list

    def convert_pathes(self, image_pathes, resouce_path, suffix=None):
        pathes = []
        for img_path in image_pathes:
            if suffix is None:
                path = os.path.join(resouce_path, os.path.basename(img_path))
            else:
                filename = os.path.basename(img_path)
                path = os.path.join(resouce_path, filename[:-4] + suffix)
            if not os.path.exists(path):
                print(f"not exists {path}")
                continue
            pathes.append(path)
        return pathes

    def get_export_resource_list(self, order_list=["video", 'image', 'effect', 'compose', 'music']):
        music_list = self.get_select_music_list()
        if len(music_list) == 0:
            return []

        video_list = self.get_select_video_list()

        image_list = self.get_select_image_list()
        if len(image_list) <= 0:
            return []

        effect_list = self.get_select_effect_list()
        if len(effect_list) <= 0:
            return []

        compose_list = self.get_select_compose_list()

        resource_dict = {'music': music_list, 'video': video_list, 'image': image_list, 'effect': effect_list,
                         'compose': compose_list}


        order_list.reverse()

        videoname_sets = self.get_all_video_set()

        export_paramter_list = []
        skip_exist_flag = self.skip_export_exists.get()
        for item0 in resource_dict[order_list[0]]:
            for item1 in resource_dict[order_list[1]]:
                for item2 in resource_dict[order_list[2]]:
                    for item3 in resource_dict[order_list[3]]:
                        for item4 in resource_dict[order_list[4]]:
                            paramter = {}
                            paramter[order_list[0]] = item0
                            paramter[order_list[1]] = item1
                            paramter[order_list[2]] = item2
                            paramter[order_list[3]] = item3
                            paramter[order_list[4]] = item4

                            # effect名称转路径
                            effect_name = paramter['effect']
                            effect_pathes = self.convert_pathes(paramter['image'],
                                                os.path.join(self.dy_data_utils.effects_dir, effect_name), suffix=".mp4")
                            if len(effect_pathes) != len(paramter['image']):
                                continue
                            paramter['effect'] = effect_pathes

                            # compose名称转路径
                            compose_name = os.path.basename(os.path.dirname(paramter['compose']))
                            compose_pathes = self.convert_pathes(paramter['image'], os.path.join(self.dy_data_utils.compose_dir, compose_name))
                            if len(compose_pathes) != len(paramter['image']):
                                continue
                            paramter['compose'] = compose_pathes

                            video_save_name = self.sluify(paramter) + ".mp4"

                            if skip_exist_flag == 1 and video_save_name in videoname_sets:
                                continue

                            paramter['video_save_name'] = video_save_name
                            export_paramter_list.append(paramter)

        return export_paramter_list

    def sluify(self, paramter):
        music_name = ""
        if os.path.exists(paramter['music']):
            music_name = os.path.basename(paramter['music'])
            music_name = music_name[0:15]

        video_name = ""
        if os.path.exists(paramter['video']):
            video_name = os.path.basename(paramter['video'])
            video_name = video_name[0:15]

        image_name = ""
        for img_path in paramter['image']:
            image_name += os.path.basename(img_path).split("_")[2][:10]
        image_name = image_name[:40]

        effect_name = ""
        if os.path.exists(paramter['effect'][0]):
            effect_name = os.path.basename(os.path.dirname(paramter['effect'][0]))
            effect_name = effect_name[0:15]

        compose_name = ""
        if os.path.exists(paramter['compose'][0]):
            compose_name = os.path.basename(os.path.dirname(paramter['compose'][0]))
            compose_name = compose_name[0:15]

        return f"{music_name}_{video_name}_{image_name}_{effect_name}_{compose_name}"

    def get_all_video_set(self):
        video_set = set()
        for dir_path, _, filenames in os.walk(self.dy_data_utils.device_dir):
            for filename in filenames:
                if filename.endswith(".mp4"):
                    video_set.add(filename)
        return video_set

    def paramter_convert(self, paramter):
        new_paramter = {}
        new_paramter['music_path'] = paramter['music']
        new_paramter['stuck_points_path'] = paramter['music'][:-4] + ".json"
        new_paramter['video_path'] = paramter['video']
        new_paramter['image_paths'] = list(paramter['image'])
        new_paramter['effect_paths'] = paramter['effect']
        new_paramter['compose_paths'] = paramter['compose']
        new_paramter['save_path'] = os.path.join(self.dy_data_utils.device_dir, paramter['device_name'], '待发送', paramter['video_save_name'])
        # new_paramter['title_content'] = '你要的姐妹头像来了...'
        # new_paramter['text_font_path'] = os.path.join(self.dy_data_utils.fonts_dir, '1.ttf')
        # new_paramter['text_color'] = (125, 125, 125)

        return new_paramter

    def export(self):
        # devices_index = self.device_list_box.curselection()
        # devices = []
        # if len(devices_index) == 0:
        #     msg.showinfo("警告", "请先选择要导出的设备！")
        #     return
        # else:
        #     for index in devices_index:
        #         devices.append(self.device_list_box.get(index))

        export_video_num = self.export_video_num.get()

        export_paramter_list = self.get_export_resource_list()

        if len(export_paramter_list) == 0:
            msg.showerror("警告", f"导出数量为0！")
            return


        answer = msg.askquestion(title='提示',
                                 message=f"预计可以生成{min(len(export_paramter_list), export_video_num)}个视频，是否继续！")
        if answer != msg.YES:
            return

        export_device_list = self.get_select_device_list()
        if len(export_device_list) <= 0:
            return

        export_list_iter = InfiniteIterator(export_device_list)

        upload_config = UploadConfig()

        for paramter in export_paramter_list:
            paramter["device_name"] = export_list_iter.next()
            fun_paramter = self.paramter_convert(paramter)
            generate_single_video(**fun_paramter)

            # 拷贝图片到未上传
            upload_folder_name = upload_config.get_upload(paramter["device_name"])
            if upload_folder_name is None:
                msg.showerror("警告", f"设备:{paramter['device_name']} 未定义取图账号！")
                return

            offline_folder_path = os.path.join(self.dy_data_utils.upload_dir, upload_folder_name, "未上传")
            if not os.path.exists(offline_folder_path):
                os.makedirs(offline_folder_path)

            online_folder_path = os.path.join(self.dy_data_utils.upload_dir, upload_folder_name, "已上传")
            if not os.path.exists(online_folder_path):
                os.makedirs(online_folder_path)

            upload_exists_filenames = list(os.listdir(online_folder_path)) + \
                                      list(os.listdir(offline_folder_path))

            for image_path in paramter['image']:
                if os.path.basename(image_path) not in upload_exists_filenames:
                    shutil.copy(image_path, os.path.join(offline_folder_path, os.path.basename(image_path)))

        msg.showinfo("提示", "视频生成成功！")
        self.destroy()


if __name__ == "__main__":
    analyse = ComposeVideo()
    analyse.mainloop()