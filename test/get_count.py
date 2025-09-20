import time
import threading

class CountDevice:
    def __init__(self):
        self.count: int = 0
        self.start_flag: bool = True
        self.end_flag: bool = False
        self.minute = 5
        self.thread = None
        self.lock = threading.Lock()

    def send_stop(self):
        self.start_flag = False

    def clear(self):
        self.count=0

    def run(self, minute: int = 5, TEST=True):
        self.start_flag = True
        self.end_flag = False
        self.minute = minute
        self.time_start = time.time()

        def worker():
            while True:
                if not self.start_flag:
                    with self.lock:
                        self.count = 0
                    break

                if TEST:
                    if time.time() - self.time_start < self.minute * 60:  # 分钟转秒
                        time.sleep(1)
                        with self.lock:
                            self.count += 1
                    else:
                        print("时间到")
                        self.end_flag = True
                        break

        self.thread = threading.Thread(target=worker, daemon=True)
        self.thread.start()

    def get_count(self):
        with self.lock:
            return self.count


if __name__ == "__main__":
    device = CountDevice()
    device.clear()
    device.run(minute=0.1)  # 6 秒

    while True:
        print("当前 count:", device.get_count())
        time.sleep(1)
        if device.end_flag:
            print(f"最终成绩:{device.count}")
            device.clear()
            break

    device.run(minute=0.2)
    while True:
        print("当前 count:", device.get_count())
        time.sleep(1)
        if device.end_flag:
            print(f"最终成绩:{device.count}")
            device.clear()
            break
        
