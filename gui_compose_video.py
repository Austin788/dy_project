# -*- encoding=utf-8 -*-
from tkinter import filedialog
from tkinter import *
from gui_util import *
from data_util import *
from tkinter import messagebox as msg
import itertools

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

        self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        self.default_source = "/Users/meitu/Downloads/8.13/1-1/"
        self.dy_data_utils = DYDataUtils(self.data_dir)
        types = self.dy_data_utils.get_image_type_list()

        self.group_num = tk.IntVar()
        self.type_value = tk.StringVar(self)
        self.export_type_value = tk.StringVar(self)

        button_width = 15
        tk.Label(self, text="操作:").grid(row=0, column=0, padx=10, pady=10)
        self.exchange_checkbtn_num = tk.IntVar()
        self.exchange_checkbtn = tk.Checkbutton(self, text="是否交换图片顺序", variable=self.exchange_checkbtn_num, onvalue=1, offvalue=0, width=button_width)
        self.exchange_checkbtn.grid(row=0, column=1)

        self.img_num_per_video = tk.IntVar(value=3)
        tk.Label(self, text="视频图片数:").grid(row=0, column=2, padx=10, pady=10)
        tk.Entry(self, textvariable=self.img_num_per_video, width=5).grid(row=0, column=3)

        self.export_video_num = tk.IntVar(value=9999)
        tk.Label(self, text="导出视频数:").grid(row=0, column=4, padx=10, pady=10)
        tk.Entry(self, textvariable=self.export_video_num, width=5).grid(row=0, column=5)

        self.export_btn = tk.Button(self, text="导出", command=self.export, width=button_width)
        self.export_btn.grid(row=0, column=8, pady=10)

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
        self.complete_all_btn.grid(row=3, column=7)
        self.complete_all_btn = tk.Button(self, text="选择导出设备", command=None, width=button_width)
        self.complete_all_btn.grid(row=3, column=8)

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

        # 合成列表
        self.compose_list = ListImageManager(self)
        self.compose_list.grid(row=4, column=7, sticky=NSEW, padx=10)
        for key, value in self.dy_data_utils.get_compose_ids_pathes().items():
            self.compose_list.add_by_path(value)

        # 设备列表
        self.devices_items = tk.StringVar(value=self.dy_data_utils.device_ids)
        self.device_list_box = tk.Listbox(self, cursor='arrow', selectborderwidth=2, listvariable=self.devices_items,
                                           selectmode=MULTIPLE)
        self.device_list_box.grid(row=4, column=8, sticky=NSEW, padx=10)
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
        music_list = self.music_list_box.get(0, END)
        if music_list is None:
            music_list = ['None']
        return list(music_list)

    def get_select_video_list(self):
        video_list = self.video_list.image_list
        if len(video_list) == 0:
            video_list= ['None']
        return video_list

    def get_select_image_list(self):
        img_num_per_video = self.img_num_per_video.get()
        if img_num_per_video is None:
            msg.showerror("警告", "请选择需要添加的类别")
            return
        image_list = self.image_list.image_list

        if len(image_list) > 0:
            image_list.sort()

            if self.exchange_checkbtn_num.get() == 1:
                image_list = list(itertools.permutations(image_list, img_num_per_video))  # 无序
            else:
                image_list = list(itertools.combinations(image_list, img_num_per_video))  # 有序
        else:
            image_list = ['None']

        return image_list

    def get_select_effect_list(self):
        selects = self.effect_list_box.curselection()
        effect_names = []
        for index in selects:
            effect_names.append(self.effect_list_box.get(index))
        if len(effect_names) == 0:
            effect_names = ['None']
        return effect_names


    def get_select_compose_list(self):
        compose_list = self.compose_list.image_list
        if len(compose_list)  == 0:
            compose_list = ['None']
        return compose_list

    def export(self):
        # devices_index = self.device_list_box.curselection()
        # devices = []
        # if len(devices_index) == 0:
        #     msg.showinfo("警告", "请先选择要导出的设备！")
        #     return
        # else:
        #     for index in devices_index:
        #         devices.append(self.device_list_box.get(index))

        music_list = self.get_select_music_list()
        video_list = self.get_select_video_list()
        image_list = self.get_select_image_list()
        effect_list = self.get_select_effect_list()
        compose_list = self.get_select_compose_list()

        resource_dict = {'music':music_list, 'video':video_list, 'image':image_list, 'effect':effect_list, 'compose':compose_list}

        order_list = ["video", 'image', 'effect', 'compose', 'music']
        order_list.reverse()

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

                            print(paramter)

        # resouce_index = [0] * len(order_list)
        # for type in order_list:
        #
        # print(music_list)
        # print(video_list)
        # print(image_list)
        # print(effect_list)
        # print(compose_list)


if __name__ == "__main__":
    analyse = ComposeVideo()
    analyse.mainloop()