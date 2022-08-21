# -*- encoding=utf-8 -*-
import os
import cv2
import tkinter as tk
import datetime as dt
import pandas as pd
import numpy as np
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import messagebox as msg
from datetime import datetime
from styleframe import StyleFrame
from tkinter import *
from gui_util import *
from data_util import *
import shutil


class ListImageSelector(tk.Toplevel):
    def __init__(self, first_image_path, other_image_dict, first_image_name="原图", title="请选择使用的模板", image_size=200):
        super().__init__()
        self.title(title)

        screenwidth = self.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.winfo_screenheight()  # 屏幕高度
        width = screenwidth - 200
        height = screenheight - 200
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置
        self.resizable(False, False)

        row_num = int(width / image_size)
        column_num = int(height / image_size)


        self.main_frame = tk.Frame(self, width=width, height=height)
        self.main_frame.grid(row=row_num, column=column_num)

        self.list_image_cache = TkImageCacheCollection(cache_size=image_size)
        compare_image = self.list_image_cache.add_by_path(first_image_path, first_image_name)
        self.select_path = None

        tk.Button(self.main_frame, text=first_image_name[:10], image=compare_image, width=image_size, compound=BOTTOM).grid(row=0, column=0)
        i = 1
        for name, path in other_image_dict.items():
            row_index = int(i / column_num)
            column_index = i - row_index * row_num
            tk.Button(self.main_frame, text=name[:10], command=lambda :self.btn_action(name), overrelief='sunken', image=self.list_image_cache.add_by_path(path, name), width=image_size, compound=BOTTOM, cursor="arrow").grid(row=row_index, column=column_index)
            i += 1

    def btn_action(self, name):
        self.select_name = name
        self.destroy()  # 销毁窗口


class AddData(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        # win = tk.Tk()  # 窗口
        self.title('数据分析')  # 标题
        screenwidth = self.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.winfo_screenheight()  # 屏幕高度
        print(screenwidth, screenheight)
        width = max(int(screenwidth / 2), 800)
        height = screenheight
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)

        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置
        # self.main_frame = tk.Frame(self, width=width, height=height)
        # self.grid(row=2, column=7)

        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)
        # self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(6, weight=1)
        #

        self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        self.default_source = "/Users/meitu/Downloads/8.13/1-1/"
        self.dy_data_utils = DYDataUtils(self.data_dir)
        types = self.dy_data_utils.get_image_type_list()


        self.group_num = tk.IntVar
        self.type_value = tk.StringVar(self)
        self.export_type_value = tk.StringVar(self)



        button_width = 15
        tk.Label(self, text="数据类型:").grid(row=0, column=0, ipadx=10, ipady=10)
        # # Dictionary to create multiple buttons
        values = {"图片+效果+合成": "图片效果合成",
                  "图片+合成": "图片合成",
                  "图片+效果": "图片效果",
                  "图片": "图片"
                  }
        count = 1
        # Loop is used to create multiple Radiobuttons
        # rather than creating each button separately
        for (text, value) in values.items():
            tk.Radiobutton(self, text=text, variable=self.type_value, value=value, indicator=0,
                           width=button_width, command=self.type_action).grid(row=0,
                                                    column=count)
            count += 1


        tk.Label(self, text="组号(可默认):").grid(row=0, column=5)
        tk.Entry(self, textvariable=self.group_num).grid(row=0, column=6)

        tk.Label(self, text="头像保存类型:").grid(row=1, column=0, ipadx=10, ipady=10)
        print(types)
        count = 1
        for type in types:
            tk.Radiobutton(self, text=type, value=type, variable=self.export_type_value, indicator=0,
                           width=button_width).grid(row=1,
                                                    column=count)
            count += 1

        tk.Label(self, text="操作:").grid(row=2, column=0)
        self.add_image_btn = tk.Button(self, text="添加图片", command=self.add_image, width=button_width, state=DISABLED)
        self.add_image_btn.grid(row=2, column=1)
        self.add_effect_btn = tk.Button(self, text="添加效果", command=self.add_effect, width=button_width, state=DISABLED)
        self.add_effect_btn.grid(row=2, column=2)
        self.add_compose_btn = tk.Button(self, text="添加合成", command=self.add_compose, width=button_width, state=DISABLED)
        self.add_compose_btn.grid(row=2, column=3)
        self.complete_current_btn = tk.Button(self, text="完成该图片", command=self.complete_current, width=button_width, state=NORMAL)
        self.complete_current_btn.grid(row=2, column=4)
        self.complete_all_btn = tk.Button(self, text="完成", command=self.complete, width=button_width)
        self.complete_all_btn.grid(row=2, column=5)


        tk.Label(self, text="序号:").grid(row=3, column=0, ipadx=10, ipady=10)
        tk.Label(self, text="图片:").grid(row=3, column=1, columnspan=2)
        tk.Label(self, text="效果:").grid(row=3, column=3, columnspan=2)
        tk.Label(self, text="合成:").grid(row=3, column=5, columnspan=2)



        self.myframe = Frame(self)
        self.myframe.grid(row=4, columnspan=7, sticky=tk.NSEW)

        self.canvas = Canvas(self.myframe, height=self.myframe.winfo_height())
        self.frame = Frame(self.canvas)
        self.myscrollbar = Scrollbar(self.myframe, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.myscrollbar.set)

        self.myscrollbar.pack(side="right", fill="y")
        self.canvas.pack(fill=BOTH)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')
        self.frame.bind("<Configure>", self.event1)


        self.photo_list = []
        self.path_tk_frame_dict = {}
        self.tk_image_collection = TkImageCacheCollection()
        self.image_num = 1
        self.current_image_path = None

    def event1(self, event):
        print(self.myframe.winfo_height())
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=self.myframe.winfo_width(), height=self.myframe.winfo_height())

    # def select_save_path(self):
    #     save_path = tk.filedialog.askdirectory(initialdir=self.default_save)
    #     if save_path is None:
    #         return
    #     self.save_path.set(save_path)

    def type_action(self):
        type_value = self.type_value.get()
        print(type_value)
        if str(type_value).find("图片") != -1:
            self.add_image_btn['state'] = NORMAL
        else:
            self.add_image_btn['state'] = DISABLED

        if str(type_value).find("效果") != -1:
            self.add_effect_btn['state'] = NORMAL
        else:
            self.add_effect_btn['state'] = DISABLED

        if str(type_value).find("合成") != -1:
            self.add_compose_btn['state'] = NORMAL
        else:
            self.add_compose_btn['state'] = DISABLED

    def new_row_frame(self, num=None, image=None, image_path='', effect_image=None, effect_path='',
                      compose_image=None, compose_path=''):
        row_frame = tk.Frame(self.canvas)

        image_btn_name = ""
        effect_btn_name = ""
        compose_btn_name = ""

        if num is None:
            num = ''

        if image is not None:
            image_btn_name = "删除"
        else:
            pass
            image = self.tk_image_collection.get_empty_image()

        if effect_image is not None:
            effect_btn_name = "删除"
        else:
            pass
            effect_image = self.tk_image_collection.get_empty_image()

        if compose_image is not None:
            compose_btn_name = "删除"
        else:
            pass
            compose_image = self.tk_image_collection.get_empty_image()



        tk.Label(row_frame, text=f"{num}", width=5).grid(row=0, column=0, rowspan=2)
        _LABEL_WIDTH=150
        image_label = tk.Label(row_frame, text=f"{image_path}", image=image, width=_LABEL_WIDTH)
        image_label.grid(row=0, column=1, rowspan=2)

        image_button = tk.Button(row_frame, text=f"{image_btn_name}", width=9, command=lambda :self.delete(1, image_path))
        image_button.grid(row=0, column=2, rowspan=2)

        image_effects_label = tk.Label(row_frame, text=f"{effect_path}", image=effect_image, width=_LABEL_WIDTH)
        image_effects_label.grid(row=0, column=3, rowspan=2)

        image_effects_del_button = tk.Button(row_frame, text=f"{effect_btn_name}", width=9, command=lambda :self.delete(2, self.current_image_path, effect_path))
        image_effects_del_button.grid(row=0, column=4)

        image_compose_label = tk.Label(row_frame, text=f"{compose_path}", image=compose_image, width=_LABEL_WIDTH)
        image_compose_label.grid(row=0, column=5, rowspan=2)

        image_compose_del_button = tk.Button(row_frame, text=f"{compose_btn_name}", width=9, command=lambda :self.delete(3, self.current_image_path, compose_path))
        image_compose_del_button.grid(row=0, column=6)

        image_effects_button = tk.Button(row_frame, text=f"", width=9)
        image_effects_button.grid(row=1, column=4)

        image_compose_button = tk.Button(row_frame, text=f"", width=9)
        image_compose_button.grid(row=1, column=6)
        # if compose_path == "":
        #     image_effects_label.grid_forget()

        row_frame.pack()
        return row_frame

    def add_image(self):
        # type = self.type_value.get()
        # if len(type) == 0:
        #     msg.showerror("警告", "请选择需要添加的类别")
        #     return

        image_path = tk.filedialog.askopenfile(filetypes=[("Configuration file", "*.jpg")],
                                                    initialdir=self.default_source).name
        print(image_path)
        if image_path is None:
            return

        self.current_image_path = image_path

        image = self.tk_image_collection.add_by_path(image_path)

        if image_path not in self.path_tk_frame_dict:
            self.path_tk_frame_dict[image_path] = []

        row_frame = self.new_row_frame(self.image_num, image=image, image_path=image_path)
        self.path_tk_frame_dict[image_path].append(row_frame)

        self.add_image_btn["state"] = DISABLED


    def add_effect(self):
        if self.current_image_path is None:
            msg.showinfo("警告", "请先选择图片")
            return

        effect_path = tk.filedialog.askopenfile(filetypes=[("Configuration file", "*.mp4")],
                                               initialdir=self.default_source)
        if effect_path is not None:
            effect_path = effect_path.name
        else:
            return
        print(effect_path)
        if effect_path is None:
            msg.showinfo("警告", "请选择效果路径！")
            return

        cap = cv2.VideoCapture(effect_path)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret is not True:
                msg.showinfo("警告", "打开视频失败！")
                return

        if self.current_image_path not in self.path_tk_frame_dict:
            msg.showinfo("警告", "请先选择图片")
            return

        tk_image = self.tk_image_collection.add_by_cv_frame(frame, cache_name=effect_path)

        add_flag = False
        for frame in self.path_tk_frame_dict[self.current_image_path]:
            print(frame.winfo_children()[4]['text'])
            if frame.winfo_children()[4]['text'] == "":
                frame.winfo_children()[3]['image'] = tk_image
                frame.winfo_children()[3]['text'] = effect_path
                frame.winfo_children()[4]['text'] = '删除'
                frame.winfo_children()[4]['command'] = lambda: self.delete(2, self.current_image_path, effect_path)
                frame.winfo_children()[7]['text'] = '请选择效果ID'
                frame.winfo_children()[7]['command'] = lambda: self.select_effect_ID(frame.winfo_children()[7])
                add_flag = True
                break

        if not add_flag:
            row_frame = self.new_row_frame(effect_image=tk_image, effect_path=effect_path)
            self.path_tk_frame_dict[self.current_image_path].append(row_frame)

    def add_compose(self):
        if self.current_image_path is None:
            msg.showinfo("警告", "请先选择图片")
            return

        compose_path = tk.filedialog.askopenfile(filetypes=[("Configuration file", "*.jpg")],
                                               initialdir=self.default_source).name
        print(compose_path)
        if compose_path is None:
            msg.showinfo("警告", "请选择效果路径！")
            return


        tk_image = self.tk_image_collection.add_by_path(compose_path)

        add_flag = False
        for frame in self.path_tk_frame_dict[self.current_image_path]:
            print(frame.winfo_children()[6]['text'])
            if frame.winfo_children()[6]['text'] == "":
                frame.winfo_children()[5]['image'] = tk_image
                frame.winfo_children()[5]['text'] = compose_path
                frame.winfo_children()[6]['text'] = '删除'
                frame.winfo_children()[6]['command'] = lambda: self.delete(3, self.current_image_path, compose_path)
                frame.winfo_children()[8]['text'] = '请选择合成ID'
                frame.winfo_children()[8]['command'] = lambda: self.select_compose_ID(frame.winfo_children()[8], compose_path)
                add_flag = True
                break

        if not add_flag:
            row_frame = self.new_row_frame(compose_image=tk_image, compose_path=compose_path)
            self.path_tk_frame_dict[self.current_image_path].append(row_frame)

    def delete(self, type, image_path, other_path=None):
        print(type, image_path)
        if type == 1:
            for frame in self.path_tk_frame_dict[image_path]:
                print("in destory")
                frame.destroy()
                del self.path_tk_frame_dict[image_path]

        elif type == 2:
            for i, frame in enumerate(self.path_tk_frame_dict[image_path]):
                if frame.winfo_children()[3]['text'] == other_path:
                    if frame.winfo_children()[2]['text'] == "" and frame.winfo_children()[6]['text'] == "":
                        frame.destroy()
                        del self.path_tk_frame_dict[image_path][i]
                    else:
                        frame.winfo_children()[3]['image'] = self.tk_image_collection.get_empty_image()
                        frame.winfo_children()[3]['text'] = ""
                        frame.winfo_children()[4]['text'] = ""
                        frame.winfo_children()[4]['command'] = None
                        frame.winfo_children()[7]['text'] = ''
                        frame.winfo_children()[7]['command'] = None

        elif type == 3:
            for i, frame in enumerate(self.path_tk_frame_dict[image_path]):
                if frame.winfo_children()[5]['text'] == other_path:
                    if frame.winfo_children()[2]['text'] == "" and frame.winfo_children()[4]['text'] == "":
                        frame.destroy()
                        del self.path_tk_frame_dict[image_path][i]
                    else:
                        frame.winfo_children()[5]['image'] = self.tk_image_collection.get_empty_image()
                        frame.winfo_children()[5]['text'] = ""
                        frame.winfo_children()[6]['text'] = ""
                        frame.winfo_children()[6]['command'] = None
                        frame.winfo_children()[8]['text'] = ''
                        frame.winfo_children()[8]['command'] = None

        print("ff")
        self.canvas.pack_forget()
        self.canvas.pack()

    def select_effect_ID(self, ui):
        ListBoxClass = create_list_box_selector(tk.Toplevel)
        items = self.dy_data_utils.effects_ids
        print(items)
        list_box_dialog = ListBoxClass(items, "请选择效果名称")
        self.wait_window(list_box_dialog)  # 这一句很重要！！
        print(list_box_dialog.list_box_select_index)
        effect_name = items[list_box_dialog.list_box_select_index[0]]
        ui['text'] = effect_name

    def select_compose_ID(self, ui, select_path):
        path_dicts = self.dy_data_utils.get_compose_ids_pathes()
        print(path_dicts)
        list_image_dialog = ListImageSelector(select_path, path_dicts)

        self.wait_window(list_image_dialog)  # 这一句很重要！！
        if list_image_dialog.select_name is not None:
            ui['text'] = list_image_dialog.select_name

    def check_data(self):
        for path, frame_list in self.path_tk_frame_dict.items():
            for frame in frame_list:
                if frame.winfo_children()[4]['text'] != "" and str(frame.winfo_children()[7]['text']).startswith("请"):
                    msg.showerror("警告", "还有效果ID没有选择")
                    return

                if frame.winfo_children()[6]['text'] != "" and str(frame.winfo_children()[8]['text']).startswith("请"):
                    msg.showerror("警告", "还有合成ID没有选择")
                    return

    def complete_current(self):
        self.add_image_btn['state'] = NORMAL
        self.image_num = self.image_num + 1

    def complete(self):
        self.check_data()

        export_type = self.export_type_value.get()
        if len(export_type) == 0:
            msg.showerror("警告", "请选择需要添加的类别")
            return

        group_num = self.dy_data_utils.get_avilable_group_num(export_type)
        for path, frame_list in self.path_tk_frame_dict.items():
            image_md5 = md5(path)
            count = frame_list[0].winfo_children()[0]['text']
            save_name = f"{group_num}_{count}_{image_md5}"
            # shutil.copy(path, os.path.join(self.dy_data_utils.get_image_dir(), str(type), f"{save_name}.jpg"))
            print(path, os.path.join(self.dy_data_utils.image_dir(), str(export_type), f"{save_name}.jpg"))

            for frame in frame_list:
                #拷贝效果
                if frame.winfo_children()[4]['text'] != "":
                    effect_path = frame.winfo_children()[3]['text']
                    effect_id = frame.winfo_children()[7]['text']
                    # shutil.copy(str(effect_path), os.path.join(self.dy_data_utils.get_effects_dir(), effect_id, f"{save_name}.mp4"))
                    print(str(effect_path), os.path.join(self.dy_data_utils.effects_dir(), effect_id, f"{save_name}.mp4"))

                #拷贝合成
                if frame.winfo_children()[6]['text'] != "":
                    compose_path = frame.winfo_children()[5]['text']
                    compose_id = frame.winfo_children()[8]['text']
                    # shutil.copy(str(compose_path), os.path.join(self.dy_data_utils.get_compose_dir(), compose_id, f"{save_name}.jpg"))
                    print(str(compose_path), os.path.join(self.dy_data_utils.compose_dir(), compose_id, f"{save_name}.jpg"))

if __name__ == "__main__":
    analyse = AddData()
    analyse.mainloop()