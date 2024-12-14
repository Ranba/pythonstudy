import multiprocessing
import socket
import sys
from multiprocessing import Process

import uvicorn

from api import app
from config import host, port, logger
from tray_menu import create_tray_menu


def is_opened():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((host, port))
        sock.close()
        return True
    except:
        return False


def api_server():
    log_config = {
        "version": 1,
        "disable_existing_loggers": True,
    }
    uvicorn.run(app=app, host=host, port=port, log_config=log_config)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    if is_opened():
        # 检测端口是否被占用
        logger.error("端口被占用")
        sys.exit()
    Process(target=api_server, name="api_server").start()
    create_tray_menu().run()
