import jenkins
from service import operationdata
from modules import ErrorModules


class build_main_obj(object):
    def __init__(self, jenkins_addr, jenkins_user, jenkins_pwd, zs_group_list, model_list, jk_view_name='stable',
                 dc_name='sc'):
        self.jenkins_addr = jenkins_addr
        self.jenkins_user = jenkins_user
        self.jenkins_pwd = jenkins_pwd

        self.server = jenkins.Jenkins(self.jenkins_addr, username=self.jenkins_user, password=self.jenkins_pwd)
        self.ZS_Group_list = zs_group_list
        self.model_list = model_list
        self.jk_view_name = jk_view_name
        self.dc_name = dc_name
        self.group_list = []

    def _build_job_obj_auxiliary_function(self, build_name, **kwargs):
        """_build_job_obj的辅助函数，为了减少重复代码
        :param kwargs： 参数化构建的参数"""
        ret_str = ''
        for group in self.group_list:
            # 根据job名字到数据库里查版本号,用数据库里的版本号来批量build
            job_name_tup = operationdata.select_job_function(job_name=build_name, group=group)
            if job_name_tup:
                job_name = job_name_tup[0]
                image_version = job_name_tup[1]
                print('执行的项目是:<%s>，执行的组是:<%s>，执行的数据中心是:<%s>' % (job_name, group, self.dc_name))
                ret_str = ret_str + '执行的项目是:<%s>，执行的组是:<%s>，执行的数据中心是:<%s>' % (job_name, group, self.dc_name) + '\n'
                parameter_dict = {"image_tag": image_version, 'ms_group': group}

                parameter_dict.update(kwargs)

                self.server.build_job(job_name, parameters=parameter_dict)
        return ret_str

    def _build_job_obj(self, b_group, b_img=None, img_v=None, all_img_obj=None, **kwargs):
        """
        build Jenkins项目调用的函数,build_option调用此函数
        :param b_group: 传入需要build到的组名
        :param b_img: 传入需要build的镜像名或者一个列表，也可以传入model名字build一部分
        :param img_v: 传入镜像版本号
        :param all_img_obj: 如果需要build所有镜像，应该把包含所有jobs的对象列表传给此参数
        :param kwargs： 参数化构建的参数
        :return:
        """
        if b_group == 'zs':
            if self.dc_name == 'sc':
                try:
                    self.ZS_Group_list.remove('center')
                except ValueError:
                    print('next job!')
            self.group_list = self.ZS_Group_list
        elif b_group == 'all':
            self.group_list = self.ZS_Group_list

        elif b_group in self.ZS_Group_list:
            self.group_list = b_group.split()
        else:
            raise ErrorModules.GroupNameError(b_group)
        # 如果要build所有镜像会执行此部分
        if all_img_obj:
            for job in all_img_obj:
                # 判断job的名字是否包含要启动的任务
                if job['color'] == 'disabled':
                    continue
                if b_img == 'all':
                    self._build_job_obj_auxiliary_function(build_name=job['name'])
                # 如果只build某些model
                elif '_' + b_img in job['name']:
                    self._build_job_obj_auxiliary_function(build_name=job['name'])
            return True
        else:
            # 只build指定镜像时
            for group in self.group_list:
                job_name = operationdata.data_select_function(img=b_img, group=group)
                print('执行的项目是:<%s>，执行的组是:<%s>，执行的数据中心是:<%s>' % (job_name, group, self.dc_name))
                parameter_dict = {"image_tag": img_v, 'ms_group': group}

                parameter_dict.update(kwargs)
                self.server.build_job(job_name, parameters=parameter_dict)
                # 数据库版本号更新
                if group != 'center':
                    operationdata.update_img_ver_function(img=b_img, ver=img_v, group=group)
                    print('更新镜像%s的版本号更新为：%s' % (b_img, img_v))
            return True

    @staticmethod
    def _str_dict_handle(img_str: str):
        """
        字符串处理成字典
        :param img_str: {classnumberserver:1.1.1,oauthwebapiserver:1.1.2}
        :return:  {'classnumberserver': '1.1.1', 'oauthwebapiserver': '1.1.2'}--- type=dict
        """
        try:
            res_dic = {}
            han_str = img_str.strip('{}')
            han_str = han_str.replace('"', '')
            han_str = han_str.replace("'", '')
            han_list = han_str.split(',')
            for imgAdnVersion in han_list:
                img_name = imgAdnVersion.split(':')[0]
                img_version = imgAdnVersion.split(':')[1]
                res_dic[img_name] = img_version
        except IndexError as e:
            raise ErrorModules.ImagesFormatError(img_str)
        else:
            return res_dic

    def build_option(self, img_version, ms_group, **kwargs):
        """
        Build Jenkins 项目前针对选项着不同的判断
        :param img_version: build所有的时候此值是model：subs，domain。。。，build指定镜像时此值是{镜像：版本号}
        :param ms_group:  发布到的组
        :param k8s_group: 本地k8s的组名
        :return:
        """
        # 如果想build所有镜像或某部分镜像执行此部分
        if img_version in self.model_list:
            all_jobs_name_obj = self.server.get_jobs(view_name=self.jk_view_name)
            self._build_job_obj(b_group=ms_group, b_img=img_version, all_img_obj=all_jobs_name_obj, **kwargs)
        else:
            # 如果只build某些指定的镜像执行此部分
            img_version_dict = self._str_dict_handle(img_version)
            for img in img_version_dict:
                version = img_version_dict[img]
                self._build_job_obj(b_group=ms_group, b_img=img, img_v=version, **kwargs)
        return True

    def insert_new_jobs(self, new_jobs, group):
        """
        向数据库内添加新项目的时候，会调用此函数
        :param new_jobs: 新项目的字典 {'aicard':'stable_aicard_website'}
        :param group: 项目添加到哪个组
        :return:
        """
        img_jobs_dict = self._str_dict_handle(new_jobs)
        # 在同时传入多个新项目的时候，把一个大字典拆分成单个字典，然后调用new_job_insert_function函数
        for img in img_jobs_dict:
            job_name = img_jobs_dict[img]
            new_str = img + ':' + job_name
            single_img_jobs_dict = self._str_dict_handle(new_str)
            operationdata.new_job_insert_function(new_job=single_img_jobs_dict, group=group)
            print('%s 已添加！' % single_img_jobs_dict)
        return True
