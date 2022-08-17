import os
from pathlib import Path

if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(__file__), "../dy_data")
    device_list = ['张1955971873', '张19559712873', '张19559711797']

    for device in device_list:
        device_dir = Path(os.path.join(base_dir, device))
        (device_dir / "已发送").mkdir(parents=True, exist_ok=True)
        (device_dir / "待发送").mkdir(parents=True, exist_ok=True)
        (device_dir / "已上传").mkdir(parents=True, exist_ok=True)
        (device_dir / "待上传").mkdir(parents=True, exist_ok=True)


