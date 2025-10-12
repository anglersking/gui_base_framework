# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from datetime import datetime
import math
import random
import time
import trace
import traceback
from gui.uis.windows.main_window.functions_main_window import *
import sys
import os
import pandas as pd

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
from gui.uis.windows.main_window import *

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *
from utils.count_device_utils import CountDevice
import serial.tools.list_ports
from openpyxl.styles import Font, Alignment  # 添加Alignment导入
from openpyxl import load_workbook


# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'

# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)

        self.run_start=SetupMainWindow.get_start_button(self)
        self.run_start.clicked.connect(self.start_race)

        self.import_path = SetupMainWindow.get_import_path(self)
        self.select_name=SetupMainWindow.get_select_name(self)
        self.table_info_widget=SetupMainWindow.get_table_info_widget(self)

        self.select_import_file = SetupMainWindow.get_select_import_file(self)
        self.select_import_file.clicked.connect(self.select_path)

        self.current_count_lable = SetupMainWindow.get_current_count_lable(self)
        self.select_timer_count = SetupMainWindow.get_select_timer_count(self)
        self.select_timer_count.currentIndexChanged.connect(self.update_current_count)

        self.select_timer_combox = SetupMainWindow.get_select_timer_combox(self)
        self.real_timer_count = SetupMainWindow.get_real_timer_count(self)
        self.unqualified_info = SetupMainWindow.get_unqualified_info(self)
        self.race_region = SetupMainWindow.get_slect_race_region(self)

        
        self.line_search_edit = SetupMainWindow.get_line_search_edit(self)
        self.search_btn = SetupMainWindow.get_search_btn(self)
        self.search_btn.clicked.connect(self.search_in_table)
        self.export_file_btn = SetupMainWindow.get_export_file_btn(self)
        self.export_file_btn.clicked.connect(self.export_in_table)
    


        self.timer_info_lable = SetupMainWindow.get_timer_info_lable(self)
        self.timer_info_lable = SetupMainWindow.get_timer_info_lable(self)
        
        
        # 初始化设备引用
        self.race_device = None
        self.race_timer = None
        self.race_timer_elapsed = QElapsedTimer()
        self.race_started = False
        
        # 列出所有可用串口
        ports = serial.tools.list_ports.comports()  # ✅ 必须先定义
        port_list = [port.device for port in ports]  # 提取串口号列表

        self.race_region.clear()
        self.race_region.addItems(port_list)

        print("======", port_list)

        for port in ports:
            print(f"设备: {port.device}, 描述: {port.description}")
            # self.slect_race_region.append(str(port.device))
        self.current_excel_file = None
        
        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()

    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def search_in_table(self):
        # 获取搜索关键字
        search_key = self.line_search_edit.text().lower()

        if search_key:
            # 遍历表格，检查每一行是否包含搜索关键词
            for row in range(self.table_info_widget.rowCount()):
                row_matches = False  # 标记行是否匹配
                for col in range(self.table_info_widget.columnCount()):
                    item = self.table_info_widget.item(row, col)
                    if item and search_key in item.text().lower():  # 不区分大小写
                        row_matches = True
                        break  # 一旦找到匹配项，跳出列的循环

                # 显示匹配的行，其他行隐藏
                self.table_info_widget.setRowHidden(row, not row_matches)
        else:
            # 如果没有输入搜索关键字，显示所有行
            for row in range(self.table_info_widget.rowCount()):
                self.table_info_widget.setRowHidden(row, False)

    def export_in_table(self):
        """将表格数据导出到 Excel 文件"""
        try:
            # 检查表格是否有数据
            if self.table_info_widget.rowCount() == 0 or self.table_info_widget.columnCount() == 0:
                QMessageBox.warning(self, "导出失败", "表格中没有数据可导出")
                return
            
            # 选择保存路径
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "导出 Excel 文件", 
                "", 
                "Excel 文件 (*.xlsx);;所有文件 (*)"
            )
            
            if not file_path:
                return  # 用户取消选择
            
            # 确保文件扩展名是 .xlsx
            if not file_path.endswith('.xlsx'):
                file_path += '.xlsx'
            
            # 从表格中提取数据
            data = []
            headers = []
            
            # 获取表头
            for col in range(self.table_info_widget.columnCount()):
                header_item = self.table_info_widget.horizontalHeaderItem(col)
                header = header_item.text() if header_item else f"列{col+1}"
                headers.append(header)
            
            # 获取表格数据
            for row in range(self.table_info_widget.rowCount()):
                row_data = []
                for col in range(self.table_info_widget.columnCount()):
                    item = self.table_info_widget.item(row, col)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                data.append(row_data)
            
            # 创建 DataFrame
            df = pd.DataFrame(data, columns=headers)
            
            # 导出到 Excel
            df.to_excel(file_path, index=False, engine='openpyxl')
            
            QMessageBox.information(self, "导出成功", f"数据已成功导出到:\n{file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出过程中发生错误:\n{str(e)}")
    
    def update_current_count(self):
        selected_text = self.select_timer_count.currentText()
        self.current_count_lable.setText(f"当前次数 {selected_text}")

    def select_path(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        
        # 如果选择了文件，设置路径到文本框
        if file_path:
            self.import_path.setText(file_path)
            self.load_excel_to_table(file_path)

    def load_excel_to_table(self, file_path):   
        # 读取 Excel 文件
        try:
            df = pd.read_excel(file_path)

            if '姓名' in df.columns:
                names = df['姓名'].dropna().unique().tolist()  # 获取所有非空名字，并去重
                self.select_name.clear()
                for name in names:
                    self.select_name.addItem(name)

            self.table_info_widget.clear()
            self.table_info_widget.setRowCount(df.shape[0])
            self.table_info_widget.setColumnCount(df.shape[1])
            self.table_info_widget.setHorizontalHeaderLabels(df.columns.tolist())  # 表头

            for row in range(df.shape[0]):
                for col in range(df.shape[1]):
                    value = df.iat[row, col]
                    if pd.isna(value):
                        value = ""
                    item = QTableWidgetItem(str(value))
                    self.table_info_widget.setItem(row, col, item)

        except Exception as e:
            print(f"Error loading Excel file: {e}")

    def start_race(self):
        self.run_start.setEnabled(False) 
        set_timer= self.select_timer_combox.currentText()
        # self.timer_info_lable.setText(set_timer)
        self.timer_info_lable.setText("等待开始...")
        # 启动设备
        duration_seconds = float(set_timer.rstrip('s'))
        duration_minutes = duration_seconds / 60.0

        self.race_device = CountDevice()
        self.race_device.clear()
        self.race_started = False
        self.race_device.run(self.race_region.currentText(),minute=duration_minutes)  # 6 秒
        # 设置定时器定期更新界面
        self.race_timer = QTimer()
        self.race_timer.timeout.connect(self.update_race_status)
        self.race_timer.start(10)  # 10毫秒更新一次     

    def update_race_status(self):
        if self.race_device:
            current_timer = self.race_device.get_count()
            time_start_flag= self.race_device.time_start_flag


            self.real_timer_count.setText(f"当前总有效成绩 {current_timer}次")
            current_info={"msg":""}
            if self.race_device.get_grade_info():
                current_info = self.race_device.get_grade_info()[-1]

            # 开始计时
            if time_start_flag and not self.race_started:
                self.race_timer_elapsed.start()
                self.race_started = True
              # 更新计时显示
            if self.race_started:
                # if self.race_device.get_time_remain():
                elapsed_ms = float(self.race_device.get_time_remain())
                # self.race_timer_elapsed.elapsed()
                seconds = elapsed_ms // 1000
                milliseconds = elapsed_ms % 1000
                
                # self.timer_info_lable.setText(f"用时: {seconds}.{milliseconds:03d} 秒") 
                self.timer_info_lable.setText(f"剩余时间: {elapsed_ms :.3f} 秒")
            if self.race_started:
                # if current_info["level"] in ["warrning","error"]:
                    
                    self.unqualified_info.setText(current_info["msg"])
                    # # 保存到 Excel
                    # self.save_to_excel(current_info, current_timer)
            # 检查是否结束
            if self.race_device.end_flag:
                if self.race_started:
                    elapsed_ms = self.race_timer_elapsed.elapsed()
                    seconds = elapsed_ms // 1000
                    milliseconds = elapsed_ms % 1000
                    time_str = f"{seconds}.{milliseconds:03d}"
                else:
                    time_str = "0.000"
                
                print(f"最终成绩: {self.race_device.get_count()}次, 用时: {time_str}秒")               
                # self.timer_info_lable.setText(f"完成! 用时: {math.ceil(float(time_str))}秒")
                self.excel_ops_enhanced()
                # self.table_ops()
                
                self.race_device.clear()
                self.race_timer.stop()
                self.run_start.setEnabled(True)
                self.race_device = None
                self.race_started = False

    def excel_ops_enhanced(self):
        """excel表格操作,插入到excel表格中"""
        try:
            _count = self.race_device.get_count()
            _name = self.select_name.currentText()
            _num = self.select_timer_count.currentText()
            _path = self.import_path.text()
            _logs = self.race_device.get_grade_info()
            
            if not os.path.exists(_path):
                print(f"Excel文件不存在: {_path}")
                return
            
            # 读取或创建Excel文件
            if os.path.exists(_path):
                df = pd.read_excel(_path)
            else:
                # 创建新的DataFrame
                columns = self.get_column_names()
                df = pd.DataFrame(columns=columns)
            
            # 确保列数足够
            required_columns = 12
            if df.shape[1] < required_columns:
                current_columns = df.shape[1]
                for i in range(current_columns, required_columns):
                    df[f'列{i+1}'] = ''
            
            # 设置有意义的列名
            column_names = self.get_column_names()
            if len(df.columns) >= len(column_names):
                df.columns = column_names[:len(df.columns)]
            
            # 查找或创建行
            target_row = self.find_or_create_row(df, _name)
            
            # 插入成绩
            if "一" in _num:
                df.iloc[target_row, 6] = _count  # 第七列：第一次成绩
                df.iloc[target_row, 10] = str(_logs) # 第十一列：第一次info
            elif "二" in _num:
                df.iloc[target_row, 7] = _count  # 第八列：第二次成绩
                df.iloc[target_row, 11] = str(_logs) # 第十二列：第二次info

            
            # 计算和处理数据
            self.calculate_total_score(df)
            self.sort_by_total_score(df)
            # 保存文件
            self.save_excel_with_formatting(df, _path)

            self.add_ranking_enhanced(df)     
            
            # 保存文件
            self.save_excel_with_formatting(df, _path)

            # 短暂延迟后加载表格，确保文件已保存
            time.sleep(0.5)
            # 显示表格
            self.load_excel_to_table(_path)
            
            print(f"Excel操作完成: {_name} 的{_num}成绩 {_count} 已保存")
            
        except Exception as e:
            print(f"Excel操作出错: {e},{traceback.format_exc()}")

    def find_or_create_row(self, df, name):
        """查找或创建匹配姓名的行"""
        for idx, row in df.iterrows():
            if str(row.iloc[2]).strip() == name.strip():  # 第三列是姓名
                return idx
        
        # 创建新行
        new_row = ['' for _ in range(df.shape[1])]
        new_row[2] = name  # 姓名列
        df.loc[len(df)] = new_row
        return len(df) - 1

    def calculate_total_score(self, df):
        """计算第七列和第八列的总分，插入到第九列"""
        try:
            # 确保第九列存在
            if df.shape[1] < 9:
                df['列9'] = ''
            
            # 计算每个行的总分
            for idx in range(len(df)):
                print(1111,df.iloc[idx, 6],df.iloc[idx, 7])
                score1 = self.safe_convert_to_float(df.iloc[idx, 6])  # 第七列
                score2 = self.safe_convert_to_float(df.iloc[idx, 7])  # 第八列
                total = score1 + score2 
                if total != 0:
                    # 如果是整数，转换为int类型
                    if total == int(total):
                        df.iloc[idx, 8] = int(total)  # 存储为整数
                    else:
                        df.iloc[idx, 8] = total       # 存储为浮点数
                
        except Exception as e:
            print(f"计算总分出错: {e}")

    def sort_by_total_score(self, df):
        """按总分从高到低排序"""
        try:
            # 确保有第九列（总分列）
            if df.shape[1] < 9:
                return
            
            # 将总分列转换为数值类型
            df['总分数值'] = pd.to_numeric(df.iloc[:, 8], errors='coerce').fillna(0)
            
            # 按总分降序排序
            df.sort_values('总分数值', ascending=False, inplace=True)
            
            # 删除临时列
            df.drop('总分数值', axis=1, inplace=True)
            
            # 重置索引
            df.reset_index(drop=True, inplace=True)
            
        except Exception as e:
            print(f"排序出错: {e}")

    def add_ranking_enhanced(self, df):
        """增强版名次添加，只对有成绩的选手排名"""
        try:
            # 确保有第10列（名次列）
            if df.shape[1] < 10:
                # 添加名次列
                df['名次'] = ""
            else:
                # 重置所有名次为空
                df.iloc[:, 9] = ""
            
            
            # 筛选出有成绩的行（总分 > 0）
            valid_scores = []
            for idx in range(len(df)):
                # 获取总分（第9列，索引8）
                total_score = self.safe_convert_to_float(df.iloc[idx, 8])
                
                if total_score > 0:
                    valid_scores.append((total_score, idx))
            
            
            if not valid_scores:
                print("没有找到有成绩的选手")
                return
            
            # 按总分降序排序
            valid_scores.sort(key=lambda x: x[0], reverse=True)
            
            # 分配名次
            current_rank = 1
            previous_score = None
            
            for i, (score, row_idx) in enumerate(valid_scores):
                # 如果当前分数与前一分数相同，则名次相同
                if score == previous_score:
                    df.iloc[row_idx, 9] = int(current_rank - 1)   
                else:
                    df.iloc[row_idx, 9] = int(current_rank)
                    current_rank += 1
                
                previous_score = score
            
            # 验证名次分配
            for idx in range(len(df)):
                total_score = self.safe_convert_to_float(df.iloc[idx, 8])
                ranking = df.iloc[idx, 9]
            
        
        except Exception as e:
            print(f"添加名次出错: {e}")
            import traceback
            traceback.print_exc()

    def save_excel_with_formatting(self, df, file_path):
        """保存Excel文件并添加格式"""
        try:
            # 先用pandas保存数据
            df.to_excel(file_path, index=False)
            
            # 使用openpyxl添加格式
            wb = load_workbook(file_path)
            ws = wb.active
            
            # 设置表头样式
            header_font = Font(bold=True)
            for cell in ws[1]:
                cell.font = header_font
                cell.alignment = Alignment(horizontal='center')
            
            # 设置列宽
            column_widths = {
                'A': 15, 'B': 15, 'C': 20, 'D': 15, 'E': 15,
                'F': 15, 'G': 15, 'H': 15, 'I': 15, 'J': 15
            }
            
            for col, width in column_widths.items():
                ws.column_dimensions[col].width = width
            
            # 设置数据居中对齐
            for row in ws.iter_rows(min_row=2, max_row=ws.max_row, 
                                min_col=1, max_col=ws.max_column):
                for cell in row:
                    cell.alignment = Alignment(horizontal='center')
            
            # 保存格式化的Excel
            wb.save(file_path)
            
        except Exception as e:
            print(f"保存Excel格式出错: {e}")
            # 如果格式化失败，至少保存数据
            df.to_excel(file_path, index=False)

    def safe_convert_to_float(self, value):
        """安全地将值转换为浮点数"""
        try:
            if pd.isna(value) or value == '' or value is None:
                return 0.0
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def get_column_names(self):
        """获取列名列表"""
        return ['组别', '学号', '姓名', '性别', '年龄', '赛事名称', '第一次', '第二次', '总分', '名次', '第一次信息', '第二次信息'] 

    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # Remove Selection If Clicked By "btn_close_left_column"
        if btn.objectName() != "btn_settings":
            self.ui.left_menu.deselect_all_tab()

        # Get Title Bar Btn And Reset Active         
        top_settings = MainFunctions.get_title_bar_btn(self, "btn_top_settings")
        top_settings.set_active(False)

        # LEFT MENU
        # ///////////////////////////////////////////////////////////////
        
        # HOME BTN
        if btn.objectName() == "btn_home":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 1
            MainFunctions.set_page(self, self.ui.load_pages.page_1)

        # WIDGETS BTN
        if btn.objectName() == "go_race_widgets":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 2
            MainFunctions.set_page(self, self.ui.load_pages.page_go_race)

        # LOAD USER PAGE
        if btn.objectName() == "btn_add_user":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 3 
            MainFunctions.set_page(self, self.ui.load_pages.page_3)

        # BOTTOM INFORMATION
        if btn.objectName() == "btn_info":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                self.ui.left_menu.select_only_one_tab(btn.objectName())

                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_2,
                    title = "Info tab",
                    icon_path = Functions.set_svg_icon("icon_info.svg")
                )

        # SETTINGS LEFT
        if btn.objectName() == "btn_settings" or btn.objectName() == "btn_close_left_column":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_setting,
                    title = "Settings Left Column",
                    icon_path = Functions.set_svg_icon("icon_settings.svg")
                )
        
        # TITLE BAR MENU
        # ///////////////////////////////////////////////////////////////
        
        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_top_settings":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                btn.set_active(True)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)

            # Get Left Menu Btn            
            top_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            top_settings.set_active_tab(False)            

        # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()


# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////
if __name__ == "__main__":
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()

    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    sys.exit(app.exec_())