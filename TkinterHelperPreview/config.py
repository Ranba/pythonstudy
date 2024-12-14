import logging.handlers

# 版本号
version = "2.11.2"
# 预览服务默认地址
host = "127.0.0.1"
port = 12300
# 托盘菜单跳转地址
update_url = f"https://www.pytk.net/tkinter-helper-preview.html?from=preview&version={version}"
helper_url = f"https://www.pytk.net/?from=preview&version={version}"

# 创建logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# 创建handler，用于写入日志文件
handler = logging.handlers.TimedRotatingFileHandler(
    filename='tkinter_helper.log',  # 日志文件名
    when='D',  # 间隔类型，这里是按天
    interval=1,  # 间隔的数量
    backupCount=7  # 保留的备份文件的个数
)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(handler)
