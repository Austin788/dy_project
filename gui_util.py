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



class ListImageManager(tk.Frame):
    def __init__(self, parent, image_dict={}, frame_width=200+50, frame_height=700, image_size=100):
        tk.Frame.__init__(self, parent)

        self.column_num = int(frame_width / image_size)
        self.row_num = int(frame_height / image_size)
        print(self.row_num, self.column_num)
        self.image_size = image_size


        self.main_frame = tk.Frame(self, width=frame_width, height=frame_height, bd=2, highlightcolor='black', highlightbackground='black', highlightthickness=1)
        self.main_frame.grid(row=self.row_num, column=self.column_num)
        self.main_frame.grid_propagate(0)

        self.list_image_cache = TkImageCacheCollection(cache_size=image_size)

        self.image_count = 0
        for name, path in image_dict.items():
            row_index = int(self.image_count / self.column_num)
            column_index = self.image_count - row_index * self.row_num
            print(row_index, column_index)
            tk.Button(self.main_frame, text=name, overrelief='sunken', image=self.list_image_cache.add_by_path(path, name),
                      width=image_size, cursor="arrow", command=lambda :self.delete(name)).grid(row=row_index, column=column_index)
            self.image_count += 1

    def add(self, path, tk_image):
        insert_flag = False
        for btn in self.main_frame.winfo_children():
            if btn['text'] == "":
                print("add to exists")
                btn['image'] = tk_image
                btn['command'] = lambda :self.delete(path)
                insert_flag = True

        if not insert_flag:
            row_index = int(self.image_count / self.column_num)
            column_index = self.image_count - row_index * self.column_num
            print(row_index, column_index)
            tk.Button(self.main_frame, text=path, overrelief='sunken',
                      image=tk_image,
                      width=self.image_size, cursor="arrow", command=lambda: self.delete(path)).grid(row=row_index,
                                                                                                column=column_index)
            self.image_count += 1
        self.main_frame.configure(height=700)

    def add_by_cv_frame(self, frame, path):
        if self.is_exists(path):
            return
        tk_image = self.list_image_cache.add_by_cv_frame(frame, path)
        self.add(path, tk_image)

    def add_by_path(self, path):
        if self.is_exists(path):
            return
        tk_image = self.list_image_cache.add_by_path(path)
        self.add(path, tk_image)

    def delete(self, path):
        for btn in self.main_frame.winfo_children():
            if btn['text'] == path:
                btn['text'] = ''
                btn['command'] = None

    def is_exists(self, path):
        for btn in self.main_frame.winfo_children():
            if btn['text'] == path:
                return True
        return False

    @property
    def image_list(self):
        pathes = []
        for btn in self.main_frame.winfo_children():
            if btn['text'] != "":
                pathes.append(btn['text'])

        return pathes

if __name__ == "__main__":
    from gui_compose_video import ListImageSelector
    from data_util import DYDataUtils

    dy_data_utils = DYDataUtils("")

    items = ['apple', 'orange', 'pear', 'grape']
    ListBoxClass = create_list_box_selector(tk.Toplevel)
    list_box = ListBoxClass(items, "list test")
    list_box.mainloop()