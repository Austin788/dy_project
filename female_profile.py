import os
import cv2
import random
import contextlib
import wave
from pydub import AudioSegment
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *

# 直接打印文字
def add_text_simple(image, frame_size):

    text_content_1 = "爱了这头像"

    # 按字符串长的计算
    font_size = int(frame_size[1] / (len(text_content_1) + 6))
    # 变色效果
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    # color = (255, 0, random.randint(0, 255))

    cv2img = cv2.cvtColor( image.astype(np.uint8), cv2.COLOR_BGR2RGB)
    pilimg = Image.fromarray(cv2img)

    # PIL图片上打印汉字
    draw = ImageDraw.Draw(pilimg)
    font = ImageFont.truetype("TTF/1.ttf", font_size, encoding="utf-8")
    draw.text((int(font_size * 3), int((frame_size[0] - font_size) / 2 )), text_content_1, color, font=font)

    # 英文长短要压缩一半
    cv2charimg = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)

    cv2.imshow('im', cv2charimg)
    cv2.waitKey(-1)

    return cv2charimg


def add_music(video_path, music_path):
    video = VideoFileClip(video_path)
    videos = video.set_audio(AudioFileClip(music_path))  # 音频文件
    videos.write_videofile(video_path)


# 设置生成视频的帧率， 【似乎素材都是等于30】
video_fps = 30
# 设置视频的分辨率【9:16】
video_size = [1080, 1920] # 【1080, 1920】 None则根据第一段素材分辨率生成【9:16】对应的大小

# 存放音乐
music_dir = 'music'
# 存放原图
# data
#   - 1-1
#   - 1-2
#       -[(1.jpg, 1-1.jpg, 1-2.mp4)、(2.jpg, 2-1.jpg, 2-2.mp4)...]
source_data = 'H:/dy_data/8.13'
# 开头图片
begin_image_dir = 'begin_image'
# 保存路径
video_save_dir = 'H:/dy_data/0814/female'

music_name = os.listdir(music_dir)
begin_immage_names = os.listdir(begin_image_dir)
group_names = os.listdir(source_data)

# TODO 目前只能预先定义好对应要的bgm要卡点的位置
mp3_position = [1.1, 1.9, 2.6, 3.4, 4.2, 5.0, 5.7, 6.5, 7.3, 8.1, 8.8]
# 视频展示头像图片的数量，第一个间隔是放热门吸引素材视频
image_number_per_video = int((len(mp3_position) - 1) / 2)

for group_name in group_names:
    group_path = os.path.join(source_data, group_name)

    frame_size = [video_size[1], video_size[0]]
    background_image = np.zeros((frame_size[0], frame_size[1], 3))

    video_save_path = os.path.join(video_save_dir, group_name +'.mp4')
    video_out = cv2.VideoWriter(video_save_path, cv2.VideoWriter_fourcc(*'XVID'), video_fps, (frame_size[1], frame_size[0]))

    # 处理开头素材部分

    # 开头素材部分总帧数
    part_0_frame_num = int(mp3_position[0] * video_fps)
    begin_image_id = random.randint(0, len(begin_immage_names) - 1)
    begin_image_path = os.path.join(begin_image_dir, begin_immage_names[begin_image_id])
    begin_image = cv2.imread(begin_image_path)
    begin_image = cv2.resize(begin_image, (frame_size[1], int(frame_size[1] / begin_image.shape[1] * begin_image.shape[0])))
    height_start = int((frame_size[0] - begin_image.shape[0])/2)
    while part_0_frame_num:
        new_frame = background_image.copy()
        new_frame[height_start:height_start+begin_image.shape[0], :, :] = begin_image
        video_out.write(np.uint8(new_frame))
        part_0_frame_num = part_0_frame_num - 1

    # 随机选取后面头像

    image_names = []
    for image_name in os.listdir(group_path):
        if image_name.find('-') == -1:
            image_names.append(image_name)
    random_numbers = random.sample(range(len(image_names)), int((len(mp3_position) - 1) / 2))
    for part_id, image_id in enumerate(random_numbers):
        source_image_path = os.path.join(group_path, image_names[image_id])
        render_image_path = source_image_path.replace('.jpg', '-2.mp4')
        show_image_path = source_image_path.replace('.jpg', '-1.jpg')

        # 头像第一部分
        part_cap = cv2.VideoCapture(render_image_path)
        part_1_0_frame_num = int((mp3_position[part_id * 2 + 1] - mp3_position[part_id * 2]) * video_fps)
        part_cap_frame_num = part_cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if (part_cap_frame_num - part_1_0_frame_num) < 0:
            # TODO 要保证运镜后视频大于所需的长度
            assert 'render video error!'
            exit()
        part_1_0_start_frame_id = random.randint(0, (part_cap_frame_num - part_1_0_frame_num))
        while part_cap.isOpened() and part_1_0_start_frame_id >= 0:

            ret, frame = part_cap.read()
            if not ret or part_1_0_start_frame_id > 0:
                part_1_0_start_frame_id = part_1_0_start_frame_id - 1
                continue

            new_frame = background_image.copy()

            frame = cv2.resize(frame, (int(frame_size[1]), int(frame_size[1] / frame.shape[1] * frame.shape[0])))
            part_1_0_height_start = int((frame_size[0] - frame.shape[0]) / 2)
            new_frame[part_1_0_height_start:part_1_0_height_start + frame.shape[0], :, :] = frame
            video_out.write(np.uint8(new_frame))
            part_1_0_frame_num = part_1_0_frame_num - 1
            if part_1_0_frame_num == 0:
                break

        # 头像第二部分
        part_1_1_frame_num = int((mp3_position[part_id * 2 + 2] - mp3_position[part_id * 2 + 1]) * video_fps)
        show_image = cv2.imread(show_image_path)
        new_frame = background_image.copy()
        show_image = cv2.resize(show_image, (int(frame_size[1]), int(frame_size[1] / show_image.shape[1] * show_image.shape[0])))
        part_1_1_height_start = int((frame_size[0] - show_image.shape[0]) / 2)
        new_frame[part_1_1_height_start:part_1_1_height_start + show_image.shape[0], :, :] = show_image
        while part_1_1_frame_num:
            video_out.write(np.uint8(new_frame))
            part_1_1_frame_num = part_1_1_frame_num - 1

    video_out.release()

    # 音乐处理部分
    # music_path = 'music/female.mp3'  # 视频文件
    # add_music(video_save_path, music_path)

    print('complete {} !'.format(group_name))