import pymysql


class database_obj(object):
    # 默认值本地测试数据库
    def __init__(self, data_host='192.168.7.201', data_port=3306, data_user='root', data_pwd='root',
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

    # 插入一条数据，镜像，job，GroupName
    def data_insert(self, img_job: dict, group):
        self.open_connect()
        for img in img_job:
            image_name = img.strip("'")
            jenkins_job = img_job[img].strip("'")
            insert_sql = "INSERT INTO jobandimage(ImageName, \
                   JenkinsJob, GroupName) \
                   VALUES ('%s', '%s', %s)" % \
                         (image_name, jenkins_job, group)
            self.cursor.execute(insert_sql)

        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        return 0

    # 查询
    def image_job_select(self, select, group, basis='ImageName', column1=None, column2=None):
        self.open_connect()
        select_sql = "SELECT %s, %s \
                      FROM jobandimage \
                      where %s='%s' AND GroupName='%s';" % (column1, column2, basis, select, group)

        self.cursor.execute(select_sql)
        rows = self.cursor.fetchall()

        self.cursor.close()
        self.conn.close()
        return rows

    # 更新数据库镜像的版本号
    def image_version_update(self, image, version, group):
        self.open_connect()
        update_sql = "UPDATE jobandimage set ImageVersion='%s', LastUpDate=CURRENT_TIMESTAMP WHERE ImageName='%s' AND GroupName='%s';" \
                     % (version, image, group)
        self.cursor.execute(update_sql)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
