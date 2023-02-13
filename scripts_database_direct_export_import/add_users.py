from scripts_database_direct_export_import.mysql_helper import MysqlHelper
from tqdm import tqdm

def is_integer(str):
    try:
        value = int(str)
        return True
    except:
        return False

def sync_expert():
    # try:
    if True:
        # 查询数据
        llqt_mysqlhelper = MysqlHelper(MysqlHelper.lyqt_conn_params)
        cztk_mysqlhelper = MysqlHelper(MysqlHelper.cztk_conn_params)

        sql = "select * from qqxcx_expert"
        result = llqt_mysqlhelper.get_all(sql, ())

        # todo 打印执行结果
        for row in tqdm(result):
            user_code = row['user_code']
            user_id = row['user_id']
            select_sql = "select * from qqxcx_expert where user_code=%s or user_id=%s"
            data = cztk_mysqlhelper.get_one(select_sql, (user_code, user_id))
            print(user_code)
            if data is None and is_integer(user_code):
            # if True:
                new_row = {}
                param = []
                for key, value in row.items():
                    if value is None:
                        continue
                    new_row[key] = value
                    param.append(value)

                table = 'qqxcx_expert'
                keys = ', '.join(new_row.keys())
                values = ', '.join(['%s'] * len(new_row))
                insert_sql = "INSERT INTO {table}({keys}) VALUES({values})".format(table=table, keys=keys, values=values)
                print(insert_sql)
                cztk_mysqlhelper.insert(insert_sql, param)
                print(f"insert usercode{new_row['user_code']}")

    # except:
    #     pass
    #
    del llqt_mysqlhelper
    del cztk_mysqlhelper


def sync_wallpaper():
    # 查询数据
    llqt_mysqlhelper = MysqlHelper(MysqlHelper.lyqt_conn_params)
    cztk_mysqlhelper = MysqlHelper(MysqlHelper.cztk_conn_params)

    sql = "select * from qqxcx_wallpaper"
    result = llqt_mysqlhelper.get_all(sql, ())

    select_sql = "select created_at from qqxcx_wallpaper where 1 order by created_at desc limit 1;"
    data = cztk_mysqlhelper.get_one(select_sql, ())
    if data is None:
        last_created_at = 0
    else:
        last_created_at = int(data[0]['created_at'])

    # todo 打印执行结果
    for row in tqdm(result):
        if row['created_at'] > last_created_at :
            id = row.pop('id')
            new_row = {}
            param = []
            for key, value in row.items():
                if value is None:
                    continue
                new_row[key] = value
                param.append(value)

            table = 'qqxcx_wallpaper'
            keys = ', '.join(new_row.keys())
            values = ', '.join(['%s'] * len(new_row))
            insert_sql = "INSERT INTO {table}({keys}) VALUES({values})".format(table=table, keys=keys, values=values)
            cztk_mysqlhelper.insert(insert_sql, param)
        else:
            print(f"{id} is exists!")


if __name__ == "__main__":
    sync_wallpaper()