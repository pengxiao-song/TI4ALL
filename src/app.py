import threading
import time
from datetime import datetime

from PyQt5.QtCore import QDir, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QFileDialog,
                             QMainWindow, QMessageBox, QTableWidgetItem)
# from pyqt5_plugins.examplebutton import QtWidgets

from .gui.MainWidget import Ui_MainWindow
from .gui.SettingWidget import Ui_SettingWindow
from .utils import *

runtime_setting = {
    "model" : None,
    "cpu_num" : mul.cpu_count(),
    "use_multi_core" : False,
}


class ModelThread(QThread):
    sig_log = pyqtSignal(str)      # signal for updating log
    sig_run = pyqtSignal()         # signal for enabling run button
    sig_res = pyqtSignal(dict)     # signal for saving straight result
    sig_cmp = pyqtSignal(dict)     # signal for saving comparing result
    sig_progress = pyqtSignal(int)  # signal for progress
    sig_table = pyqtSignal(dict)    # signal for showing result in table

    def __init__(self, image_dir, info_file, model):
        """Initialize model running class

        Args:
            image_dir (str): dir
            info_file (str): .xlsx
        """
        super().__init__()
        self.image_dir = image_dir
        self.info_file = info_file
        self.model = model
        self.done = True
        self.total_image_num = -1
        self.cur_image_num = -1
    
    def run(self):
        self.done = False
        self.total_image_num = -1
        self.cur_image_num = -1
        self.sig_progress.emit(0)

        # 载入待检核酸报告图片
        images = load_images(dir_name=self.image_dir)
        self.sig_log.emit('完成图片载入，载入图片数量：' + str(len(images)))

        # 载入待检人员辅助信息
        try:
            self.dict_id_to_item, self.dict_mask_to_id = load_info(info_file=self.info_file)
            self.sig_log.emit('完成信息载入')
        except:
            self.sig_log.emit("请仔细检查: 信息文件(.xslx)是否符合要求")
            self.sig_run.emit()
            return 

        self.dict_image_to_item = {}    # 关联数据和监测信息
        cur_count = 0   # 当前识别数量
        total_n = len(images)   # 需识别总数
        
        # 单核检测
        s = time.time()
        if not runtime_setting["use_multi_core"]:
            for image in images:
                try:
                    info = get_info_from_image(self.model, image)
                    self.record_item(info)
                    cur_count += 1
                    self.sig_progress.emit(self.cal_progress(cur_count, total_n))

                except Exception as e:
                    print("出现错误:{}".format(e))
        # 多核检测       
        else:
            q = mul.Queue()
            processes = []

            for batch_images in self.batch_images_generator(images, len(images) / runtime_setting["cpu_num"]):
                p = mul.Process(
                    target=run_one_batch_multi_process,
                    args=(batch_images, q)
                )
                processes.append(p)
                p.start()
            
            for _ in range(len(images)):
                res_dict = q.get()
                cur_count += 1
                self.sig_progress.emit(self.cal_progress(cur_count, total_n))
                if 'error' in res_dict:
                    print("多进程出错:{}".format(res_dict['error']))
                else:
                    self.record_item(res_dict)
                    
        self.sig_run.emit()
        self.sig_res.emit(self.dict_image_to_item)
        self.sig_cmp.emit(self.dict_id_to_item)
        self.sig_log.emit("所有核酸图片识别完成，请选择保存类型及保存路径...")
        
        self.done = True
        
        total_cost_time = round(time.time() - s, 2)
        avg_cost_time = round(total_cost_time / len(images), 2)
        self.sig_log.emit("总耗时: {}s".format(total_cost_time))
        self.sig_log.emit("平均耗时: {}s".format(avg_cost_time))    

    # 多核状态下每个进程的待检图片生成器
    def batch_images_generator(self, images, batch_size):
        batch = []
        for image in images:
            batch.append(image)
            if len(batch) == batch_size:
                yield batch
                batch.clear()
        if len(batch) > 0:
            yield batch

    # 后处理单次识别结果
    def record_item(self, info):
        info_list = list(info.values())
        info_str = ' '.join(info_list)

        mask = info['身份证号码']
        if mask in self.dict_mask_to_id:
            id_ = self.dict_mask_to_id[mask]    # 身份证号为主键
            
            # 关联每条辅助信息对应的检测结果
            for k, v in info.items():
                if k not in self.dict_id_to_item[id_]:  # 增加辅助信息中没有的 “列” 
                    self.dict_id_to_item[id_][k] = v
            
            self.sig_table.emit(self.dict_id_to_item[id_])

        # 关联每张图片对应的检测结果
        self.dict_image_to_item[info["图片"]] = info
        self.sig_log.emit("{} - {}".format(info_str, os.path.basename(info["图片"])))
    
    # 计算进度条进度
    def cal_progress(self, cur_count, total):
        return min(100, cur_count * 100 // total)


class MainWidget(QMainWindow):
    def __init__(self, parent=None, config_file="config.yaml"):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 设置配置文件
        self.config_file = config_file

        # 设置程序默认配置
        self.params = self.get_default_param()
        self.ui.lineImgDir.setText(self.params["ImgDir"])
        self.ui.lineInfoFile.setText(self.params["InfoFile"])
        self.ui.checkUseMultiCore.setChecked(self.params["AllowMultiCore"])
        
        runtime_setting["use_multi_core"] = self.params["AllowMultiCore"]

        self.ui.btnSaveRes.setEnabled(False)
        self.ui.btnSaveCmp.setEnabled(False)
        self.ui.btnStop.setEnabled(False)

        # 保存检测信息
        self.dict_id_to_item = {}
        self.dict_image_to_item = {}
        
        # 异步载入模型线程
        self.td_model_loading = self.load_model_async()  

        self.ui.table.setAlternatingRowColors(True) # 使表格颜色交错显示
        # self.ui.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)   # 禁止编辑单元格
        self.ui.table.horizontalHeader().setStretchLastSection(True)    # 充满widget
        self.ui.table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 整行选中
        self.ui.table.verticalHeader().setVisible(True) #垂直表格头
        
        # 菜单栏 QAction 关联
        self.ui.menu1.triggered[QAction].connect(self.openSetFile)   # 关联“配置”
        self.ui.menu2.triggered[QAction].connect(self.OpenSetAbout)   # 关联“帮助”

    def openSetFile(self, m):
        if m.text() == "高级设置":
            self.setting_window = SettingWidget(self)
            self.setting_window.show()

    def OpenSetAbout(self, m):
        if m.text() == "使用帮助":
            about_content = self.params['About_content']
            QMessageBox.information(None, '使用帮助', about_content, QMessageBox.Ok)
        if m.text() == "联系我们":
            about_content = self.params['Connect_content']
            QMessageBox.information(None, '联系我们', about_content, QMessageBox.Ok)
        
    # 模型异步载入
    def load_model_async(self):
        load_td = threading.Thread(target=load_model_to_obj, args=(runtime_setting, ))
        load_td.start()
    
        return load_td
    
    # 主程序退出流程
    def closeEvent(self, e: QCloseEvent) -> None:
        if hasattr(self, "run_model_thread") and self.run_model_thread.done:
            message = "您确定退出吗？"
        else:
            message = "您的任务尚未完成，确定退出吗？"
            
        reply = QMessageBox.question(self, "提示", message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            save_config_to_yaml(self.params, self.config_file)
            e.accept()
        else:
            e.ignore()

    def get_default_param(self) -> dict:
        default_config = {
                "ImgDir" : "image",
                "InfoFile" : "info.xlsx",
                "AllowMultiCore" : False
            }
        try:
            if not os.path.exists(self.config_file):
                save_config_to_yaml(default_config, self.config_file)
                return default_config
            else:
                config = load_config_from_yaml(self.config_file)
                return config
        except:
            return default_config

    @pyqtSlot()
    def on_btnSetImgDir_clicked(self):
        curPath = QDir.currentPath()
        dlgTitle = "选择核酸图片目录"
        
        selectedDir = QFileDialog.getExistingDirectory(self, dlgTitle, curPath, QFileDialog.Option.ShowDirsOnly)
        self.params["ImgDir"] = selectedDir
        
        self.ui.lineImgDir.setText(selectedDir)
        
    @pyqtSlot()
    def on_btnSetInfoFile_clicked(self):
        curPath = QDir.currentPath()
        dlgTitle = "选择辅助信息文件"
        filt = "表格文件(*.xlsx)"
        
        filename, _ = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
        self.params["InfoFile"] = filename
        
        self.ui.lineInfoFile.setText(filename)
    
    @pyqtSlot()
    def on_btnSaveRes_clicked(self):
        curPath = QDir.currentPath()
        dlgTitle = "保存位置"
        filt = "表格文件(*.xlsx)"
        
        # 选择保存位置
        save_file, _ = QFileDialog.getSaveFileName(self, dlgTitle, curPath, filt)
        if save_file == '':
            return 

        # 保存原始检测结果
        try:    
            save_info_to_file(self.dict_image_to_item, save_file=save_file)   
        except:     
            QMessageBox.critical(self, "警告", "该文件被占用，请关闭该文件窗口")
            return
        
        # 更新日志区
        self.update_log('成功保存原始检测结果：' + save_file)
        
    @pyqtSlot()
    def on_btnSaveCmp_clicked(self):
        curPath = QDir.currentPath()
        dlgTitle = "保存位置"
        file = "表格文件(*.xlsx)"
        
        # 选择保存位置
        save_file, _ = QFileDialog.getSaveFileName(self, dlgTitle, curPath, file)
        if save_file == '':
            return
        
        # 保存综合检测文件
        try:
            save_info_to_file(self.dict_id_to_item, save_file=save_file)   
        except:     
            QMessageBox.critical(self, "警告", "该文件被占用，请关闭该文件窗口")
            return
        
        # 更新日志区
        self.update_log('成功保存综合检测结果：' + save_file)
    
    @pyqtSlot()
    def on_checkUseMultiCore_clicked(self):
        self.params["AllowMultiCore"] = not self.params["AllowMultiCore"]
        runtime_setting["use_multi_core"] = self.params["AllowMultiCore"]

    @pyqtSlot()
    def on_btnRun_clicked(self):
        '''
        点击“开始运行”按钮
        '''
        # 模型运行中 设置主界面按钮为 unenabled 状态
        self.ui.btnSaveRes.setEnabled(False)
        self.ui.btnSaveCmp.setEnabled(False) 
        
        # 清空表格信息
        self.ui.table.setRowCount(0)
        self.ui.table.clearContents()   
        
        # 读取图片文件夹和辅助信息文件
        image_dir = self.ui.lineImgDir.text()
        info_file = self.ui.lineInfoFile.text()
        
        if not os.path.exists(image_dir):
            QMessageBox.critical(self, "警告", "图片文件夹不存在，请重新选择！")
            return
        if not os.path.exists(info_file):
            QMessageBox.critical(self, "警告", "辅助信息文件不存在，请重新选择！")
            return
        
        self.update_log('图片目录选择完成：' + image_dir)
        self.update_log('信息文件选择完成：' + info_file)

        # 判断模型载入状态
        if self.td_model_loading.is_alive():
            self.update_log("正在等待模型载入...")
            self.td_model_loading.join()
        
        # 启动检测线程
        self.run_model_thread = ModelThread(image_dir, info_file, runtime_setting["model"])
        self.run_model_thread.sig_log.connect(self.update_log)  # 主界面日志更新
        self.run_model_thread.sig_run.connect(self.enable_run)  # 启动按钮
        self.run_model_thread.sig_res.connect(self.enable_res)  # 原始检测结果
        self.run_model_thread.sig_cmp.connect(self.enable_cmp)  # 综合检测信息
        self.run_model_thread.sig_progress.connect(self.update_progress)    # 进度条更新
        self.run_model_thread.sig_table.connect(self.write_table)   # 可视化表格数据
        self.run_model_thread.start()
        
        # 设置自身为 unenabled 状态
        self.ui.btnRun.setEnabled(False)
        self.ui.btnStop.setEnabled(True)

    @pyqtSlot()
    def on_btnStop_clicked(self):
        self.run_model_thread.terminate()
        self.ui.btnRun.setEnabled(True)
        
    @pyqtSlot(str)
    def update_log(self, message):
        '''
        添加 message 到主界面日志区
        '''
        now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        self.ui.pteLog.appendHtml("<p><b style=\"color:red\">[{}]</b> {}</p> ".format(now, message))

    @pyqtSlot()
    def enable_run(self):
        self.ui.btnRun.setEnabled(True)
        self.ui.table.setSortingEnabled(True)   # 使能表格排序功能
        
    @pyqtSlot(dict)
    def enable_res(self, dict_image_to_item):
        self.dict_image_to_item = dict_image_to_item
        self.ui.btnSaveRes.setEnabled(True)
    
    @pyqtSlot(dict)
    def enable_cmp(self, dict_id_to_item):
        self.dict_id_to_item = dict_id_to_item
        self.ui.btnSaveCmp.setEnabled(True)
        
    @pyqtSlot(int)
    def update_progress(self, value):
        self.ui.progressBar.setValue(value)

    @pyqtSlot(dict)
    def write_table(self, single_info):
        # 设置表格标题及相关格式
        self.ui.table.setColumnCount(len(list(single_info.keys())))
        self.ui.table.setHorizontalHeaderLabels(list(single_info.keys()))
        
        # 添加一行
        num = self.ui.table.rowCount()
        self.ui.table.setRowCount(num + 1)        
        
        # 填充内容
        for j in range(len(single_info.values())):
            item = QTableWidgetItem(str(list(single_info.values())[j]))
            self.ui.table.setItem(num, j, item)
            # item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)   
            
        self.ui.table.resizeColumnsToContents()


class SettingWidget(QMainWindow):
    def __init__(self, parent=MainWidget):
        super().__init__(parent)
        self.ui = Ui_SettingWindow()
        self.ui.setupUi(self)

    @pyqtSlot()
    def on_confirm_clicked(self):
        self.close()
        
    @pyqtSlot()
    def on_cancel_clicked(self):
        self.close()
