import pymysql


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

    # 创建镜像和Job的信息表
    def create_tables(self):
        self.open_connect()
        create_table_sql = """CREATE TABLE IF NOT EXISTS `JobMessage`(
                           `ImageName` VARCHAR(60) NOT NULL,
                           `JenkinsJob` VARCHAR(100) NOT NULL,
                           `ImageVersion` VARCHAR(30) DEFAULT '1.1.0',
                           `EnvAndGroupID` INT(60) NOT NULL,
                           `LastUpDate` TIMESTAMP DEFAULT now() NOT NULL,
                           FOREIGN KEY(EnvAndGroupID) REFERENCES EnvAndGroup(ID)
                        )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

        ret = self.cursor.execute(create_table_sql)
        self.cursor.close()
        self.conn.close()
        return ret

    # 创建环境和组信息表
    def create_table_env(self):
        self.open_connect()
        create_table_env_sql = """CREATE TABLE IF NOT EXISTS `EnvAndGroup`(
                           `ID` INT(60) NOT NULL AUTO_INCREMENT,
                           `Environment` VARCHAR(60) NOT NULL,
                           `GroupName` VARCHAR(60) NOT NULL,
                           PRIMARY KEY ( `ID` )
                        )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
        ret = self.cursor.execute(create_table_env_sql)
        self.cursor.close()
        self.conn.close()
        return ret

    # 插入一条数据，镜像，job，image_version，group_id
    def data_insert(self, img_job: dict, group_id, image_version='1.1.0'):
        self.open_connect()
        for img in img_job:
            image_name = img.strip("'")
            jenkins_job = img_job[img].strip("'")
            insert_sql = "INSERT INTO JobMessage(ImageName, \
                   JenkinsJob, ImageVersion, EnvAndGroupID) \
                   VALUES ('%s', '%s', %s)" % \
                         (image_name, jenkins_job, image_version, group_id)
            self.cursor.execute(insert_sql)

        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        return True

    # 查询column1 column2 ：要获取的结果，group_id：组id
    def image_job_select(self, select, group_id, basis='ImageName', column1=None, column2=None):
        self.open_connect()
        select_sql = "SELECT %s, %s \
                      FROM JobMessage \
                      where %s='%s' AND EnvAndGroupID='%s';" % (column1, column2, basis, select, group_id)

        self.cursor.execute(select_sql)
        rows = self.cursor.fetchall()

        self.cursor.close()
        self.conn.close()
        return rows

    # 更新数据库镜像的版本号
    def image_version_update(self, image, version, group_id):
        self.open_connect()
        update_sql = "UPDATE JobMessage set ImageVersion='%s', LastUpDate=CURRENT_TIMESTAMP  \
                     WHERE ImageName='%s' AND EnvAndGroupID='%s';" \
                     % (version, image, group_id)
        self.cursor.execute(update_sql)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    # EnvAndGroup表查询操作
    def env_and_group_select(self):
        """
        ID
        Environment
        GroupName
        """
        self.open_connect()
        select_sql = "SELECT ID FROM EnvAndGroup  where Environment='sc' AND GroupName='center';"

        self.cursor.execute(select_sql)
        return_value = self.cursor.fetchall()
        #TODO
        print(return_value,'xxx')

        self.cursor.close()
        self.conn.close()
        return return_value

obj = database_obj()
# ret = obj.image_job_select(select='aicard', group_id=1, basis='ImageName', column1='JenkinsJob', column2='ImageName')
# ret2 = obj.env_and_group_select(select='ID', where1='Environment', where2='GroupName', value1='sc', value2='center')
ret2 = obj.env_and_group_select()
# print(ret)
print(ret2[0][0])