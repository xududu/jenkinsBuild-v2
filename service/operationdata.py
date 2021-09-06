from configparser import ConfigParser
from modules import DataModules
from modules import ErrorModules

# 读配置文件
cp = ConfigParser()
cp.read('./config/config.cfg')
data_host = cp.get('DatabaseAddr', 'data_host')
data_port = cp.get('DatabaseAddr', 'data_port')
data_user = cp.get('DatabaseAddr', 'data_user')
data_pwd = cp.get('DatabaseAddr', 'data_pwd')
data_db = cp.get('DatabaseAddr', 'data_db')


"""数据操作"""
# 实例化
data_obj = DataModules.database_obj(data_host=data_host, data_port=int(data_port), data_user=data_user,
                                    data_pwd=data_pwd, data_db=data_db)


# 创建表
def create_table_function():
    data_obj.create_tables()
    return True


# 根据镜像查询job名
def data_select_function(img):
    """根据镜像查询镜像和job对应的关系，返回job名"""
    select_res = data_obj.image_job_select(column1='ImageName', column2='JenkinsJob', select=img)
    if select_res:
        return dict(select_res)[img]
    else:
        print(img, '在库中不存在')
        return 402


# 更新镜像版本号
def update_img_ver_function(img, ver):
    data_obj.image_version_update(image=img, version=ver)
    return True


# 调用插入sql
def new_job_insert_function(new_job: dict):
    """向表中插入镜像名和job名"""
    data_obj.data_insert(new_job)
    return True


# 根据镜像查询job名
def select_job_function(job_name):
    """根据镜像查询镜像和job对应的关系，返回job名字和版本号的元组"""
    select_res = data_obj.image_job_select(column1='JenkinsJob', column2='ImageVersion', select=job_name,
                                           basis='JenkinsJob')
    try:
        res = select_res[0]
    except IndexError as IE:

        return 402
    else:
        return res

