# -*- encoding=utf-8 -*-
import os
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
from PIL import Image, ImageTk


sheet_unit_len = 30

"""
引力魔方分析工具
"""

time_now = str(datetime.now().strftime('%Y-%m-%d'))
title_list = {'出价': 0, '消耗': 1, '投资回报率': 2, '点击量': 3, '添加购物车量': 4, '成交订单量': 5, '点击成本': 6, '成交订单金额': 7, '点击率': 8,
                      '收藏宝贝': 9, '展现量': 10}

def insert(df, i, df_add):
    # 指定第i行插入一行数据
    df1 = df.iloc[:i, :]
    df2 = df.iloc[i:, :]
    df_new = pd.concat([df1, df_add, df2], ignore_index=True)
    return df_new


def is_interger(s, precision=10000):
    try:
        f_v = float(s)
        if f_v * precision - int(f_v) * precision == 0:
            return True
        else:
            return False
    except ValueError:
        pass

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def strformat(float_value, int_length=4, dot_length=2):
    str_value = str(round(float(float_value), dot_length))
    dot_index = str_value.find('.')

    if dot_index == -1:
        add_dot_length = dot_length
        add_int_length = int_length - len(str_value)
    else:
        int_str = str_value[:dot_index]
        dot_str = str_value[dot_index + 1:]
        add_int_length = int_length - len(int_str)
        add_dot_length = dot_length - len(dot_str)
    if add_int_length > 0:
        str_value = '  ' * add_int_length + str_value
    if dot_index == -1:
        str_value = str_value + '.'
    if add_dot_length > 0:
        str_value = str_value + '0' * add_dot_length
    return str_value








class AddData(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        # win = tk.Tk()  # 窗口
        self.title('数据分析')  # 标题
        screenwidth = self.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.winfo_screenheight()  # 屏幕高度
        print(screenwidth, screenheight)
        width = screenwidth
        height = screenheight
        x = int((screenwidth - width) / 2)
        y = int((screenheight - height) / 2)

        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置
        # self.main_frame = tk.Frame(self, width=width, height=height)
        # self.main_frame.grid(row=3, column=7)

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        #

        self.save_path = tk.StringVar()
        self.analyse_days = tk.StringVar()

        self.store_value = tk.StringVar(self)

        self.default_save = r'/Users/meitu/Documents/midlife_crisis/python_script/data/'
        self.default_days = 9

        self.save_path.set(self.default_save)
        self.analyse_days.set(self.default_days)
        # # Dictionary to create multiple buttons


        button_width = 15
        tk.Label(self, text="数据类型:").grid(row=0, column=0, ipadx=10, ipady=10)

        # # Dictionary to create multiple buttons
        values = {"图片+效果+合成": "图片效果合成",
                  "图片+合成": "图片合成",
                  "图片": "图片"
                  }
        count = 1
        # Loop is used to create multiple Radiobuttons
        # rather than creating each button separately
        for (text, value) in values.items():
            tk.Radiobutton(self, text=text, variable=self.store_value, value=value, indicator=0, width=button_width).grid(row=0,
                                                                                                                 column=count)
            count += 1

        self.notebook = ttk.Notebook(self, height=screenheight-50)
        # self.table_frame = ttk.Frame(self.notebook)
        self.table_frame = tk.Canvas(self.notebook, bg="white")
        # sv = Scrollbar(self.table_frame)  # 定义垂直滚动条
        # sv.pack(side=RIGHT, fill=Y)  # 放置垂直滚动条在最右侧,占满Y轴
        # self.table_frame.config(yscrollcommand=sv.set)  # 设置画布的Y轴滚动条函数与垂直滚动条绑定
        # self.table_frame.config(scrollregion=(0, 0, self.table_frame.winfo_width(), self.table_frame.winfo_height()))  # 设置画布可以滚动的范围
        # sv.config(command=self.table_frame.yview)  # 设置垂直滚动条的函数与画布的Y轴滚动条事件绑定
        # self.table_frame.config(yscrollincrement=1)  # 设置滚动条的步长
        # self.table_frame.bind("<MouseWheel>", self.event1)  # 添加滚轮事件


        tk.Button(self, text="添加", command=lambda :self.add(self.table_frame), width=button_width).grid(row=0, column=4)
        tk.Button(self, text="删除", command=self.add, width=button_width).grid(row=0, column=5)
        tk.Button(self, text="执行", command=self.add, width=button_width).grid(row=0, column=6)

        self.sv = Scrollbar(self.table_frame)  # 定义垂直滚动条
        self.sv.pack(side=RIGHT, fill=Y)  # 放置垂直滚动条在最右侧,占满Y轴
        self.table_frame.config(yscrollcommand=self.sv.set)  # 设置画布的Y轴滚动条函数与垂直滚动条绑定
        self.table_frame.config(scrollregion=(0, 0, 1440, 900))  # 设置画布可以滚动的范围
        self.sv.config(command=self.table_frame.yview)  # 设置垂直滚动条的函数与画布的Y轴滚动条事件绑定
        self.table_frame.config(yscrollincrement=5)  # 设置滚动条的步长
        self.table_frame.bind("<MouseWheel>", self.event1)  # 添加滚轮事件
        #
        # xscroll = Scrollbar(self.table_frame, orient=HORIZONTAL)
        # yscroll = Scrollbar(self.table_frame, orient=VERTICAL)

        # self.columns = ['名称', '近几日消耗、成交、回报、加购比、点击率、单价', '近3日回报', '近7日回报', '近14日回报', '累计消耗回报', '系统建议']
        # self.table = ttk.Treeview(
        #     master=self.table_frame,  # 父容器
        #     height=5,  # 表格显示的行数,height行
        #     columns=self.columns,  # 显示的列
        #     show='headings',  # 隐藏首列
        #     xscrollcommand=xscroll.set,  # x轴滚动条
        #     yscrollcommand=yscroll.set,  # y轴滚动条
        # )
        #
        # for column in self.columns:
        #     self.table.heading(column=column, text=column, anchor=CENTER,
        #                        command=lambda name=column:
        #                        messagebox.showinfo('', '{}描述信息~~~'.format(name)))  # 定义表头
        #     self.table.column(column=column, width=60, minwidth=0, anchor=NW, )  # 定义列
        # self.table.column(column='系统建议', width=100, minwidth=0, anchor=NW, )  # 定义列

        # xscroll.config(command=self.table_frame.xview)
        # xscroll.pack(side=BOTTOM, fill=X)
        # yscroll.config(command=self.table_frame.yview)
        # yscroll.pack(side=RIGHT, fill=Y)
        # self.table.pack(fill=BOTH, expand=True)

        # style = ttk.Style(self.table_frame)
        # style.configure('Treeview', rowheight=120)

        self.notebook.add(self.table_frame, text="添加列表")
        self.notebook.grid(row=1, columnspan=7, sticky=tk.NSEW)

        self.photo_list = []

    def event1(self, event):
        """
        事件的属性 delta 解析
        在MouseWheel 事件中,正值代表上卷,负值代表下卷;
        在 Window 下,通常是 120 的倍数;在 MacOS 下,为 1 的倍数
        """
        self.table_frame.configure(scrollregion=self.table_frame.bbox("all"), width=1440, height=900)
        number = int(-event.delta / 120)
        self.table_frame.yview_scroll(number, 'units')

    def select_save_path(self):
        save_path = tk.filedialog.askdirectory(initialdir=self.default_save)
        if save_path is None:
            return
        self.save_path.set(save_path)

    def add(self, widget):
        row = tk.Frame(widget)
        _SIZE=200
        image1 = Image.open("/Users/meitu/Downloads/33333.png")
        image1 = image1.resize((_SIZE, _SIZE))
        tk_image1 = ImageTk.PhotoImage(image1)
        self.photo_list.append(tk_image1)
        comment_img1 = tk.Canvas(widget, bg="white", width=_SIZE, height=_SIZE)
        comment_img1.create_image(0, 0, image=tk_image1, anchor="nw")
        comment_img1.pack()
        row.pack(fill=X)

    def say_hi(self):
        print("hello ~ !")

    def analyse(self):
        print("bb")

    def get_line_chart_data_list(self, sheet, key_list):
        date_list = []
        data_list = []
        for i in range(len(key_list)):
            data_list.append([])

        for i in range(0, len(sheet)):
            current_time = dt.datetime.strptime(str(sheet.iloc[i]['调整时间']), "%Y-%m-%d %H:%M:%S")
            if i == 0 or (current_time.hour == 23 and current_time.minute == 59 and current_time.second == 59):
                date_list.append(current_time.strftime('%m.%d'))
                for j, key in enumerate(key_list):
                    data_list[j].append(float(str(sheet.iloc[i][key])))
        return date_list, data_list



    def insert(self):
        self.notebook.select(1)
        # self.tabel_frame.pack_forget() if self.tabel_frame.winfo_manager() else self.tabel_frame.pack(fill=BOTH, expand=True)

if __name__ == "__main__":
    analyse = AddData()
    analyse.mainloop()