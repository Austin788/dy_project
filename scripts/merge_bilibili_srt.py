import os

if __name__ == "__main__":
    txt_path = "BV17r4y1u77B - P1：DALL·E 2（内含扩散模型介绍）【论文精读】 - zh-CN.srt"
    out_path = "dalle2.txt"

    with open(txt_path) as f:
        lines = f.readlines()

    with open(out_path, "w") as f:
        for i, line in enumerate(lines):
            line = line.strip('\n')
            if line.find("-->") != -1:
                continue
            try:
                int(line)
            except:
                f.write(line)
