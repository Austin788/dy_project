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
    image_dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image"

    save_dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_effects/摇摆运镜星火炸开"
    video_path = "/Users/meitu/Downloads/CB0CC170-F59E-44FE-85C8-234F3CC27D14.MOV"

    save_dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_effects/摇摆运镜"
    video_path = "/Users/meitu/Downloads/1622E6B2-44E2-4EC6-AE2C-0B9001143783.MOV"

    save_dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_effects/3D运镜"
    video_path = "/Users/meitu/Downloads/445B95D3-C093-49A3-A967-A5C68ABF4107.MOV"

    save_dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_effects/3D运镜星火炸开"
    video_path = "/Users/meitu/Downloads/FD39ADBA-212F-4B94-BF54-61083C7C1C89.MOV"

    # save_dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_effects/3D运镜屏幕律动"
    # save_dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data_fast/image_effects/3D运镜屏幕扫描"


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
    video_count = 0
    while video_cap.isOpened():
        ret, frame = video_cap.read()
        # cv2.imshow("f", frame)
        # cv2.waitKey(1)
        if ret:
            # if frame_count % 88 == 0:
            if frame_count % 94 == 0:
                if video_out is not None:
                    video_out.release()
                # video_count += 1
                # if video_count == 11:
                #     continue
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