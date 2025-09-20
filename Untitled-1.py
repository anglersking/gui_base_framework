

import time

from nine_ghost.serial_convertor.hardware_BLL.gpio_BLL import Gpio_manager


count_app=Gpio_manager()
count_app.set_com("com5")
count_app.new_compation_prepare()

count=count_app.start_count()

timer_count=60

while True: 
#中途 实时的
  time.sleep(0.1)

  current_count=count_app.get_gpio_count_value()
  print("倒计时",timer_count,"已过线次数",current_count)

  timer_count-=1
  if timer_count==0:
     count_app.stop_count()
     break

print("最终成绩 ", count_app.get_gpio_count_value())




