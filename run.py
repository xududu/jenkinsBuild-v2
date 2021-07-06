import getopt
from configparser import ConfigParser, RawConfigParser
import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))
from service import BuildJenkins

'''buildJenkins的脚本，
启动命令：python run.py -g <group> -i <images:version>
可选参数：-g 可选参数：单个group，zs=正式，all=所有组
        -i 可选参数： 一个或多个镜像和版本号的字典，某个model=domain,subs,....，all=所有镜像
        -n 添加新项目：'aicard':'stable_aicard_website'
        -d 选择发布的数据中心，默认生产环境
'''


# 读取配置文件,实例化build_main_obj
def config_instantiation(var_sections='sc'):
    cp = RawConfigParser()
    # cp = ConfigParser()
    cp.read('./config/config.cfg')
    secs = cp.sections()
    assert var_sections in secs, 'dc_name ERROR!!!!!'

    sections = var_sections
    dc_name = cp.get(sections, 'dc_name')
    jenkins_addr = cp.get(sections, 'jenkins_addr')
    jenkins_username = cp.get(sections, 'jenkins_username')
    jenkins_password = cp.get(sections, 'jenkins_password')

    zs_group_list = cp.get(sections, 'ZS_Group_list').replace(' ', '').split(',')
    model_list = cp.get(sections, 'model_list').replace(' ', '').split(',')
    jk_view_name = cp.get(sections, 'jk_view_name')

    # 实例化
    build_obj = BuildJenkins.build_main_obj(jenkins_addr=jenkins_addr, jenkins_user=jenkins_username,
                                            jenkins_pwd=jenkins_password, zs_group_list=zs_group_list,
                                            model_list=model_list, jk_view_name=jk_view_name, dc_name=dc_name)
    return build_obj


def main(argv):
    """
    调用的入口函数
    支持的参数： -g 组名：ms_group
                -i 镜像名：{"sharehtesub":"1.1.0"}
                -n 添加新项目：'aicard':'stable_aicard_website'
                -d 选择发布的数据中心，默认生产环境
    :param argv:
    :return:
    """
    ms_group = ''
    img_version = ''
    new_jobs = ''
    dc_name = 'sc'

    try:
        opts, args = getopt.getopt(argv, "g:i:n:d:", ["ms_group", "img_version", "add_new_jobs", "dc_name"])
    except getopt.GetoptError:
        print('run.py -g <ms_group> -i <img_version> -n <add new jobs to jenkins> -d <dc_name>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('run.py -g <ms_group> -i <img_version> -n <add new jobs to jenkins> -d <dc_name>')
            sys.exit()
        elif opt in ("-g", "--ms_group"):
            ms_group = arg
        elif opt in ("-i", "--img_version"):
            img_version = arg
        elif opt in ("-n", "--add_new_jobs"):
            new_jobs = arg
        elif opt in ("-d", "--dc_name"):
            dc_name = arg

    # 实例化
    build_init = config_instantiation(var_sections=dc_name)
    # build项目
    if img_version:
        build_init.build_option(img_version=img_version, ms_group=ms_group)
    # 添加项目
    elif new_jobs:
        build_init.insert_new_jobs(new_jobs=new_jobs)


if __name__ == "__main__":
    main(sys.argv[1:])
