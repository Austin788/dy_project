import os
import numpy as np
import time
import math
import cv2
import random
import shutil
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *


##### 管理数据界面 #####
# 地址格式：目标目录/[男头、女头]/[数据类型]/[日期]/文件类型_id.后缀
DATA_DIR = ''
DATA_TYPE = {
    1: 'image_render_synthetise',
    2: 'image_synthetise',
    3: 'image_render',
    4: 'image'
}
PROFILE_TYPE = {
    1: 'female',
    2: 'male'
}
VIDEO_TYPE = {
    1: 'use_begin_video',
    2: 'no_begin_video'
}

def manage_data(data_type, profile_type, image_list, render_list, synthetise_list):
    data_list = list()
    if data_type == 1:
        if len(image_list) == len(render_list) and len(image_list) == len(synthetise_list) and len(image_list) > 0:
            data_list = [image_list, render_list, synthetise_list]
        else:
            raise ValueError("data error!")
    elif data_type == 2:
        if len(image_list) == len(synthetise_list) and len(image_list) > 0:
            data_list = [image_list, synthetise_list]
        else:
            raise ValueError("data error!")
    elif data_type == 3:
        if len(image_list) == len(render_list) and len(image_list) > 0:
            data_list = [image_list, render_list]
        else:
            raise ValueError("data error!")
    else:
        if len(image_list) > 0:
            data_list = [image_list]
        else:
            raise ValueError("data error!")

    target_dir = os.path.join(DATA_DIR, PROFILE_TYPE[profile_type], DATA_TYPE[data_type], time.strftime('%Y-%m-%d', time.localtime()))
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for i, path_list in enumerate(data_list):
        file_name_prefixs = DATA_TYPE[data_type].split('_')
        for id, file_path in enumerate(path_list):
            file_dst_path = os.path.join(target_dir, file_name_prefixs[i]+'_'+str(id)+'.'+file_path.split('.')[-1])
            shutil.copyfile(file_path, file_dst_path)


def main(music_path, stuck_points, title_content, text_font_path, text_color, video_path, image_paths, video_properties,
         save_path, video_type, generate_num):
    if video_type == 2:
        # 卡点时间列开头加个0
        stuck_points.insert(0, 0)

    for id in range(generate_num):
        random.shuffle(image_paths)
        save_path = set_save_path(save_path, music_path, video_path, image_paths, id)
        generate_single_video(music_path, stuck_points, title_content, text_font_path, text_color, video_path,
                              image_paths, video_properties, save_path)


def generate_single_video(music_path, stuck_points, title_content, text_font_path, text_color, video_path, image_paths,
                          video_properties, save_path):
    video_size = video_properties['video_size'] # （宽、高）
    video_fps = video_properties['video_fps']
    video_encoding = video_properties['video_encoding']
    video_background_color = video_properties['video_background_color']
    video_frames_num = int(stuck_points[-1] * video_fps) # 总帧数

    # 设置统一的背景图片
    background_image = np.zeros((video_size[1], video_size[0], 3))
    for RGB_id, RGB_value in enumerate(video_background_color):
        background_image[:, :, RGB_id] = RGB_value

    # 视频输出流
    video_out = cv2.VideoWriter(save_path, video_encoding, video_fps, video_size)

    # part one
    part_one_duration = stuck_points[0]
    part_one_frames_num = int(part_one_duration * video_fps)
    part_one_frames = read_video(video_path)

    # 视频太短进行插针处理
    if len(part_one_frames) < part_one_frames_num:
        part_one_frames = video_frame_interpolation(part_one_frames, part_one_frames_num)

    frames_start_id = random.randint(0, len(part_one_frames)-part_one_frames_num)
    part_one_frames = part_one_frames[frames_start_id:frames_start_id+part_one_frames_num]
    for frame in part_one_frames:
        frame_out = adjust_frame(background_image.copy(), frame)
        frame_out = add_title_text(frame_out, title_content, text_font_path, text_color)
        video_out.write(frame_out)

    # part two
    # image_order = random.sample(range(len(image_paths)), len(image_paths))
    image_order = range(len(image_paths))
    for part_id, image_id in enumerate(image_order):
        source_image_path = image_paths[image_id]
        render_video_path = image_paths[image_id]
        show_image_path = image_paths[image_id]

        # part two-1
        part_two_duration_1 = stuck_points[part_id * 2 + 1] - stuck_points[part_id * 2]
        part_two_frame_num_1 = int(part_two_duration_1 * video_fps)
        part_two_frames_1 = read_video(render_video_path)
        # 视频太短进行插针处理
        if len(part_two_frames_1) < part_two_frame_num_1:
            part_two_frames_1 = video_frame_interpolation(part_two_frames_1, part_two_frame_num_1)
        frames_start_id = random.randint(0, len(part_two_frames_1) - part_two_frame_num_1)
        part_two_frames_1 = part_two_frames_1[frames_start_id:frames_start_id + part_two_frame_num_1]
        for frame in part_two_frames_1:
            frame_out = adjust_frame(background_image.copy(), frame)
            video_out.write(frame_out)

        # part two-2
        part_two_duration_2 = stuck_points[part_id * 2 + 2] - stuck_points[part_id * 2 + 1]
        part_two_frame_num_2 = int(part_two_duration_2 * video_fps)
        frame = cv2.imread(show_image_path)
        frame_out = adjust_frame(background_image.copy(), frame)
        for i in range(part_two_frame_num_2):
            video_out.write(frame_out)

    video_out.release()
    add_music(save_path, music_path)

    print('video complete!')


def set_save_path(save_path, music_path, video_path, image_paths, id):
    music_name = music_path.split('/')[-1].replace('.')[0]
    video_name = video_path.split('/')[-1].replace('.')[0]
    image_name = ''
    for image_path in image_paths:
        image_name = image_name + image_path.split('/')[-1].replace('.')[0]
    save_path = os.path.join(save_path, music_name + '_' + video_name + '_' + image_name + '_' + str(id) + '.mp4')
    return save_path


def add_music(video_path, music_path):
    video = VideoFileClip(video_path)
    videos = video.set_audio(AudioFileClip(music_path))  # 音频文件
    videos.write_videofile(video_path)


def add_title_text(image, title_content, text_font_path, text_color):
    frame_size = image.shape
    font_size = int(frame_size[1] / (len(title_content) + 4))
    # 变色效果
    # color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    color = text_color
    cv2img = cv2.cvtColor( image.astype(np.uint8), cv2.COLOR_BGR2RGB)
    pilimg = Image.fromarray(cv2img)
    draw = ImageDraw.Draw(pilimg)
    font = ImageFont.truetype(text_font_path, font_size, encoding="utf-8")
    if title_content.isalpha():
        adjust_x = 2
    else:
        adjust_x = 1
    draw_xy = ((int((frame_size[1] - font_size * len(title_content) / adjust_x)) / 2), int(font_size * 4))
    draw.text(draw_xy, title_content, color, font=font)
    cv2charimg = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
    return cv2charimg


def adjust_frame(background, frame):
    resize_width = int(background.shape[1])
    resize_height = int(background.shape[1] / frame.shape[1] * frame.shape[0])
    frame = cv2.resize(frame, (resize_width, resize_height))
    start_row = int((background.shape[0] - frame.shape[0]) / 2)
    if start_row < 0:
        cover_frame = frame[start_row * -1:start_row * -1+background.shape[0]]
        start_row = 0
    else:
        cover_frame = frame
    background[start_row:start_row+cover_frame.shape[0], :, :] = cover_frame
    return background


def read_video(video_path):
    video_cap = cv2.VideoCapture(video_path)
    video_frames = []
    while video_cap.isOpened():
        ret, frame = video_cap.read()
        if ret:
            video_frames.append(frame)
        else:
            break
    return video_frames


def video_frame_interpolation(video_frames, expect_frames_num):
    # TODO 视频插帧（简单拼接）
    expand_ratio = int(math.ceil(expect_frames_num / len(video_frames)))
    video_frames_interpolated = video_frames * expand_ratio
    return video_frames_interpolated


if __name__ == '__main__':
    main()




