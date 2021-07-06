"""自定义异常类"""


class GroupNameError(Exception):
    def __init__(self, group_name):
        self.group_name = group_name

    def __str__(self):
        return '%s GroupName ERROR!!!!' % self.group_name


class ImagesFormatError(Exception):
    def __init__(self, img_str):
        self.img_str = img_str

    def __str__(self):
        return '%s parameter -i FormatError!!!!!' % self.img_str


class ProjectDoesNotExist(Exception):
    def __init__(self, job_name):
        self.job_name = job_name

    def __str__(self):
        return '项目%s在数据库中不存在！！！！！添加新项目：-n "aicard":"stable_aicard_website"' % self.job_name
