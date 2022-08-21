# -*- encoding=utf-8 -*-
from tkinter import filedialog
from tkinter import *
from gui_util import *
from data_util import *
from tkinter import messagebox as msg




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

        self.group_num = tk.IntVar
        self.type_value = tk.StringVar(self)
        self.export_type_value = tk.StringVar(self)

        button_width = 15
        self.add_image_btn = tk.Button(self, text="选择音乐", command=self.select_music, width=int(button_width/2))
        self.add_image_btn.grid(row=3, column=0, padx=10, pady=10)
        self.add_image_btn = tk.Button(self, text="删除音乐", command=self.delete_music, width=int(button_width/2))
        self.add_image_btn.grid(row=3, column=1)
        self.add_effect_btn = tk.Button(self, text="选择视频", command=self.select_video, width=button_width)
        self.add_effect_btn.grid(row=3, column=2)
        self.add_compose_btn = tk.Button(self, text="选择图片", command=self.select_image, width=button_width)
        self.add_compose_btn.grid(row=3, column=3)
        self.complete_current_btn = tk.Button(self, text="选择特效", command=self.select_effects, width=10)
        self.complete_current_btn.grid(row=3, column=4)
        self.complete_all_btn = tk.Button(self, text="选择合成", command=self.select_compose, width=button_width)
        self.complete_all_btn.grid(row=3, column=5)
        self.complete_all_btn = tk.Button(self, text="选择导出设备", command=None, width=button_width)
        self.complete_all_btn.grid(row=3, column=6)

        # 音乐列表
        self.music_list_box = tk.Listbox(self, cursor='arrow', selectborderwidth=2, selectmode=MULTIPLE)
        self.music_list_box.grid(row=4, column=0, columnspan=2, sticky=NSEW, padx=10)
        self.music_list_box.configure(exportselection=False)

        # 热点视频列表
        self.video_list = ListImageManager(self)
        self.video_list.grid(row=4, column=2, sticky=NSEW, padx=10)

        # 图片列表
        self.image_list = ListImageManager(self)
        self.image_list.grid(row=4, column=3, sticky=NSEW, padx=10)

        # 效果列表
        self.effects_items = tk.StringVar(value=self.dy_data_utils.effects_ids)
        self.effect_list_box = tk.Listbox(self, cursor='arrow', selectborderwidth=2, listvariable=self.effects_items, selectmode=MULTIPLE, width=10)
        self.effect_list_box.grid(row=4, column=4, sticky=NSEW, padx=10)
        self.effect_list_box.configure(exportselection=False)

        # 合成列表
        self.compose_list = ListImageManager(self, self.dy_data_utils.get_compose_ids_pathes())
        self.compose_list.grid(row=4, column=5, sticky=NSEW, padx=10)

        # 设备列表
        self.devices_items = tk.StringVar(value=self.dy_data_utils.device_ids)
        self.device_list_box = tk.Listbox(self, cursor='arrow', selectborderwidth=2, listvariable=self.devices_items,
                                           selectmode=MULTIPLE)
        self.device_list_box.grid(row=4, column=6, sticky=NSEW, padx=10)
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

if __name__ == "__main__":
    analyse = ComposeVideo()
    analyse.mainloop()