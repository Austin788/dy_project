# encoding=utf8
import pymysql

class MysqlHelper(object):
    # todo 数据库连接参数，可以定义多个，比如conn_params1，conn_params2，用于连接多个数据库，在类实例化时指定
    lyqt_conn_params = {
        'host': '43.142.234.129',
        'port': 3306,
        'user': 'liyuqutu',
        'passwd': 'Zzt20180301.',
        'db': 'liyuqutu',
        'charset': 'utf8',
        "cursorclass": pymysql.cursors.DictCursor
    }

    cztk_conn_params = {
        'host': '43.142.170.84',
        'port': 3306,
        'user': 'zyf4',
        'passwd': 'zyf18396185253',
        'db': 'dy_img_download',
        'charset': 'utf8',
    }

    cztk2_conn_params = {
        'host': '43.142.170.84',
        'port': 3306,
        'user': 'dy_image2',
        'passwd': 'zyf18396185253',
        'db': 'dy_image2',
        'charset': 'utf8',
    }

    # todo 类的构造函数，主要用于类的初始化
    def __init__(self, conn_params):
        self.__host = conn_params['host']
        self.__port = conn_params['port']
        self.__db = conn_params['db']
        self.__user = conn_params['user']
        self.__passwd = conn_params['passwd']
        self.__charset = conn_params['charset']

        self.__conn = pymysql.connect(host=self.__host,
                                      port=self.__port,
                                      database=self.__db,
                                      user=self.__user,
                                      password=self.__passwd,
                                      charset=self.__charset)

    def __del__(self):
        self.__conn.close()

    # todo 关闭游标和关闭连接
    def __close(self):
        self.__conn.close()

    # todo 取一条数据
    def get_one(self, sql, params):
        result = None
        try:
            __cursor = self.__conn.cursor(cursor=pymysql.cursors.DictCursor)
            __cursor.execute(sql, params)
            result = __cursor.fetchone()
            __cursor.close()
        except Exception as e:
            print(e)
        return result

    # todo 取所有数据
    def get_all(self, sql, params):
        lst = ()
        try:
            __cursor = self.__conn.cursor(cursor=pymysql.cursors.DictCursor)
            __cursor.execute(sql, params)
            lst = __cursor.fetchall()
            __cursor.close()
        except Exception as e:
            print(e)
        return lst

    # todo 增加数据
    def insert(self, sql, params):
        return self.__edit(sql, params)

    # todo 修改数据
    def update(self, sql, params):
        return self.__edit(sql, params)

    # todo 删除数据
    def delete(self, sql, params):
        return self.__edit(sql, params)

    # todo 写数据操作具体实现，增删改操作都是调用这个方法来实现，这是个私有方法，不允许类外部调用
    def __edit(self, sql, params):
        count = 0
        # try:
        if True:
            __cursor = self.__conn.cursor(cursor=pymysql.cursors.DictCursor)
            count = __cursor.execute(sql, params)
            self.__conn.commit()
            __cursor.close()
        # except Exception as e:
        #     print(e)
        return count

