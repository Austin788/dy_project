import numpy as np
import math
import cv2
import random
import shutil
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
import json
import sys
from enum import Enum


# TextPosition = Enum("Position", ('CENTER', 'TOP'))

def border_text_draw(draw, pos, text, font, fill=None, border='black', bp=1):
    x, y = pos
    shadowcolor = border
    draw.text((x - bp, y), text, font=font, fill=shadowcolor)
    draw.text((x + bp, y), text, font=font, fill=shadowcolor)
    draw.text((x, y - bp), text, font=font, fill=shadowcolor)
    draw.text((x, y + bp), text, font=font, fill=shadowcolor)
    # thicker border
    draw.text((x - bp, y - bp), text, font=font, fill=shadowcolor)
    draw.text((x + bp, y - bp), text, font=font, fill=shadowcolor)
    draw.text((x - bp, y + bp), text, font=font, fill=shadowcolor)
    draw.text((x + bp, y + bp), text, font=font, fill=shadowcolor)
    # now draw the text over it
    draw.text((x, y), text, font=font, fill=fill)


class TextWriter():
    def __init__(self, title_content, text_font_path, text_color, target_width_ratio=0.7, padding_y=5, min_y=70):
        self.title_content = title_content
        self.text_font_path = text_font_path
        self.text_color = text_color
        self.target_width_ratio = target_width_ratio
        self.min_y = min_y
        self.padding_y = padding_y

        self.font = None
        self.top_position = None
        self.center_position = None

    def get_max_title(self):
        max_len = -1
        max_title = None
        for title in self.title_content:
            if len(title) > max_len:
                max_len = len(title)
                max_title = title
        return max_title

    @staticmethod
    def find_font_size(text, font, image, target_width_ratio):
        tested_font_size = 100
        tested_font = ImageFont.truetype(font, tested_font_size)
        observed_width, observed_height = TextWriter.get_text_size(text, image, tested_font)
        estimated_font_size = tested_font_size / (observed_width / image.width) * target_width_ratio
        return round(estimated_font_size)

    @staticmethod
    def get_text_size(text, image, font):
        im = Image.new('RGB', (image.width, image.height))
        draw = ImageDraw.Draw(im)
        return draw.textsize(text, font)

    def add_title_text(self, image, position):
        # 变色效果
        pilimg = Image.fromarray(cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_BGR2RGB))

        if self.font is None:
            font_size = TextWriter.find_font_size(self.get_max_title(), self.text_font_path, pilimg,
                                                  target_width_ratio=self.target_width_ratio)
            self.font = ImageFont.truetype(self.text_font_path, font_size, encoding="utf-8")

            self.observed_width, self.observed_height = TextWriter.get_text_size(self.get_max_title(), pilimg,
                                                                                 self.font)

            title_height = self.observed_height * len(self.title_content) + self.padding_y * (
                len(self.title_content) - 1)

            self.top_min_y = max(self.min_y, 400 - title_height)
            self.center_min_y = max(self.min_y, (pilimg.height - title_height) / 2)

        draw = ImageDraw.Draw(pilimg)

        for i, title in enumerate(self.title_content):
            if position == "TOP":

                observed_width, _ = TextWriter.get_text_size(title, pilimg, self.font)
                position = (
                    (pilimg.width - observed_width) / 2, self.top_min_y + i * (self.observed_height + self.padding_y))

            if position == "CENTER":
                observed_width, _ = TextWriter.get_text_size(title, pilimg, self.font)
                position = (
                    (pilimg.width - observed_width) / 2,
                    self.center_min_y + i * (self.observed_height + self.padding_y))
            # draw.text(position, title, fill=self.text_color, font=self.font)
            border_text_draw(draw, position, title, fill=self.text_color, font=self.font)

        return cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)


def generate_single_video(music_path, stuck_points_path, video_path, image_paths, effect_paths, compose_paths,
                          save_path, title_content=None, text_font_path=None, text_color=None, title_position=None):
    # video_size = video_properties['video_size']  # （宽、高）
    # video_fps = video_properties['video_fps']
    # video_encoding = video_properties['video_encoding']
    # video_background_color = video_properties['video_background_color']


    video_size = (1080, 1920)  # （宽、高）
    video_fps = 30
    video_encoding = cv2.VideoWriter_fourcc(*'XVID')
    video_background_color = (0, 0, 0)

    if os.path.exists(video_path):
        stuck_points = read_stuck_points(stuck_points_path, points_num=len(image_paths) * 2 + 1)
    else:
        stuck_points = read_stuck_points(stuck_points_path, points_num=len(image_paths) * 2)
        stuck_points = [0] + stuck_points

    # 设置统一的背景图片
    background_image = np.zeros((video_size[1], video_size[0], 3))
    for RGB_id, RGB_value in enumerate(video_background_color):
        background_image[:, :, RGB_id] = RGB_value

    # 视频输出流
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))
    video_out = cv2.VideoWriter(save_path, video_encoding, video_fps, video_size)

    if title_content is not None and len(title_content) > 0 and os.path.exists(text_font_path) and text_color is not None:
        text_writer = TextWriter(title_content, text_font_path, text_color)
    else:
        text_writer = None

    # part one
    # 无开头素材视频
    if video_path == '':
        stuck_points.insert(0, 0)

    part_one_duration = stuck_points[0]
    part_one_frames_num = int(part_one_duration * video_fps)
    part_one_frames = read_video(video_path)

    # 视频太短进行插针处理
    if len(part_one_frames) < part_one_frames_num:
        part_one_frames = video_frame_interpolation(part_one_frames, part_one_frames_num)

    frames_start_id = random.randint(0, len(part_one_frames) - part_one_frames_num)
    part_one_frames = part_one_frames[frames_start_id:frames_start_id + part_one_frames_num]
    for frame in part_one_frames:
        frame_out = adjust_frame(background_image.copy(), frame)
        if text_writer is not None:
            frame_out = text_writer.add_title_text(frame_out, title_position)
        video_out.write(np.uint8(frame_out))

    # part two
    frames_start_id = 0
    for image_id in range(len(image_paths)):
        source_image_path = image_paths[image_id]
        effect_video_path = effect_paths[image_id]
        compose_image_path = compose_paths[image_id]

        # part two-1
        part_two_duration_1 = stuck_points[image_id * 2 + 1] - stuck_points[image_id * 2]
        part_two_frame_num_1 = int(part_two_duration_1 * video_fps)
        part_two_frames_1 = read_video(effect_video_path)
        # 视频太短进行插针处理
        if len(part_two_frames_1) < part_two_frame_num_1:
            part_two_frames_1 = video_frame_interpolation(part_two_frames_1, part_two_frame_num_1)
        # elif (len(part_two_frames_1) // part_two_frame_num_1) > 2: # 效果视频太长，只能截取一小部分，效果展现不完整
        #     part_two_frames_1 = video_frame_extract(part_two_frames_1, part_two_frame_num_1)
        # 使得一个视频内的特效视频截取的开始位置一致，视频看起来比较统一
        if frames_start_id == 0:
            frames_start_id = random.randint(0, len(part_two_frames_1) - part_two_frame_num_1)
        part_two_frames_1 = part_two_frames_1[frames_start_id:frames_start_id + part_two_frame_num_1]
        for frame in part_two_frames_1:
            frame_out = adjust_frame(background_image.copy(), frame)
            # 无开头素材视频时，文字标题则添加在第一张图片的效果上
            if image_id == 0 and len(part_one_frames) == 0:
                if text_writer is not None:
                    frame_out = text_writer.add_title_text(frame_out, title_position)
            video_out.write(np.uint8(frame_out))

        # part two-2
        part_two_duration_2 = stuck_points[image_id * 2 + 2] - stuck_points[image_id * 2 + 1]
        part_two_frame_num_2 = int(part_two_duration_2 * video_fps)
        frame = cv2.imread(compose_image_path)
        frame_out = adjust_frame(background_image.copy(), frame)
        for i in range(part_two_frame_num_2):
            video_out.write(np.uint8(frame_out))

    video_out.release()
    add_music_to_video(save_path, music_path)

    print('video complete!')


def read_stuck_points(stuck_points_path, points_num):
    with open(stuck_points_path) as f:
        stuck_points_info = json.load(f)

    nearest_list = None
    if "stuck_points" in stuck_points_info:
        if str(points_num) in stuck_points_info['stuck_points']:
            return stuck_points_info['stuck_points'][str(points_num)]
        else:
            nearest_num = sys.maxsize
            for key, value in stuck_points_info['stuck_points'].items():
                if int(key) > points_num and int(key) < nearest_num:
                    nearest_num = key
                    nearest_list = value
            return nearest_list

    return nearest_list


def set_save_path(save_path, music_path, video_path, image_paths, id):
    music_name = music_path.split('/')[-1].replace('.')[0]
    video_name = video_path.split('/')[-1].replace('.')[0]
    image_name = ''
    for image_path in image_paths:
        image_name = image_name + image_path.split('/')[-1].replace('.')[0]
    save_path = os.path.join(save_path, music_name + '_' + video_name + '_' + image_name + '_' + str(id) + '.mp4')
    return save_path


# 输出不能覆盖原地址，可能导致画面卡住
def add_music_to_video(video_path, music_path):
    my_clip = VideoFileClip(video_path)
    audio_background = AudioFileClip(music_path)
    final_clip = my_clip.set_audio(audio_background)
    tmp_path = os.path.join(os.path.abspath("."), 'tmp.mp4')
    final_clip.write_videofile(tmp_path, audio_codec='aac')
    shutil.copyfile(tmp_path, video_path)
    os.remove(tmp_path)


def adjust_frame(background, frame):
    resize_width = int(background.shape[1])
    resize_height = int(background.shape[1] / frame.shape[1] * frame.shape[0])
    frame = cv2.resize(frame, (resize_width, resize_height))
    start_row = int((background.shape[0] - frame.shape[0]) / 2)
    if start_row < 0:
        cover_frame = frame[start_row * -1:start_row * -1 + background.shape[0]]
        start_row = 0
    else:
        cover_frame = frame
    background[start_row:start_row + cover_frame.shape[0], :, :] = cover_frame
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


def video_frame_extract(video_frames, expect_frames_num):
    # TODO 视频跳帧提取
    extract_ratio = int(math.floor(len(video_frames) / expect_frames_num))
    video_frames_extrct = list()
    extract_frame_id = 0
    while extract_frame_id < len(video_frames):
        video_frames_extrct.append(video_frames[extract_frame_id])
        extract_frame_id = extract_frame_id + extract_ratio
    return video_frames_extrct


def video_frame_interpolation(video_frames, expect_frames_num):
    # TODO 视频插帧（简单拼接）
    expand_ratio = int(math.ceil(expect_frames_num / len(video_frames)))
    video_frames_interpolated = video_frames * expand_ratio
    return video_frames_interpolated


if __name__ == '__main__':
    parmater = {'music_path': '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/music/这头像太适合你兄弟了.mp3',
                'stuck_points_path': '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/music/这头像太适合你兄弟了.json',
                'video_path': 'None', 'image_paths': [
            '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image/胖子奥特曼/1_17_51ef0edc2f97853ff5d44ace8c7123de.jpg',
            '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image/胖子奥特曼/1_16_f0558b245fbaf104d3fb7d6786264681.jpg',
            '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image/胖子奥特曼/1_15_a1c66aad30a94f7737f55bad66caa7c4.jpg',
            '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image/胖子奥特曼/1_14_ca0af621aabe36ab8cf3fe43619579cc.jpg',
            '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image/胖子奥特曼/1_13_0e01c75c64e4a3034d3105d0e33eb3f1.jpg'],
                'effect_paths': [
                    '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_effects/3D运镜/1_17_51ef0edc2f97853ff5d44ace8c7123de.mp4',
                    '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_effects/3D运镜/1_16_f0558b245fbaf104d3fb7d6786264681.mp4',
                    '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_effects/3D运镜/1_15_a1c66aad30a94f7737f55bad66caa7c4.mp4',
                    '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_effects/3D运镜/1_14_ca0af621aabe36ab8cf3fe43619579cc.mp4',
                    '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_effects/3D运镜/1_13_0e01c75c64e4a3034d3105d0e33eb3f1.mp4'],
                'compose_paths': [
                    '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_compose/合成_4/1_17_51ef0edc2f97853ff5d44ace8c7123de.jpg',
                    '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_compose/合成_4/1_16_f0558b245fbaf104d3fb7d6786264681.jpg',
                    '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_compose/合成_4/1_15_a1c66aad30a94f7737f55bad66caa7c4.jpg',
                    '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_compose/合成_4/1_14_ca0af621aabe36ab8cf3fe43619579cc.jpg',
                    '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_compose/合成_4/1_13_0e01c75c64e4a3034d3105d0e33eb3f1.jpg'],
                'save_path': '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/device/000000导出测试/待发送/这头像太适合你兄弟了.mp3__51ef0edc2ff0558b245fa1c66aad30ca0af621aa_3D运镜_合成_4.mp4',
                'title_content': ['这头像太适合我兄弟了'],
                'text_font_path': '/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/fonts/新青年体.ttf',
                'text_color': (255, 255, 255), 'title_position': 'CENTER'}

    generate_single_video(**parmater)
