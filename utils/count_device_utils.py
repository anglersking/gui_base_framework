import time
import threading
import re
import serial  # 需要 pip install pyserial

class CountDevice:
    def __init__(self):
        self.count: int = 0
        self.start_flag: bool = True
        self.end_flag: bool = False
        self.minute = 5
        self.thread = None
        self.lock = threading.Lock()
        self.grade_info:list =list()
        # [{"level":"warrning","msg":"合格不合格xxxx"}]

    def send_stop(self):
        self.start_flag = False

    def clear(self):
        with self.lock:
            self.count = 0

    def run(self, region: str = "COM5", baud: int = 115200, minute: int = 5, TEST=True):
        """region = 串口号，比如 'COM5' 或 '/dev/ttyUSB0'"""
        self.start_flag = True
        self.end_flag = False
        self.minute = minute
        self.time_start = time.time()

        def worker_test():
            print(f"[TEST] 模拟计数，区域: {region}")
            while True:
                if not self.start_flag:
                    self.clear()
                    break
                if time.time() - self.time_start < self.minute * 60:
                    time.sleep(1)
                    with self.lock:
                        self.count += 1
                else:
                    print("测试时间到")
                    self.end_flag = True
                    break

        def worker_real():
            print(f"[REAL] 打开串口 {region}, {baud} baud")
            try:
                ser = serial.Serial(region, baud, timeout=1)
            except Exception as e:
                print(f"串口打开失败: {e}")
                self.end_flag = True
                return

            left_cout, right_cout = 0, 0
            left_flag, right_flag = True, True
            total=0
            last_line=""
            current_line=""
            while True:
                if not self.start_flag:
                    break
                if time.time() - self.time_start >= self.minute * 60:
                    print("真实计数时间到")
                    self.end_flag = True
                    break

                try:
                    line = ser.readline().decode(errors="ignore").strip()
                except Exception as e:
                    print(f"串口读取错误: {e}")
                    continue

                if not line:
                    continue

                match = re.search(
                    r"ID:\s*(\d+)\s*\|\s*Left Volt:\s*([\d.]+)\s*V\s*\|\s*Right Volt:\s*([\d.]+)\s*V",
                    line
                )
                if match:
                    left_vol = float(match.group(2))
                    right_vol = float(match.group(3))

                    if left_vol < 0.03:
                        if right_cout>0:
                            # print("右边 无效成绩，双脚经过次数",right_cout)
                            info={"level":"error","msg":f"右边无效成绩，双脚经过次数 {right_cout}"}
                            self.grade_info.append(info)
                            right_cout=0
                        if left_flag:
                            if left_cout>=4:
                                left_cout=0
                            left_cout+=1
                            print(f"左边经过{left_cout}次")
                            
                            left_flag=False

                    if left_vol > 0.9:
                        left_flag = True

                    if right_vol < 0.03:
                        
                        if left_cout>0:
                            # print("左边 无效成绩，双脚经过次数",left_cout)
                            info={"level":"error","msg":f"左边无效成绩，双脚经过次数 {left_cout}"}
                            self.grade_info.append(info)

                            left_cout=0
                        if right_flag:
                            if right_cout >= 2:
                                right_cout = 0
                            right_cout += 1
                            print(f"右边经过{right_cout}次")
                            right_flag = False
                    if right_vol > 0.9:
                        right_flag = True

                    if left_cout==4 or right_cout==4:
                        total+=1
                        self.count=total

                        if right_cout==4:
                            current_line="right"
                            if last_line==current_line:
                                # print("警报 左面没过线重复过右面")
                                info={"level":"warning","msg":"警报 左面没过线重复过右面"}
                                self.grade_info.append(info)

                           
                            last_line=current_line
                            # print(f"右边过的 有效成绩：{total} 次")
                            info={"level":"info","msg":f"右边过的 有效成绩：{total} 次"}
                            self.grade_info.append(info)


                        if left_cout==4:
                            current_line="left"
                            print(f"左边过的 有效成绩：{total} 次")
                            

                            if last_line==current_line:
                                # print("警报 右边没过线重复过左面")
                                info={"level":"warning","msg":"警报 右边没过线重复过左面"}
                                self.grade_info.append(info)

                            last_line=current_line
                             # print(f"右边过的 有效成绩：{total} 次")
                            info={"level":"info","msg":f"左边过的 有效成绩：{total} 次"}
                            self.grade_info.append(info)

                        left_cout=0
                        right_cout=0

            try:
                ser.close()
            except:
                pass

        self.thread = threading.Thread(
            target=worker_test if TEST else worker_real,
            daemon=True
        )
        self.thread.start()

    def get_count(self)->int:
        with self.lock:
            return self.count
    def get_grade_info(self)->list:
        return self.grade_info


if __name__ == "__main__":
    # 测试模式
    device = CountDevice()
    device.clear()
    device.run(region="COM5", minute=0.1, TEST=True)  # 6秒模拟
    while True:
        print("当前 count:", device.get_count())
        time.sleep(1)
        if device.end_flag:
            print(f"最终成绩:{device.get_count()}")
            device.clear()
            break

    # 串口真实模式
    device = CountDevice()
    device.run(region="COM5", baud=115200, minute=0.2, TEST=False)  # 串口采集12秒
    while True:
        print("当前 count:", device.get_count())
        time.sleep(1)
        if device.end_flag:
            print(f"最终成绩:{device.get_count()}")
            device.clear()
            break