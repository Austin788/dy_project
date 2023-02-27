import os
import numpy as np
import shutil
from colorama import Fore

class CopyWritingHelper():
    def __init__(self, copywriting_path, max_length=60, min_length=5):
        self.copywriting_path = copywriting_path
        self.copywritings = []
        self.max_length = max_length
        self.min_length =min_length
        self.load_copywriting()


    def load_copywriting(self):
        with open(self.copywriting_path) as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip('\n')
            if len(line) < self.min_length:
                continue
            line = CopyWritingHelper.remove_begin(line)
            if len(line) > self.max_length:
                continue
            self.copywritings.append(line)

    def save(self):
        with open(self.copywriting_path, "w") as f:
            for copywriting in self.copywritings:
                f.write(copywriting)
                f.write('\n')

    @staticmethod
    def remove_begin(text):
        flag = True
        skip = ['.', '、', ' ', '\t']
        count = 0
        while flag:
            if text[count].isdigit() or text[count] in skip:
                count += 1
            else:
                break

        return text[count:]

    def get_one(self):
        if len(self.copywritings) == 0:
            return None
        index = np.random.randint(0, len(self.copywritings) - 1)
        text = self.copywritings.pop(index)
        return text




if __name__ == "__main__":
    # dir = "/Users/meitu/同步空间/KS/1 黄19559702973-二次元[梓萱][1838]"
    # dir = "/Users/meitu/同步空间/KS/8 张17268202114-动漫"
    # copywriting_path = "/Users/meitu/Documents/midlife_crisis/文案/12.搞笑段子很皮的文案-830个.txt"

    # dir = "/Users/meitu/同步空间/KS/5 杨19559712873-男生2"
    # dir = "/Users/meitu/同步空间/KS/7 张13771417931-女生2"
    # dir = "/Users/meitu/同步空间/KS/10 张18396185253-男生/"
    # dir = "/Users/meitu/同步空间2/KS/3 黎15880650619-女生"
    # copywriting_path = "/Users/meitu/Documents/midlife_crisis/文案/11.励志哲理文案-850个.txt"

    # dir = "/Users/meitu/同步空间/KS/6 杨19559718173-壁纸"
    # copywriting_path = "/Users/meitu/Documents/midlife_crisis/文案/【古风第一期】300句抖音超美古风文案.txt"

    dir = "/Users/meitu/同步空间2/KS/4 杨13950832578-亲子"
    copywriting_path = '/Users/meitu/Documents/midlife_crisis/文案/晒娃句子出去玩句子.txt'


    copy_writings = CopyWritingHelper(copywriting_path)

    for dir_path, _, filenames in os.walk(dir):
        for filename in filenames:
            if not filename.endswith(".mp4"):
                continue

            mp4_path = os.path.join(dir_path, filename)

            text = copy_writings.get_one()
            if text is None:
                print(Fore.RED, "copy writing 用完了！")
                exit(0)

            # print(mp4_path, os.path.join(dir_path, text + ".mp4"))
            os.rename(mp4_path, os.path.join(dir_path, text + ".mp4"))

    copy_writings.save()