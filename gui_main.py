import tkinter as tk
from gui_add_data import AddData
from gui_add_music import AddMusic
from gui_compose_video import ComposeVideo

from tkinter import *
from tkinter.ttk import *
"""

"""


class MainGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("抖音视频生成")
        frame_width = 700
        frame_height = 600
        x = 50
        y = 50
        self.geometry('{}x{}+{}+{}'.format(frame_width, frame_height, x, y))  # 大小以及位置
        self.resizable(False, False)

        self.standard_font = (None, 16)

        self.main_frame = tk.Frame(self, width=frame_width, height=frame_height)
        # self.main_frame.grid(row=9, column=3)

        bt_width = 40
        bt_height = 2
        self.select_order_btn = tk.Button(self.main_frame, text="添加图片、效果、合成数据", width=bt_width, height=bt_height)
        self.select_order_btn.pack(expand=True)
        self.select_order_btn.bind("<Button>", lambda e: AddData(self))

        self.rename_comment_btn = tk.Button(self.main_frame, text="合成视频(视频+图片+合成模式)", width=bt_width, height=bt_height)
        self.rename_comment_btn.pack(expand=True)
        self.rename_comment_btn.bind("<Button>", lambda e: ComposeVideo(self))

        self.add_music_btn = tk.Button(self.main_frame, text="添加音乐踩点", width=bt_width, height=bt_height)
        self.add_music_btn.pack(expand=True)
        self.add_music_btn.bind("<Button>", lambda e: AddMusic(self))


        self.main_frame.pack(fill=tk.BOTH, expand=1)

    def function(self, Class):
        self.class_obj = Class()
        self.class_obj.mainloop()

if __name__ == "__main__":
    main_gui = MainGUI()
    main_gui.mainloop()