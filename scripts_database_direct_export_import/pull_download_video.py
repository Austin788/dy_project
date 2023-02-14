import os
import numpy as np
import shutil

if __name__ == "__main__":
    video_path = "/Volumes/[C] Windows 10/作品保存/作者作品/"
    save_dir = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data/素材库/download_video"
    save_filenames = "exists_filenames.npz"


    npz_path = os.path.join(save_dir, save_filenames)

    if os.path.exists(npz_path):
        data = np.load(npz_path, allow_pickle=True)
        exist_filenames = set(data['arr_0'].tolist())

    else:
        exist_filenames = set()

    count = 0
    for dir_path, _, filenames in os.walk(video_path):
        for filename in filenames:
            if not filename.endswith(".mp4") or filename.startswith('.'):
                continue

            file_path = os.path.join(dir_path, filename)
            file_size = os.path.getsize(file_path)

            if file_size < 1024:
                continue


            relative_path = file_path.replace(video_path, "")
            dst_path = os.path.join(save_dir, relative_path)

            if relative_path in exist_filenames:
                continue

            if not os.path.exists(os.path.dirname(dst_path)):
                os.makedirs(os.path.dirname(dst_path))

            shutil.move(file_path, dst_path)
            # shutil.copy(file_path, dst_path)
            with open(file_path, "w") as f:
                pass
            count += 1
            exist_filenames.add(relative_path)

    print(f"pull video number:{count}")
    np.savez(npz_path, exist_filenames)


