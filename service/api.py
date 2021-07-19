from configparser import RawConfigParser
from service import BuildJenkins


# 读取配置文件,实例化build_main_obj
def config_instantiation(var_sections='sc'):
    cp = RawConfigParser()
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


def build_api(img_version='', ms_group='', dc_name='sc', new_jobs='', **kwargs):
    # 实例化
    build_init = config_instantiation(var_sections=dc_name)
    # build项目
    if img_version:
        res = build_init.build_option(img_version=img_version, ms_group=ms_group, **kwargs)
        if res:
            return True
    # 添加项目
    elif new_jobs:
        build_init.insert_new_jobs(new_jobs=new_jobs)
    return build_init

