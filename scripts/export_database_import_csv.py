import cv2
import time

if __name__ == "__main__":

    url_dir = "/Users/meitu/Downloads/亲子头像.txt"
    save_dir = "/Users/meitu/Downloads/亲子头像_import.csv"
    with open(url_dir) as f:
        lines = f.readlines()


    with open(save_dir, "w", encoding='utf-8-sig') as f:
        for line in lines:
            url = line.strip("\n")
            if url.startswith("http://"):
                url = "https://" + url[7:]

            id=""
            cate_id = 0
            name = "sc2022111233372042"
            img = url
            show_index = "0"
            is_deleted = "0"
            created_at = int(time.time())
            updated_at = created_at
            is_recommend = 0
            author_id = 82
            download_count = 0
            type = 4
            source = 2
            status = 1
            video_url = url
            tag_ids = ""
            thumb_img = url
            weight = 0
            expression_video_url = ""
            expression_show_video = 0
            self_name = '亲子头像'

            text_line = f"{id},{cate_id},{name},{img},{show_index},{is_deleted},{created_at},{updated_at},{is_recommend},{author_id},{download_count},{type},{source},{status},{video_url},{tag_ids},{thumb_img},{weight},{expression_video_url},{expression_show_video},{self_name}\n"

            f.write(text_line)
            # break