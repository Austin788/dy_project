import os
import shutil

if __name__ == "__main__":
    video_dir = "/Users/meitu/Documents/midlife_crisis/每日视频/KS"

    for dir_path, _, filenames in os.walk(video_dir):
        for filename in filenames:
            if not filename.endswith(".mp4"):
                continue
            print(filename)
            if len(filename.split("_")) <= 1:
                continue
            koulin = filename.split("_")[1]
            if filename.find("-") == -1:
                continue
            new_filename = filename[filename.find("-")+1:]

            parent_path = os.path.dirname(dir_path)
            new_dir = os.path.basename(dir_path)
            new_path = os.path.join(parent_path, koulin + "_" + new_dir, new_filename)

            old_path = os.path.join(dir_path, filename)
            if not os.path.exists(os.path.dirname(new_path)):
                os.makedirs(os.path.dirname(new_path))

            shutil.move(old_path, new_path)
            # os.remove(old_path)

            if len(os.listdir(os.path.dirname(old_path))) == 0:
                shutil.rmtree(os.path.dirname(old_path))

