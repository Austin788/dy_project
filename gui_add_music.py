import os

import tkinter as tk
from tkinter import messagebox as msg
from tkinter import filedialog
from tkinter import *
from moviepy.editor import VideoFileClip, AudioFileClip, afx
from data_util import *
import json

class AddMusic(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)

        self.title("添加音乐文件")
        self.geometry("500x700")
        self.resizable(False, False)

        self.standard_font = (None, 16)

        self.main_frame = tk.Frame(self, width=700, height=300)
        self.main_frame.grid(row=5, column=8)

        self.default_source = r'/Users/meitu/Downloads'
        self.source_path = tk.StringVar(value=self.default_source)
        tk.Label(self.main_frame, text="mp4文件路径:").grid(row=0, column=0)
        tk.Entry(self.main_frame, textvariable=self.source_path, width=30).grid(row=0, column=1)
        tk.Button(self.main_frame, text="选择", command=self.select_source_path, width=10).grid(row=0, column=2)

        self.frame_rate = tk.IntVar(value=30)
        tk.Label(self.main_frame, text="帧率:").grid(row=1, column=0)
        tk.Entry(self.main_frame, textvariable=self.frame_rate, width=30).grid(row=1, column=1)

        self.music_name = tk.StringVar()
        tk.Label(self.main_frame, text="音乐名称:").grid(row=2, column=0)
        tk.Entry(self.main_frame, textvariable=self.music_name, width=30).grid(row=2, column=1)
        tk.Button(self.main_frame, text="保存", command=self.save, width=10).grid(row=2, column=2)

        self.stuck_points_tk_list = []
        self.stuck_points_tk_valiable = []
        self.stuck_points_label_begein_row = 3

        for i in range(7):
            self.add_stuck_points_label()

        self.main_frame.pack(fill=tk.BOTH, expand=1)
        self.dy_data_utils = DYDataUtils()

    def add_stuck_points_label(self):

        tk.Label(self.main_frame, text=f"卡点{self.stuck_points_label_begein_row-2}:").grid(row=self.stuck_points_label_begein_row, column=0)
        textvariable = tk.StringVar()
        self.stuck_points_tk_valiable.append(textvariable)
        self.stuck_points_tk_list.append(tk.Entry(self.main_frame, textvariable=textvariable, width=30).grid(row=self.stuck_points_label_begein_row, column=1))
        if self.stuck_points_label_begein_row - 2 == 1:
            tk.Button(self.main_frame, text="添加卡点", command=self.add_stuck_points_label, width=10).grid(row=self.stuck_points_label_begein_row, column=2)
        self.stuck_points_label_begein_row += 1

    def select_save_path(self):
        save_path = tk.filedialog.askdirectory(initialdir=self.default_save)
        if save_path is None:
            return
        self.save_path.set(save_path)

    def select_source_path(self):
        source_path = tk.filedialog.askopenfile(filetypes=[("Configuration file", ["*.mp4", "*.mp3"])], initialdir=self.default_source)
        print(source_path)
        if source_path is None:
            return
        self.source_path.set(source_path.name)
        self.music_name.set((os.path.basename(source_path.name))[:-4] + ".mp3")

    def save(self):
        stuck_points = []
        for i in range(len(self.stuck_points_tk_valiable)):
            valiable = self.stuck_points_tk_valiable[i].get()
            if valiable is not None and len(valiable) > 0:
                stuck_points.append(valiable)

        save_music_path = os.path.join(self.dy_data_utils.music_dir, self.music_name.get())

        if not os.path.samefile(self.dy_data_utils.music_dir, os.path.dirname(self.source_path.get())):
            video = VideoFileClip(self.source_path.get())
            audio = video.audio
            audio.write_audiofile(save_music_path)

        if len(stuck_points) > 0:
            for i in range(len(stuck_points)):
                parts = stuck_points[i].split('.')
                try:
                    if len(parts) > 1 and len(parts[1]) > 0:
                        stuck_points[i] = int(parts[0]) + (int(parts[1]) / self.frame_rate.get())
                    else:
                        stuck_points[i] = int(parts[0])

                    if i > 0 and stuck_points[i] < stuck_points[i-1]:
                        msg.showinfo("状态", f"后面卡点值小于前面卡点值，请核对")
                        return
                except:
                    msg.showinfo("状态", f"卡点格式为 秒数.帧数")
                    return

            save_json_path = save_music_path[:-4] + ".json"
            if os.path.exists(save_json_path):
                with open(save_json_path) as f:
                    data = json.load(f)
            else:
                data = {}
            data['music_name'] = self.music_name.get()
            with open(save_json_path, "w") as f:
                if "stuck_points" not in data:
                    data["stuck_points"] = {}
                data["stuck_points"][str(len(stuck_points))] = stuck_points
                json.dump(data, f, indent=4, ensure_ascii=False)

        msg.showinfo("状态", f"保存成功")
        self.destroy()


if __name__ == "__main__":
    timer = AddMusic()
    timer.mainloop()
