import os
import pandas as pd
import io
import argparse
import msoffcrypto
import pandas as pd

"""
用于导出iphone cvf card
"""
def decode_excel(file_path, password):
    """
    用于xlsx文件解密
    :param file_path:
    :param password:
    :return:
    """
    try:
        save_path = file_path.replace(".xlsx", "_decode.xlsx")
        with open(file_path, "rb") as f:
            file = msoffcrypto.OfficeFile(f)
            file.load_key(password=password)  # Use password
            file.decrypt(open(save_path, 'wb'))

        return save_path

    except:
        return file_path
        print(f"decode {file_path} happen except!")

if __name__ == "__main__":
    save_path = "/Users/meitu/Downloads/0404上午MB.xlsx"
    excel_path = "/Users/meitu/Documents/midlife_crisis/廖荣寿/SD登记表/其它/1店11月订单_decode.xlsx"
    out_path = "/Users/meitu/Documents/midlife_crisis/project/phont_vcf/"

    if not os.path.exists(out_path):
        os.makedirs(out_path)
    df = pd.read_excel(excel_path, dtype=str)


    out=None
    for i in range(len(df)):
        if i % 300 == 0:
            if out is not None:
                out.close()
            out = open(f"{out_path}/phone1_{int(i/200)}.vcf", "w")
        name = df.iloc[i]['收货人姓名']
        phone = df.iloc[i]['联系手机']
        if len(phone) == 12:
            phone = phone[1:]
        out.write(f"BEGIN:VCARD\nVERSION:3.0\nN:{name[0]};{name[1:3]};;;\nFN:{name[1:3]} {name[0]}\nTEL;TYPE=CELL;TYPE=pref;TYPE=VOICE:{phone[0:3]} {phone[3:7]} {phone[7:11]}\nPRODID:-//Apple Inc.//iCloud Web Address Book 2220B25//EN\nREV:2022-08-22T08:45:49Z\nEND:VCARD\n")
    out.close()





