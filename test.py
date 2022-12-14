import os
import cv2
import random
import contextlib
import wave
from pydub import AudioSegment
import numpy as np

# 设置需要生成的视频数量
video_number = 10
# 设置生成视频的帧率， 【似乎素材都是等于30】
video_fps = 30
# 设置视频的分辨率【9:16】
video_size = [1080, 1920] # 【1080, 1920】 None则根据第一段素材分辨率生成【9:16】对应的大小

# 存放音乐
music_dir = 'music'
# 存放开头热门素材
begin_video_dir = 'begin_video'
# 存放原图
source_image_dir = 'source_image'
# 存放抖音运镜处理后的视频素材
render_image_dir = 'render_image'
# 存放醒图处理后的图片素材
show_image_dir = 'show_image'
# 保存路径
video_save_dir = 'video_save'

music_name = os.listdir(music_dir)
image_name = os.listdir(source_image_dir)
begin_video_name = os.listdir(begin_video_dir)

# TODO 目前只能预先定义好对应要的bgm要卡点的位置
# mp3_position = [5.9, 6.6, 7.3, 7.9, 8.5, 9.1, 9.8, 10.5, 11.1, 11.8, 12.4]
mp3_position = [5.9, 6.6, 7.3, 7.9, 8.5, 9.1, 9.8, 10.5, 11.1, 11.8, 12.4]
# 视频展示头像图片的数量，第一个间隔是放热门吸引素材视频
image_number_per_video = int((len(mp3_position) - 1) / 2)

for i in range(video_number):

    # TODO 当前用别人的原声且背景上传的话，不需要添加背景音乐
    # 音乐处理部分
    # music_id = random.randint(0, len(music_name) - 1)
    # current_music_path = os.path.join(music_dir, music_name[music_id])
    # music = AudioSegment.from_wav(current_music_path)
    # music[:6000].export("mashup.wav", format="wav")
    # with contextlib.closing(wave.open(current_music_path, 'r')) as music_file:
    #     music_frames = music_file.getnframes()
    #     music_rate = music_file.getframerate()
    #     music_length = music_frames / float(music_rate)
    # image_number_per_video = music_length * video_fps

    # 随机选一个片头素材
    begin_video_id = random.randint(0, len(begin_video_name) - 1)
    begin_video_path = os.path.join(begin_video_dir, begin_video_name[begin_video_id])

    # 素材部分
    begin_video_cap = cv2.VideoCapture(begin_video_path)
    begin_video_fps = begin_video_cap.get(cv2.CAP_PROP_FPS)
    begin_video_frame_num = begin_video_cap.get(cv2.CAP_PROP_FRAME_COUNT)
    begin_video_fourcc = int(begin_video_cap.get(cv2.CAP_PROP_FOURCC))
    begin_video_width = int(begin_video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    begin_video_height = int(begin_video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


    # begin_cut_frame_num = int(begin_video_frame_num / begin_video_fps * mp3_position[1])
    # begin_frame_num = random.randint(begin_video_frame_num - begin_cut_frame_num)

    if video_size is None:
        frame_size = [begin_video_height, begin_video_width]
    else:
        frame_size = [video_size[1], video_size[0]]

    # 开头素材需要生成的分辨率
    begin_video_resize_width = frame_size[1]
    begin_video_resize_height = int(begin_video_resize_width / begin_video_width * begin_video_height)

    background_image = np.zeros((frame_size[0], frame_size[1], 3))

    video_save_path = os.path.join(video_save_dir, str(i) +'.mp4')
    video_out = cv2.VideoWriter(video_save_path, cv2.VideoWriter_fourcc(*'XVID'), int(begin_video_fps), (frame_size[1], frame_size[0]))

    # 处理开头素材部分

    # 开头素材部分总帧数
    part_0_frame_num = int(mp3_position[0] * begin_video_fps)

    # TODO 素材太短直接跳过，后续考虑插帧
    if begin_video_frame_num - part_0_frame_num < 0:
        continue

    # 随机截取素材，以免重复
    part_0_start_frame_id = random.randint(0, (begin_video_frame_num - part_0_frame_num))
    while begin_video_cap.isOpened() and part_0_start_frame_id >= 0:
        ret, frame = begin_video_cap.read()

        # 去掉开头不要部分
        if not ret or part_0_start_frame_id > 0:
            part_0_start_frame_id = part_0_start_frame_id - 1
            continue

        new_frame = background_image.copy()
        # TODO 直接rezie，后续考虑resize后的画质
        frame = cv2.resize(frame, (frame_size[1], begin_video_resize_height))
        # 用于上下居中的目的 下同
        height_start = int((frame_size[0] - begin_video_resize_height) / 2)
        new_frame[height_start:height_start+begin_video_resize_height, :, :] = frame
        video_out.write(np.uint8(new_frame))
        part_0_frame_num = part_0_frame_num - 1
        if part_0_frame_num == 0:
            break

    # 随机选取后面头像
    random_numbers = random.sample(range(len(image_name)), image_number_per_video)

    for part_id, image_id in enumerate(random_numbers):
        source_image_path = os.path.join(source_image_dir, image_name[image_id])
        render_image_path = os.path.join(render_image_dir, image_name[image_id]).replace('.jpg', '.mp4')
        show_image_path = os.path.join(show_image_dir, image_name[image_id])

        # 头像第一部分
        part_cap = cv2.VideoCapture(render_image_path)
        part_1_0_frame_num = int((mp3_position[part_id * 2 + 1] - mp3_position[part_id * 2]) * begin_video_fps)
        part_cap_frame_num = part_cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if part_cap_frame_num - part_1_0_frame_num < 0:
            # TODO 要保证运镜后视频大于所需的长度
            assert 'render video error!'
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
        part_1_1_frame_num = int((mp3_position[part_id * 2 + 2] - mp3_position[part_id * 2 + 1]) * begin_video_fps)
        show_image = cv2.imread(show_image_path)
        new_frame = background_image.copy()
        show_image = cv2.resize(show_image, (int(frame_size[1]), int(frame_size[1] / show_image.shape[1] * show_image.shape[0])))
        part_1_1_height_start = int((frame_size[0] - show_image.shape[0]) / 2)
        new_frame[part_1_1_height_start:part_1_1_height_start + show_image.shape[0], :, :] = show_image
        while part_1_1_frame_num:
            video_out.write(np.uint8(new_frame))
            part_1_1_frame_num = part_1_1_frame_num - 1

    video_out.release()
    print('complete {} !'.format(i))