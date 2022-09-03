import os
import cv2
import functools
from data_util import *



if __name__ == "__main__":
    image_dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image/职业头像"

    # 先用剪映导一遍，保证帧率30
    video_path = "/Users/meitu/Downloads/一眼就心动的头像2.mp4"
    save_dir = os.path.join("/Users/meitu/Downloads/", "split_video_"+os.path.basename(video_path))
    frame_rate = 30
    split_time = [5.3] #剪映上的计时方式 同一组视频的最后一帧

    for i in range(len(split_time)):
        parts = str(split_time[i]).split('.')
        if len(parts) > 1:
            split_time[i] = int(parts[0]) * frame_rate + int(parts[1])
        else:
            split_time[i] = int(parts[0]) * frame_rate


    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    video_size = [1080, 1920]  # （宽、高）
    video_fps = 30
    video_encoding = cv2.VideoWriter_fourcc(*'XVID')

    video_cap = cv2.VideoCapture(video_path)
    width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # video_frames = []
    frame_count = 0
    video_count = 0
    video_out = None
    video_out = cv2.VideoWriter(os.path.join(save_dir, f"video_split{video_count + 1}.mp4"), video_encoding, video_fps,
                                (width, height))
    while video_cap.isOpened():
        ret, frame = video_cap.read()
        # cv2.imshow("f", frame)
        # cv2.waitKey(1)
        if ret:
            if video_count < len(split_time) and frame_count == split_time[video_count]:
                if video_out is not None:
                    video_out.release()
                video_count += 1
                video_out = cv2.VideoWriter(os.path.join(save_dir, f"video_split{video_count + 1}.mp4"), video_encoding, video_fps, (width, height))

            video_out.write(frame)
            frame_count += 1
        else:
            break
    video_out.release()
    # 视频输出流
