from scripts_database_direct_export_import.mysql_helper import MysqlHelper
from tqdm import tqdm
from colorama import Fore

def is_integer(str):
    try:
        value = int(str)
        return True
    except:
        return False

def sync_expert():
    # 查询数据
    llqt_mysqlhelper = MysqlHelper(MysqlHelper.new_lyqt_conn_params)
    wxtk_mysqlhelper = MysqlHelper(MysqlHelper.wxtk_conn_params)

    sql = "select * from qqxcx_expert"
    result = llqt_mysqlhelper.get_all(sql, ())

    select_created_at_sql = "select created_at from qqxcx_wallpaper where 1 order by created_at desc limit 1;"
    data = wxtk_mysqlhelper.get_one(select_created_at_sql, ())
    if data is None:
        last_created_at = 0
    else:
        last_created_at = int(data['created_at'])

    # todo 打印执行结果
    for row in tqdm(result):
        if row['created_at'] > last_created_at:
            user_code = row['user_code']
            user_id = row['user_id']
            select_sql = "select * from qqxcx_expert where user_code=%s or user_id=%s"
            data = wxtk_mysqlhelper.get_one(select_sql, (user_code, user_id))
            if data is None:
                if is_integer(user_code):
                    wxtk_mysqlhelper.insert('qqxcx_expert', row)
                    msg = f"insert usercode{row['user_code']}"
                    print(Fore.BLACK + msg)
            else:
                msg = f"user_id:{user_id} user_code:{user_code} insert failed! Because exists!"
                print(Fore.RED + msg)

    del llqt_mysqlhelper
    del wxtk_mysqlhelper


def sync_wallpaper():
    # 查询数据
    llqt_mysqlhelper = MysqlHelper(MysqlHelper.new_lyqt_conn_params)
    wxtk_mysqlhelper = MysqlHelper(MysqlHelper.wxtk_conn_params)

    select_created_at_sql = "select created_at from qqxcx_wallpaper where 1 order by created_at desc limit 1;"
    data = wxtk_mysqlhelper.get_one(select_created_at_sql, ())
    if data is None:
        last_created_at = 0
    else:
        last_created_at = int(data['created_at'])

    sql = "select * from qqxcx_wallpaper where created_at > '%s'"
    result = llqt_mysqlhelper.get_all(sql, (last_created_at))

    # todo 打印执行结果
    for row in tqdm(result):
        if row['created_at'] > last_created_at:
            row.pop('id')
            wxtk_mysqlhelper.insert('qqxcx_wallpaper', row)


if __name__ == "__main__":
    sync_expert()
    sync_wallpaper()