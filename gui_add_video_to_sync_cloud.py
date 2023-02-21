import os

import tkinter as tk
from tkinter import messagebox as msg
from tkinter import filedialog
from tkinter import *
from moviepy.editor import VideoFileClip, AudioFileClip, afx
from data_util import *
import json
import shutil
import time

class AddVideo(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)

        self.title("添加视频到同步云")
        self.geometry("1000x700")
        self.resizable(False, False)

        self.standard_font = (None, 16)

        self.main_frame = tk.Frame(self, width=1000, height=600)
        self.main_frame.grid(row=5, column=4)

        self.default_source = r'/Users/meitu/Documents/midlife_crisis/project/dy_project/data/素材库/download_video'

        self.video_str = tk.StringVar(value=self.default_source)
        tk.Label(self.main_frame, text="视频路径:").grid(row=0, column=0)
        tk.Entry(self.main_frame, textvariable=self.video_str, width=80).grid(row=0, column=1, columnspan=2, sticky=NSEW)
        tk.Button(self.main_frame, text="选择", command=self.select_source_path, width=10).grid(row=0, column=3)

        # self.dst_path = tk.StringVar(value=self.default_save)
        # tk.Label(self.main_frame, text="保存路径:").grid(row=1, column=0)
        # tk.Entry(self.main_frame, textvariable=self.source_path, width=30).grid(row=1, column=1, rowspan=2)
        # tk.Button(self.main_frame, text="选择", command=self.select_source_path, width=10).grid(row=1, column=3)

        tk.Label(self.main_frame, text="导出路径:").grid(row=1, column=0, rowspan=2)
        tk.Label(self.main_frame, text="快手设备").grid(row=1, column=1)
        tk.Label(self.main_frame, text="抖音设备").grid(row=1, column=2)

        self.ks_dir = "/Users/meitu/同步空间/视频/KS"
        ks_device_ids = [dirname for dirname in os.listdir(self.ks_dir) if os.path.isdir(os.path.join(self.ks_dir, dirname))]
        self.ks_devices_items = tk.StringVar(value=ks_device_ids)
        self.ks_device_list_box = tk.Listbox(self.main_frame, cursor='arrow', selectborderwidth=2, listvariable=self.ks_devices_items,
                                          selectmode=MULTIPLE)
        self.ks_device_list_box.grid(row=2, column=1, sticky=NSEW, padx=10)
        self.ks_device_list_box.configure(exportselection=False)

        self.dy_dir = "/Users/meitu/同步空间/视频/DY"
        dy_device_ids = [dirname for dirname in os.listdir(self.dy_dir) if os.path.isdir(os.path.join(self.dy_dir, dirname))]
        self.dy_devices_items = tk.StringVar(value=dy_device_ids)
        self.dy_device_list_box = tk.Listbox(self.main_frame, cursor='arrow', selectborderwidth=2, listvariable=self.dy_devices_items,
                                          selectmode=MULTIPLE)
        self.dy_device_list_box.grid(row=2, column=2, sticky=NSEW, padx=10)
        self.dy_device_list_box.configure(exportselection=False)


        self.koulin = tk.StringVar()
        tk.Label(self.main_frame, text="口令:").grid(row=3, column=0)
        tk.Entry(self.main_frame, textvariable=self.koulin).grid(row=3, column=1, columnspan=2, sticky=NSEW)
        tk.Button(self.main_frame, text="保存", command=self.save, width=10).grid(row=3, column=3)

        self.main_frame.pack(fill=tk.BOTH, expand=1)

    #
    # def select_save_path(self):
    #     save_path = tk.filedialog.askdirectory(initialdir=self.default_save)
    #     if save_path is None:
    #         return
    #     self.save_path.set(save_path)

    def select_source_path(self):
        self.video_pathes = tk.filedialog.askopenfiles(filetypes=[("Configuration file", "*.mp4")],
                                                  initialdir=self.default_source)
        self.video_str.set(self.video_pathes)

        print(self.video_pathes)


    def get_box_list(self, list_box, parent_dir):
        select_indexes = list_box.curselection()
        box_list = []
        for index in select_indexes:
            box_list.append(list_box.get(index))

        for i in range(len(box_list)):
            box_list[i] = os.path.join(parent_dir, box_list[i])

        return box_list

    def save(self):

        if len(self.video_pathes) == 0:
            msg.showinfo("状态", f"请先选择路径！")
            return



        save_paths = self.get_box_list(self.dy_device_list_box, self.dy_dir) + \
                     self.get_box_list(self.ks_device_list_box, self.ks_dir)

        if len(save_paths) == 0:
            msg.showinfo("状态", f"请先选择导出设备！")
            return

        koulin = self.koulin.get()
        try:
            koulin = f"口令[{koulin}]"
        except:
            koulin = ""

        save_dir = koulin + "_" + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        for i, filepath in enumerate(self.video_pathes):
            filepath = filepath.name
            if str(filepath).endswith('.mp4'):
                base_filename = os.path.basename(filepath)
                base_filename = base_filename[base_filename.find("-")+1:]
                save_path = os.path.join(save_paths[i % len(save_paths)], save_dir, base_filename)
                if not os.path.exists(os.path.dirname(save_path)):
                    os.makedirs(os.path.dirname(save_path))
                shutil.move(filepath, save_path)
                print(f"move {filepath} to {save_path}")
                # shutil.move()

        msg.showinfo("状态", f"导入成功")

if __name__ == "__main__":
    timer = AddVideo()
    timer.mainloop()
