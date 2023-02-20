from scripts_database_direct_export_import.mysql_helper import MysqlHelper

def is_integer(str):
    try:
        value = int(str)
        return True
    except:
        return False



def diff_table():
    # try:
    if True:
        # 查询数据
        cztk1_mysqlhelper = MysqlHelper(MysqlHelper.cztk_conn_params)
        cztk2_mysqlhelper = MysqlHelper(MysqlHelper.cztk2_conn_params)

        sql1 = "SELECT  TABLE_NAME FROM information_schema.tables WHERE TABLE_SCHEMA = 'dy_img_download' ORDER BY TABLE_NAME;"
        result1 = cztk1_mysqlhelper.get_all(sql1, ())
        table_names1 = []
        for row in result1:
            table_name = row['TABLE_NAME']
            table_names1.append(table_name)

        sql2 = "SELECT  TABLE_NAME FROM information_schema.tables WHERE TABLE_SCHEMA = 'dy_image2' ORDER BY TABLE_NAME;"
        result2 = cztk2_mysqlhelper.get_all(sql2, ())
        table_names2 = []
        for row in result2:
            table_name = row['TABLE_NAME']
            table_names2.append(table_name)

        # todo 打印执行结果
        for table_name in table_names2:
            if table_name not in table_names1:
                print(table_name, 'need create!')
            # cztk 中表的所有键值

            # cztk2中某个表的所有键值

            # user_code = row['user_code']
            # select_sql = "select * from qqxcx_expert where user_code=%s"
            # data = cztk_mysqlhelper.get_one(select_sql, (user_code))
            # print(user_code)
            # if data is None and is_integer(user_code):
            # # if True:
            #
            #     row.pop('user_id')
            #     new_row = {}
            #     param = []
            #     for key, value in row.items():
            #         if value is None:
            #             continue
            #         new_row[key] = value
            #         param.append(value)
            #
            #     table = 'qqxcx_expert'
            #     keys = ', '.join(new_row.keys())
            #     values = ', '.join(['%s'] * len(new_row))
            #     insert_sql = "INSERT INTO {table}({keys}) VALUES({values})".format(table=table, keys=keys, values=values)
            #     print(insert_sql)
            #     cztk_mysqlhelper.insert(insert_sql, param)
            #     print(f"insert usercode{new_row['user_code']}")

    # except:
    #     pass
    #
    del cztk1_mysqlhelper
    del cztk2_mysqlhelper


def diff_column():
    # try:
    if True:
        # 查询数据
        cztk1_mysqlhelper = MysqlHelper(MysqlHelper.lyqt_conn_params)
        cztk2_mysqlhelper = MysqlHelper(MysqlHelper.cztk2_conn_params)

        sql1 = "SELECT  TABLE_NAME FROM information_schema.tables WHERE TABLE_SCHEMA = 'liyuqutu' ORDER BY TABLE_NAME;"
        result1 = cztk1_mysqlhelper.get_all(sql1, ())
        table_names1 = []
        for row in result1:
            table_name = row['TABLE_NAME']
            table_names1.append(table_name)

        sql2 = "SELECT  TABLE_NAME FROM information_schema.tables WHERE TABLE_SCHEMA = 'dy_image2' ORDER BY TABLE_NAME;"
        result2 = cztk2_mysqlhelper.get_all(sql2, ())
        table_names2 = []
        for row in result2:
            table_name = row['TABLE_NAME']
            table_names2.append(table_name)

        # todo 打印执行结果
        for table_name in table_names2:
            # print(table_name)
            if table_name not in table_names1:
                print(f'table:{table_name}: need create!')
                continue

            pass
            sql_column = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.Columns WHERE table_name='{table_name}' ORDER BY COLUMN_NAME"

            column_result1 = cztk1_mysqlhelper.get_all(sql_column, ())
            column_names1 = []
            for row in column_result1:
                column_names1.append(row['COLUMN_NAME'])

            column_result2 = cztk2_mysqlhelper.get_all(sql_column, ())
            column_names2 = []
            for row in column_result2:
                column_names2.append(row['COLUMN_NAME'])

            for column_name in column_names2:
                if column_name not in column_names1:
                    print(f'table:{table_name} column: {column_name} need create!')


            # cztk 中表的所有键值

            # cztk2中某个表的所有键值

            # user_code = row['user_code']
            # select_sql = "select * from qqxcx_expert where user_code=%s"
            # data = cztk_mysqlhelper.get_one(select_sql, (user_code))
            # print(user_code)
            # if data is None and is_integer(user_code):
            # # if True:
            #
            #     row.pop('user_id')
            #     new_row = {}
            #     param = []
            #     for key, value in row.items():
            #         if value is None:
            #             continue
            #         new_row[key] = value
            #         param.append(value)
            #
            #     table = 'qqxcx_expert'
            #     keys = ', '.join(new_row.keys())
            #     values = ', '.join(['%s'] * len(new_row))
            #     insert_sql = "INSERT INTO {table}({keys}) VALUES({values})".format(table=table, keys=keys, values=values)
            #     print(insert_sql)
            #     cztk_mysqlhelper.insert(insert_sql, param)
            #     print(f"insert usercode{new_row['user_code']}")

    # except:
    #     pass
    #
    del cztk1_mysqlhelper
    del cztk2_mysqlhelper


if __name__ == "__main__":
    diff_column()