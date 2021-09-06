# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\todolist.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
import threading
from service.api import build_api
import ctypes

DC_NAME_DICT = {"华为云": "sc", "本地": "bd", "云阳": "yy", "龙口": "lk"}
STATUS_CODE = {101: 'success!', 201: '', 301: '%s 格式化错误!', 401: '%s 组名错误!',
               402: '输入的内容中：%s至少有一个在数据库中不存在！检查镜像名或者根据后台输出添加新项目："aicard":"stable_aicard_website"'}

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")


class Ui_PublishTools(object):
    def setupUi(self, PublishTools):
        PublishTools.setWindowIcon(QtGui.QIcon('./web.png'))
        PublishTools.setObjectName("PublishTools")
        PublishTools.resize(947, 579)
        self.save_but = QtWidgets.QPushButton(PublishTools)
        self.save_but.setGeometry(QtCore.QRect(10, 520, 271, 51))
        self.save_but.setObjectName("save_but")
        self.close_but = QtWidgets.QPushButton(PublishTools)
        self.close_but.setGeometry(QtCore.QRect(600, 520, 331, 51))
        self.close_but.setObjectName("close_but")
        self.text_input = QtWidgets.QTextBrowser(PublishTools)
        self.text_input.setGeometry(QtCore.QRect(0, 0, 951, 131))
        self.text_input.setObjectName("text_input")
        # 编辑日期时间
        self.editor_time = QtWidgets.QDateTimeEdit(PublishTools)
        self.editor_time.setGeometry(QtCore.QRect(670, 200, 261, 41))
        self.editor_time.setObjectName("editor_time")
        self.editor_time.setDateTime(QtCore.QDateTime.currentDateTime())  # 设置为当前时间
        # self.editor_time.setMinimumDateTime(QtCore.QDateTime.currentDateTime())  # 最小时间为当前时间
        self.editor_time.setCalendarPopup(True)
        # 镜像输入框
        self.images_input = QtWidgets.QPlainTextEdit(PublishTools)
        self.images_input.setGeometry(QtCore.QRect(0, 360, 951, 121))
        self.images_input.setPlainText("")
        self.images_input.setObjectName("images_input")
        self.group_name = QtWidgets.QComboBox(PublishTools)
        self.group_name.setGeometry(QtCore.QRect(340, 200, 261, 41))
        self.group_name.setObjectName("group_name")
        self.label = QtWidgets.QLabel(PublishTools)
        self.label.setGeometry(QtCore.QRect(410, 340, 101, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(PublishTools)
        self.label_2.setGeometry(QtCore.QRect(430, 170, 101, 16))
        self.label_2.setObjectName("label_2")
        self.dc_name = QtWidgets.QComboBox(PublishTools)
        self.dc_name.setGeometry(QtCore.QRect(0, 200, 261, 41))
        self.dc_name.setObjectName("dc_name")
        self.dc_name.addItem("")
        self.dc_name.setItemText(0, "")
        self.dc_name.addItem("")
        self.dc_name.addItem("")
        self.dc_name.addItem("")
        self.dc_name.addItem("")
        self.label_3 = QtWidgets.QLabel(PublishTools)
        self.label_3.setGeometry(QtCore.QRect(60, 170, 121, 16))
        self.label_3.setObjectName("label_3")
        # 定时选择框
        self.timingBox = QtWidgets.QCheckBox(PublishTools)
        self.timingBox.setGeometry(QtCore.QRect(670, 260, 91, 19))
        self.timingBox.setObjectName("timingBox")
        # 添加项目选择框
        self.addJobsBox = QtWidgets.QCheckBox(PublishTools)
        self.addJobsBox.setGeometry(QtCore.QRect(780, 260, 91, 19))
        self.addJobsBox.setObjectName("addJobsBox")
        # k8s_group框
        self.k8sOptionsBox = QtWidgets.QCheckBox(PublishTools)
        self.k8sOptionsBox.setGeometry(QtCore.QRect(670, 300, 16, 21))
        self.k8sOptionsBox.setText("")
        self.k8sOptionsBox.setObjectName("k8sOptionsBox")
        self.k8sGroupEdit = QtWidgets.QLineEdit(PublishTools)
        self.k8sGroupEdit.setGeometry(QtCore.QRect(690, 300, 81, 21))
        self.k8sGroupEdit.setAutoFillBackground(False)
        self.k8sGroupEdit.setDragEnabled(True)
        self.k8sGroupEdit.setClearButtonEnabled(False)
        self.k8sGroupEdit.setObjectName("k8sGroupEdit")
        # 定时选择框触发事件
        # self.timingBox.stateChanged.connect(self.timing_box_event)
        # 点击事件
        self.save_but.clicked.connect(self.save_clicked)
        self.close_but.clicked.connect(self.close)
        # dc_name选择框触发
        self.dc_name.activated.connect(self.box_data)

        self.retranslateUi(PublishTools)
        QtCore.QMetaObject.connectSlotsByName(PublishTools)

    def retranslateUi(self, PublishTools):
        _translate = QtCore.QCoreApplication.translate
        PublishTools.setWindowTitle(_translate("PublishTools", "PublishTools"))
        self.save_but.setText(_translate("PublishTools", "确认发布"))
        self.close_but.setText(_translate("PublishTools", "退出"))
        self.text_input.setHtml(_translate("PublishTools",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                           "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#00ff00;\">发布信息</span></p></body></html>"))

        self.label.setText(_translate("PublishTools", "发布的镜像"))
        self.label_2.setText(_translate("PublishTools", "发布的组"))
        self.dc_name.setItemText(0, _translate("PublishTools", ""))
        self.dc_name.setItemText(1, _translate("PublishTools", "华为云"))
        self.dc_name.setItemText(2, _translate("PublishTools", "本地"))
        self.dc_name.setItemText(3, _translate("PublishTools", "云阳"))
        self.dc_name.setItemText(4, _translate("PublishTools", "龙口"))
        self.label_3.setText(_translate("PublishTools", "发布的数据中心"))
        self.timingBox.setText(_translate("PublishTools", "定时发布"))
        self.addJobsBox.setText(_translate("PublishTools", "添加项目"))
        self.k8sGroupEdit.setText(_translate("PublishTools", "k8s_group"))

    # def timing_box_event(self):
    #     timing_box_status = self.timingBox.isChecked()
    #     if timing_box_status:
    #         print(self.editor_time.dateTime().toString("yyyy-MM-dd HH:mm:ss"))
    #         print(self.editor_time.dateTime().toTime_t())
    #         print(QtCore.QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss"))

    def box_data(self):
        # dc_name选择框触发函数
        rel_dc_name = self.dc_name.currentText()
        if rel_dc_name:
            dc_name = DC_NAME_DICT[rel_dc_name]
            # 获取组列表
            config_obj = build_api(dc_name=dc_name)
            group_list = config_obj.ZS_Group_list
            if rel_dc_name == "华为云":
                group_list.append("正式")
            self.group_name.clear()
            self.group_name.addItems(group_list)
        else:
            self.group_name.clear()

    def save_clicked(self, event):
        # 获取输入的组名
        group = self.group_name.currentText()
        if group != 'center':
            if group != '':
                # 点击发布按钮后的确认框判断
                reply = QMessageBox.question(self,
                                             "Are you sure?",
                                             "确认发布?",
                                             QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.No)
                if reply == QMessageBox.Yes:
                    print(event)
                else:
                    return False
        # 检查是否是添加新项目
        add_job_status = self.addJobsBox.isChecked()
        # 如果是添加新项目执行这个部分
        if add_job_status:
            new_job_str = self.images_input.toPlainText().strip()
            res = build_api(new_jobs=new_job_str)
            if res == 101:
                self.text_input.setText("%s,添加成功！" % new_job_str)
            else:
                res_text = STATUS_CODE[res]
                self.text_input.setText(res_text % new_job_str)
            # 重置按钮状态
            self.addJobsBox.setChecked(False)
            self.timingBox.setChecked(False)
            return True
        elif self.dc_name.currentText():
            # 镜像和版本号
            img_and_version = self.images_input.toPlainText().strip()
            img_and_version = img_and_version.lower().replace(' ', '')

            if group == '正式':
                group = 'zs'
            dc = self.dc_name.currentText()
            dc_name = DC_NAME_DICT[dc]

            # 检查是否定时发布
            timing_box_status = self.timingBox.isChecked()
            if timing_box_status:
                # 定时发布部分
                timing_timestamp = self.editor_time.dateTime().toTime_t()
                now_timestamp = QtCore.QDateTime.currentDateTime().toTime_t()
                if timing_timestamp > now_timestamp:
                    string_time = self.editor_time.dateTime().toString("yyyy-MM-dd HH:mm:ss")
                    time_difference = timing_timestamp - now_timestamp

                    print('%s seconds from the scheduled task' % time_difference)
                    timing = threading.Timer(time_difference, build_api, (img_and_version, group, dc_name))
                    self.text_input.setText("将在%s 发布%s 镜像，到%s 数据中心的 %s 组！" % (string_time, img_and_version,
                                                                              dc_name, group))
                    timing.start()
                    # 取消选择框的选则状态，每次定时发布都需要重新选择定时发布
                    self.timingBox.setChecked(False)
                    # self.timing.cancel()
                    return True
                else:
                    self.text_input.setText("输入的时间小于当前时间！！！")
                    return False
            else:
                # 非定时发布部分
                # 检查是否勾选了k8s_group
                k8s_box_status = self.k8sOptionsBox.isChecked()
                if k8s_box_status:
                    k8s_group_str = self.k8sGroupEdit.text().strip()
                    res = build_api(img_version=img_and_version, ms_group=group, dc_name=dc_name,
                                    k8s_group=k8s_group_str)
                else:
                    res = build_api(img_version=img_and_version, ms_group=group, dc_name=dc_name)
                if res == 101:
                    self.text_input.setText("镜像是：" + img_and_version + "\n" + "组名是：" + group + "\n" +
                                            "dcName是：" + dc)
                    return True
                else:
                    res_text = STATUS_CODE[res]
                    self.text_input.setText(res_text % img_and_version)
                    return False
        else:
            self.text_input.setText("没有选择发布的数据中心！！！")
            return False
