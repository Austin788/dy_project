import os
import cv2
import functools
from data_util import *


def cmp(x, y):
    if int(x.split("_")[1]) > int(y.split("_")[1]):
        return -1

    if int(x.split("_")[1]) < int(y.split("_")[1]):
        return 1

    return 0


if __name__ == "__main__":
    image_dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image/姓氏头像"
    save_dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_effects/摇摆运镜"
    video_path = "/Users/meitu/Downloads/D81FF6FC-C414-4FDC-AB21-B439E7BCF6E0.MOV"

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    video_size = [1080, 1920]  # （宽、高）
    video_fps = 30
    video_encoding = cv2.VideoWriter_fourcc(*'XVID')

    data_utils = DYDataUtils()
    filenames = os.listdir(image_dir)
    if ".DS_Store" in filenames:
        filenames.remove(".DS_Store")
    filenames.sort(key=functools.cmp_to_key(cmp), reverse=True)
    filenames = filenames
    # print(filenames)
    # exit(0)

    video_cap = cv2.VideoCapture(video_path)
    width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # video_frames = []
    frame_count = 0
    filenames_count = 0
    video_out = None
    while video_cap.isOpened():
        ret, frame = video_cap.read()
        # cv2.imshow("f", frame)
        # cv2.waitKey(1)
        if ret:
            if frame_count % 88 == 0:
                if video_out is not None:
                    video_out.release()
                video_out = cv2.VideoWriter(os.path.join(save_dir, filenames[filenames_count][:-4]+".mp4"), video_encoding, video_fps, (width, height))
                filenames_count += 1
            else:
                video_out.write(frame)
            frame_count += 1

        else:
            break
    video_out.release()
    # # 视频输出流
    #