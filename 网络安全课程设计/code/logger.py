import logging
import os
from colorama import Fore, Style
from datetime import datetime
from colorama import init
init(autoreset=True)

MAX_LOG = 100
LOG_DIR = "logs"
LOG_FILENAME_ENV = "RSA_LOGGER"

class ColorFormatter(logging.Formatter):
    """自定义日志格式化器，支持颜色输出"""
    LEVEL_STYLES = {
        "INFO": f"[{Fore.GREEN}INFO{Style.RESET_ALL}]    ",
        "DEBUG": f"[{Fore.BLUE}DEBUG{Style.RESET_ALL}]   ",
        "WARNING": f"[{Fore.YELLOW}WARNING{Style.RESET_ALL}] ",
        "ERROR": f"[{Fore.RED}ERROR{Style.RESET_ALL}]   ",
        "CRITICAL": f"[{Fore.MAGENTA}CRITICAL{Style.RESET_ALL}]"
    }

    def format(self, record):
        record.pathname = os.path.relpath(record.pathname)
        log_msg = super().format(record)
        # 替换日志级别为对应的颜色样式
        if record.levelname in self.LEVEL_STYLES:
            log_msg = log_msg.replace(record.levelname, self.LEVEL_STYLES[record.levelname])
        return log_msg

def manage_log_files(log_dir, max_log):
    def parse_date(filename):
        try:
            return datetime.strptime(filename.split(".")[0], "%Y-%m-%d_%H-%M-%S")
        except ValueError:
            return datetime.min

    log_files = [f for f in os.listdir(log_dir) if f.endswith(".log")]
    log_files = sorted(log_files, key=parse_date)
    while len(log_files) > max_log:
        try:
            oldest_file = log_files.pop(0)
            os.remove(os.path.join(log_dir, oldest_file))
        except Exception: ...


def get_logger(console_level=logging.INFO, max_log=MAX_LOG):
    logger = logging.getLogger("logger")
    # 如果logger已经有handler，则直接返回
    if logger.hasHandlers():
        return logger

    # 设置日志级别
    logger.setLevel(logging.DEBUG)

    # 设置控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    formatter = ColorFormatter(
        fmt="%(asctime)s.%(msecs)03d %(levelname)s[%(pathname)s:%(lineno)d] %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)

    # 设置文件日志处理器
    os.makedirs(LOG_DIR, exist_ok=True)
    log_filename = os.environ.get(LOG_FILENAME_ENV, None)
    if not log_filename:
        # 如果没有环境变量，则生成一个新的文件名
        log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
        os.environ[LOG_FILENAME_ENV] = log_filename
        manage_log_files(LOG_DIR, max_log)
    file_path = os.path.join(LOG_DIR, log_filename)

    file_handler = logging.FileHandler(file_path, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d [%(levelname)s] [%(pathname)s:%(lineno)d] %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)

    # 添加处理器到logger
    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    logger.console_handler = console_handler
    logger.file_handler = file_handler

    return logger

def set_log_level(logger, level):
    """设置日志级别"""
    logger.console_handler.setLevel(level)