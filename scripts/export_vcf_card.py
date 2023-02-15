import os
import pandas as pd
import io
import argparse
# import msoffcrypto
import pandas as pd

phone_list = [15959571093,
15659829007,
15959572907,
15260760100,
15860552421,
13665945636,
15759717081,
15860556623,
19559581236,
17302258183,
13665933529,
15959571790,
15859573507,
13055657567,
18659556430,
17268325603,
15160006789,
18659010106,
18750552915,
15106057883,
15105990255,
18160923222,
13626977328,
15260354868,
13625993535,
19905071232,
18965850170,
13559368788,
15280852573,
18250737274,
13950198808,
15959538421,
13559506582,
13489300106,
18650428713,
15859550079,
13314964285,
18659405888,
18250620272,
13850735137,
13315795402,
18016711819,
19859570119,
13960382981,
13599231996,
13459241294,
15259589865,
13645911500,
13860732629,
13850739160,
13015873335,
15759717837,
15396598368,
18396185253,
13055658707,
13665939386,
13625995660,
17729788892,
13959933431,
19959732909,
18659085081,
18759295593,
13559030123,
18059851080,
15960799325,
18859265350,
13599733183,
13505033839,
15805999972,
13004804736,
13067076006,
18159271738]

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

def list_to_vcf():
    out_path = "/Users/meitu/Documents/midlife_crisis/project/dy_project/data/素材库/"

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    out = open(f"{out_path}/lyqt.vcf", "w")
    for i in range(len(phone_list)):
        print(i)
        name = f"啊{i}{i}"
        phone = str(phone_list[i])
        out.write(f"BEGIN:VCARD\nVERSION:3.0\nN:{name[0]};{name[1:3]};;;\nFN:{name[1:3]} {name[0]}\nTEL;TYPE=CELL;TYPE=pref;TYPE=VOICE:{phone[0:3]} {phone[3:7]} {phone[7:11]}\nPRODID:-//Apple Inc.//iCloud Web Address Book 2220B25//EN\nREV:2022-08-22T08:45:49Z\nEND:VCARD\n")
    out.close()


if __name__ == "__main__":
    list_to_vcf()
    exit(0)

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





