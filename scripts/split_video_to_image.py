import os
import cv2
import functools
from data_util import *


if __name__ == "__main__":
    video_path = "/Users/meitu/Downloads/一眼就心动的头像2.mp4"
    save_dir = ""
    frame_interval = 30

    video_cap = cv2.VideoCapture(video_path)

    frame_count = 1
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    while video_cap.isOpened():
        ret, frame = video_cap.read()

        if ret and frame_count % frame_interval == 0:
            cv2.imwrite(os.path.join(save_dir, video_name + ".jpg"), frame)

        frame_count += 1