from scripts_database_direct_export_import.mysql_helper import MysqlHelper
from tqdm import tqdm
from colorama import Fore

if __name__ == "__main__":
    user = {}
    user_code = "1838"
    name = "hua5ban"
    ks_dy_id = '1265239334'

    user['user_phone'] = ks_dy_id  # 抖音号 快手号
    user['user_nickname'] = ks_dy_id
    user['wechat_num'] = ks_dy_id
    user['nickname'] = name  # 使用昵称
    user['user_code'] = user_code
    user['avatar_url'] = '/static/images/2.png'
    user['user_headimg'] = '/static/images/2.png'
    user['is_reviewed'] = 1
    user['password'] = '71447ab1c47bf268e6db921a7be52fef'
    user['pwd_salt'] = 'iuLU'


    cztk_mysqlhelper = MysqlHelper(MysqlHelper.cztk_conn_params)

    select_sql = "select * from qqxcx_expert where user_code=%s"
    data = cztk_mysqlhelper.get_one(select_sql, (user_code))
    if data is None:
        cztk_mysqlhelper.insert('qqxcx_expert', user)
        msg = f"insert usercode:{user_code} name:{name}"
        print(Fore.BLACK + msg)
    else:
        msg = f"{user_code} insert failed! Because exists! user id is {data['user_id']}"
        print(Fore.RED + msg)

