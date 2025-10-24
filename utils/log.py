import inspect
import logging
from logging import handlers
from colorama import Fore, Style
import os
import sys

# 获取对象
def get_logger():
    logger = logging.getLogger("kpi_gui.log")
    logger.setLevel(logging.DEBUG)
 

    if not logger.handlers:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = ColoredFormatter(
            '%(asctime)s - %(message)s'
        )

        # formatter = ColoredFormatter(
        #     '%(asctime)s - %(pathname)s[line:%(lineno)d] - [%(levelname)s]: %(message)s'
        # )

       
  
        ch.setFormatter(formatter)
        fmt='%(asctime)s - %(message)s'
        # fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - [%(levelname)s]: %(message)s'
        format_str_inlog = logging.Formatter(fmt)#设置日志格式

        when='D'
        backCount=3

        th = handlers.TimedRotatingFileHandler(filename="kpi_gui.log",when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str_inlog)#设置文件里写入的格式

        logger.addHandler(ch)
        logger.addHandler(th)
    
    return logger

# 自定义 Formatter
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.WHITE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        log_message = super(ColoredFormatter, self).format(record)
        log_level_color = self.COLORS.get(record.levelname, Fore.RESET)
        return f'{log_level_color}{log_message}{Style.RESET_ALL}'

#通过静态成员方法来调用
class Log:

    logger = get_logger()

    @staticmethod
    def debug(msg):
        caller_frame = inspect.stack()[1]
        file_path = caller_frame.filename
        line_number = caller_frame.lineno
        Log.logger.debug(f"{file_path}:{line_number} [DEBUG]: {str(msg)}")
        # Log.logger.debug(str(msg))

    @staticmethod
    def info(msg):
        caller_frame = inspect.stack()[1]
        file_path = caller_frame.filename
        line_number = caller_frame.lineno
        Log.logger.info(f"{file_path}:{line_number} [INFO]: {str(msg)}")
        # Log.logger.info(str(msg))

    @staticmethod
    def warning(msg):
        caller_frame = inspect.stack()[1]
        file_path = caller_frame.filename
        line_number = caller_frame.lineno
        Log.logger.warning(f"{file_path}:{line_number} [WARNING]: {str(msg)}")
        # Log.logger.warning(str(msg))

    @staticmethod
    def error(msg):
        caller_frame = inspect.stack()[1]
        file_path = caller_frame.filename
        line_number = caller_frame.lineno
        Log.logger.error(f"{file_path}:{line_number} [ERROR]: {str(msg)}")
        # Log.logger.error(str(msg))

    @staticmethod
    def critical(msg):
        caller_frame = inspect.stack()[1]
        file_path = caller_frame.filename
        line_number = caller_frame.lineno
        Log.logger.critical(f"{file_path}:{line_number} [CRITICAL]: {str(msg)}")
        # Log.logger.critical(str(msg))


