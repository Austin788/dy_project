import os
import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk


def open_image(path, size=100):
    image = Image.open(path)
    image = image.resize((size, size))
    tk_image = ImageTk.PhotoImage(image)
    return tk_image


def cv_frame_to_tk_image(frame):
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    tk_image = ImageTk.PhotoImage(image)
    return tk_image


class TkImageCacheCollection():
    def __init__(self, cache_size=100):
        self.name_tk_frame_dict = {}
        self.cache_size = cache_size

    def get_empty_image(self):
        empty_image_name = "empty_image"
        if empty_image_name not in self.name_tk_frame_dict:
            tk_image = cv_frame_to_tk_image(np.ones((self.cache_size, self.cache_size, 3), dtype=np.uint8) * 255)
            self.name_tk_frame_dict[empty_image_name] = tk_image
        else:
            tk_image = self.name_tk_frame_dict[empty_image_name]

        return tk_image

    def add_by_path(self, path, cache_name=None):
        if cache_name is None:
            cache_name = path
        if path not in self.name_tk_frame_dict:
            tk_image = open_image(path, self.cache_size)
            self.name_tk_frame_dict[cache_name] = tk_image
        else:
            tk_image = self.name_tk_frame_dict[cache_name]

        return tk_image

    def remove(self, cache_name):
        if cache_name in self.name_tk_frame_dict:
            del self.name_tk_frame_dict[cache_name]

    def add_by_cv_frame(self, frame, cache_name):
        resize_frame = cv2.resize(frame, (self.cache_size, self.cache_size))
        if cache_name not in self.name_tk_frame_dict:
            tk_image = cv_frame_to_tk_image(resize_frame)
            self.name_tk_frame_dict[cache_name] = tk_image
        else:
            tk_image = self.name_tk_frame_dict[cache_name]

        return tk_image



pass

def create_list_box_selector(cls):
    class ListBoxSelector(cls):
        def __init__(self, list_names, title):
            super().__init__()
            self.list_names = list_names
            self.title(title)

            screenwidth = self.winfo_screenwidth()  # 屏幕宽度
            screenheight = self.winfo_screenheight()  # 屏幕高度
            width = 250
            height = 300
            x = int((screenwidth - width) / 2)
            y = int((screenheight - height) / 2)
            self.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置
            self.resizable(False, False)

            self.standard_font = (None, 16)

            self.main_frame = tk.Frame(self, width=width, height=height)
            self.main_frame.grid(row=2, column=2)
            strvar_items = tk.StringVar(value=self.list_names)

            self.list_box = tk.Listbox(self.main_frame, cursor='arrow', listvariable=strvar_items,
                                       selectborderwidth=2)
            self.ok_btn = tk.Button(self.main_frame, text="确定", command=self.ok, width=5)
            self.cancel_btn = tk.Button(self.main_frame, text="取消", command=self.cancel, width=5)

            self.list_box.grid(row=0, column=0, columnspan=2, pady=15, padx=15)
            self.ok_btn.grid(row=1, column=0, pady=15, padx=15)
            self.cancel_btn.grid(row=1, column=1, pady=15, padx=15)


        def ok(self):
            self.list_box_select_index = self.list_box.curselection()
            self.destroy()  # 销毁窗口

        def cancel(self):
            self.list_box_select_index = None  # 空！
            self.destroy()


    return ListBoxSelector


if __name__ == "__main__":
    items = ['apple', 'orange', 'pear', 'grape']
    ListBoxClass = create_list_box_selector(tk.Toplevel)
    list_box = ListBoxClass(items, "list test")
    list_box.mainloop()