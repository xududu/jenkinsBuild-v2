import pymysql
import time

update_time = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))


class database_obj(object):
    # 默认值本地测试数据库
    def __init__(self, data_host='192.168.104.44', data_port=4400, data_user='root', data_pwd='123456',
                 data_db='jenkinsbuild'):
        self.data_host = data_host
        self.data_port = data_port
        self.data_user = data_user
        self.data_pwd = data_pwd
        self.data_db = data_db
        self.conn = ''
        self.cursor = ''

    def open_connect(self):
        self.conn = pymysql.connect(host=self.data_host, port=self.data_port, user=self.data_user,
                                    password=self.data_pwd, db=self.data_db, charset='utf8')
        self.cursor = self.conn.cursor()

    # 创建表
    def create_tables(self):
        self.open_connect()
        create_table_sql = """CREATE TABLE IF NOT EXISTS `jobandimage`(
                           `ImageName` VARCHAR(60) NOT NULL,
                           `JenkinsJob` VARCHAR(100) NOT NULL,
                           `ImageVersion` VARCHAR(30) DEFAULT '1.1.0',
                           `GroupName` VARCHAR(30) NOT NULL,
                           `LastUpDate` TIMESTAMP DEFAULT now() NOT NULL
                        )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

        ret = self.cursor.execute(create_table_sql)
        self.cursor.close()
        self.conn.close()
        return ret


a = database_obj()
a.create_tables()
