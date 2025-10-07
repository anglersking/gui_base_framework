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
        # ports = serial.tools.list_ports.comports()
        ports = ["COM3","COM5"]
        self.race_region.clear()
        self.race_region.addItems(ports)
        # for port in ports:
        #     print(f"设备: {port.device}, 描述: {port.description}")
        #     self.slect_race_region.items.append(str(port.device))
        self.excel_folder = "D:/race_detail_info"
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
        self.initialize_excel_file()
        self.race_device.run(self.race_region.currentText(),minute=duration_minutes)  # 6 秒
        # 设置定时器定期更新界面
        self.race_timer = QTimer()
        self.race_timer.timeout.connect(self.update_race_status)
        self.race_timer.start(10)  # 10毫秒更新一次
        

    def update_race_status(self):
        if self.race_device:
            current_timer = self.race_device.get_count()
            self.real_timer_count.setText(f"当前次数 {current_timer}次")
            current_info = self.race_device.get_grade_info()[0]

            # 开始计时
            if current_timer >= 1 and not self.race_started:
                self.race_timer_elapsed.start()
                self.race_started = True
              # 更新计时显示
            if self.race_started:
                elapsed_ms = self.race_timer_elapsed.elapsed()
                seconds = elapsed_ms // 1000
                milliseconds = elapsed_ms % 1000
                self.timer_info_lable.setText(f"用时: {seconds}.{milliseconds:03d} 秒") 
            if self.race_started:
                if current_info["level"] in ["warrning","error"]:
                    
                    self.unqualified_info.setText(current_info["msg"])
                    # 保存到 Excel
                    self.save_to_excel(current_info, current_timer)
            # 检查是否结束
            if self.race_device.end_flag:
                if self.race_started:
                    elapsed_ms = self.race_timer_elapsed.elapsed()
                    seconds = elapsed_ms // 1000
                    milliseconds = elapsed_ms % 1000
                    time_str = f"{seconds}.{milliseconds:03d}"
                else:
                    time_str = "0.000"
                
                print(f"最终成绩: {self.race_device.count}次, 用时: {time_str}秒")               
                self.timer_info_lable.setText(f"完成! 用时: {math.ceil(float(time_str))}秒")
                self.table_ops()
                
                self.race_device.clear()
                self.race_timer.stop()
                self.run_start.setEnabled(True)
                self.race_device = None
                self.race_started = False

    def table_ops(self):
        """表格操作：插入值并根据条件进行排序"""
        try:
            timer_text = self.select_timer_count.currentText()
            
            # 在表格中查找并修改
            if "一" in timer_text:
                target_column = 6  # 第7列
                self.insert_value_and_sort(target_column)
                
            elif "二" in timer_text:
                target_column = 7  # 第8列
                self.calculate_and_sort()
                
            else:
                print("未检测到'一'或'二'")
                return
                
        except Exception as e:
            print(f"表格操作出错: {e}")

    def insert_value_and_sort(self, target_column):
        """插入值并按照目标列排序"""
        # 插入值
        value_inserted = False
        for row in range(self.table_info_widget.rowCount()):
            item = self.table_info_widget.item(row, 2)  # 第三列（索引2）匹配姓名
            if item and item.text() == self.select_name.currentText():
                # +  random.randint(1, 10)
                new_item = QTableWidgetItem(f"{self.race_device.count }")
                self.table_info_widget.setItem(row, target_column, new_item)
                value_inserted = True
                # print(f"已在{self.select_name.currentText()}的第{target_column + 1}列插入值: {self.race_device.count}")
                break
        
        if value_inserted:
            # 按照目标列降序排序，空值排在最后
            self.sort_column_descending(target_column)
            # print(f"已按照第{target_column + 1}列降序排序")
        else:
            print(f"未找到姓名匹配的行: {self.select_name.currentText()}")

    def calculate_and_sort(self):
        """计算第7列+第8列的值插入第9列，并按照第9列排序"""
        # 首先确保表格有足够的列
        current_cols = self.table_info_widget.columnCount()
        if current_cols < 9:
            self.table_info_widget.setColumnCount(9)
            # 设置新列的表头（如果还没有）
            for col in range(current_cols, 9):
                header = self.table_info_widget.horizontalHeaderItem(col)
                if not header:
                    self.table_info_widget.setHorizontalHeaderItem(col, QTableWidgetItem(f"列{col+1}"))
        
        # 插入值到第8列
        value_inserted = False
        for row in range(self.table_info_widget.rowCount()):
            item = self.table_info_widget.item(row, 2)  # 第三列匹配姓名
            if item and item.text() == self.select_name.currentText():
                new_item = QTableWidgetItem(f"{self.race_device.count}")
                self.table_info_widget.setItem(row, 7, new_item)  # 第8列
                value_inserted = True
                # print(f"已在{self.select_name.currentText()}的第8列插入值: {self.race_device.count}")
                break
        
        if value_inserted:
            # 计算第7列+第8列，结果插入第9列
            self.calculate_sum_column(6, 7, 8)  # 第7列+第8列→第9列
            
            # 按照第9列降序排序
            self.sort_column_descending(8)  # 第9列索引为8
            # print("已计算第7列+第8列的值插入第9列，并按照第9列降序排序")
        else:
            print(f"未找到姓名匹配的行: {self.select_name.currentText()}")

    def calculate_sum_column(self, col1_idx, col2_idx, result_col_idx):
        """计算两列的和并插入到结果列"""
        for row in range(self.table_info_widget.rowCount()):
            # 获取第7列的值
            item1 = self.table_info_widget.item(row, col1_idx)
            value1 = self.safe_convert_to_float(item1.text() if item1 else "0")
            
            # 获取第8列的值
            item2 = self.table_info_widget.item(row, col2_idx)
            value2 = self.safe_convert_to_float(item2.text() if item2 else "0")
            
            # 计算总和
            total = value1 + value2
            
            # 插入到第9列
            result_item = QTableWidgetItem(str(total))
            self.table_info_widget.setItem(row, result_col_idx, result_item)

    def sort_column_descending(self, column_index):
        """按照指定列降序排序，空值排在最后"""
        rows = self.table_info_widget.rowCount()
        if rows <= 1:
            return
        
        # 收集所有行的数据和行索引
        row_data = []
        for row in range(rows):
            item = self.table_info_widget.item(row, column_index)
            if item and item.text().strip():
                try:
                    value = float(item.text())
                    row_data.append((value, row, 1))  # 第三个值表示有数据
                except ValueError:
                    # 如果不能转换为数字，按字符串处理
                    row_data.append((item.text(), row, 1))
            else:
                # 空值标记，排序时排在最后
                row_data.append((float('-inf'), row, 0))
        
        # 排序：先按是否有数据（1>0），再按值降序
        row_data.sort(key=lambda x: (x[2], x[0]), reverse=True)
        
        # 重新排列行
        self.reorder_table_rows([row_idx for _, row_idx, _ in row_data])

    def reorder_table_rows(self, new_row_order):
        """根据新的行顺序重新排列表格"""
        rows = self.table_info_widget.rowCount()
        cols = self.table_info_widget.columnCount()
        
        # 保存所有数据
        all_data = []
        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = self.table_info_widget.item(row, col)
                row_data.append(item.text() if item else "")
            all_data.append(row_data)
        
        # 按照新顺序重新设置数据
        for new_row, old_row in enumerate(new_row_order):
            for col in range(cols):
                new_item = QTableWidgetItem(all_data[old_row][col])
                self.table_info_widget.setItem(new_row, col, new_item)

    def safe_convert_to_float(self, text):
        """安全地将文本转换为浮点数"""
        try:
            return float(text)
        except ValueError:
            return 0.0    

    def initialize_excel_file(self):
        """初始化 Excel 文件"""
        try:
            # 创建文件夹（如果不存在）
            if not os.path.exists(self.excel_folder):
                os.makedirs(self.excel_folder)
                print(f"已创建文件夹: {self.excel_folder}")
            
            # 生成以当前名字_场次_时间为文件名的 Excel 文件
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            excel_filename = f"{self.select_name.currentText()}_{self.select_timer_count.currentText()}_{current_time}.xlsx"
            self.current_excel_file = os.path.join(self.excel_folder, excel_filename)
            
            # 创建空的 Excel 文件
            columns = ['timestamp', 'count', 'level', 'message']
            df = pd.DataFrame(columns=columns)
            df.to_excel(self.current_excel_file, index=False)
            print(f"已创建新的 Excel 文件: {self.current_excel_file}")
            
        except Exception as e:
            print(f"初始化 Excel 文件失败: {e}")
    
    def save_to_excel(self, current_info, current_timer):
        """保存信息到 Excel 文件"""
        try:
            # 确保文件已初始化
            if self.current_excel_file is None:
                self.initialize_excel_file()
            
            # 创建新记录
            new_record = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'count': current_timer,
                'level': current_info["level"],
                'message': current_info["msg"]
            }
            
            # 读取现有数据
            if os.path.exists(self.current_excel_file):
                df_existing = pd.read_excel(self.current_excel_file)
            else:
                df_existing = pd.DataFrame(columns=['timestamp', 'count', 'level', 'message'])
            
            # 添加新记录
            df_new = pd.DataFrame([new_record])
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            
            # 保存到 Excel
            df_combined.to_excel(self.current_excel_file, index=False)
            print(f"第 {current_timer} 次记录已保存到: {os.path.basename(self.current_excel_file)}")
            
        except Exception as e:
            print(f"保存到 Excel 失败: {e}")

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