import os
from pathlib import Path

if __name__ == "__main__":
    import yaml

    data = yaml.load(open("../config.yml", mode='r', encoding='utf-8'))
    print(data)
    exit()


    base_dir = os.path.join(os.path.dirname(__file__), "../data/device")
    device_list = ['男生_张18396185253', '男生_张19559718173', '女生_张19559712873', '女生_张19559711797']

    for device in device_list:
        device_dir = Path(os.path.join(base_dir, device))
        (device_dir / "已发送").mkdir(parents=True, exist_ok=True)
        (device_dir / "待发送").mkdir(parents=True, exist_ok=True)
        (device_dir / "已上传").mkdir(parents=True, exist_ok=True)
        (device_dir / "待上传").mkdir(parents=True, exist_ok=True)


