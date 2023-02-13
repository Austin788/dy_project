import tkinter,threading
import BiliccSrt_Down


# BV1m3411P7TG gzip
# BV13f4y1G7sA 无压缩
# BV18a4y1H73s 很多P


def xc():
    xiancheng1 = threading.Thread(target=zzz)   # 定义线程，运行抓取程序
    xiancheng1.start()                          # 让线程开始工作
def zzz():
	BiliccSrt_Down.downAll(avhao.get())


# 单选按钮回调函数,就是当单选按钮被点击会执行该函数
def radCall():
    radSel = radVar.get()
    if radSel == 1:
        BiliccSrt_Down.bianma = 'utf-8'
        print ('编码输出变更为：UTF-8')
    elif radSel == 2:
        BiliccSrt_Down.bianma = 'utf-16'
        print ('编码输出变更为：UTF-16')


### Tk GUI窗口 ###
chaungkou = tkinter.Tk()
chaungkou.title('BLIBILI CC字幕下载器 V4.1')
chaungkou.geometry('400x220')

diyijie = tkinter.Frame(chaungkou)      #第一节
dierjie = tkinter.Frame(chaungkou)      #第二节
disanjie = tkinter.Frame(chaungkou)      #第三节

biaoqian = tkinter.Label(chaungkou,text='BLIBILI CC字幕下载器 V4.1',width=20,height=2,font=("微软雅黑",22))   #标签
biaoqian.pack()

diyijie.pack()  #显示一二三节
dierjie.pack()
disanjie.pack()

tkinter.Label(diyijie,text='目标BV号：',width=8,height=1,font=("微软雅黑",15)).pack(side='left')      #标签
avhao = tkinter.Entry(diyijie)                                                                      #AV号输入框
avhao.pack(side='right')

radVar = tkinter.IntVar()    # 通过tk.IntVar() 获取单选按钮value参数对应的值
rad1 = tkinter.Radiobutton(dierjie,text='UTF-8     ',variable=radVar,value=1,command=radCall,font=("微软雅黑",15))        #单选框
rad1.pack(side='left')

rad2 = tkinter.Radiobutton(dierjie,text='UTF-16',variable=radVar,value=2,command=radCall,font=("微软雅黑",15))
rad2.pack(side='right')

anniu1 = tkinter.Button(disanjie,text='抓取',command=xc,width=15,height=1,font=("微软雅黑",18))        #按钮
anniu1.pack(side='right')

print ('### 编码默认输出：UTF-8。\n### 如果字幕乱码，可尝试选择UTF-16编码。\n')

chaungkou.mainloop()