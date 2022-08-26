import os
import cv2


if __name__ == "__main__":
    dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/"

    for filename in os.listdir(dir):
        if filename.endswith(".jpg"):
            pic = cv2.imread(os.path.join(dir, filename))
            pic = cv2.resize(pic, (1024, 1024))
            cv2.imwrite(os.path.join(dir, filename[:-4]+".jpg"), pic)