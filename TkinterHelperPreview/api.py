from multiprocessing import active_children, Process

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import version, logger
from core.GenerateWin import GenerateWin
from core.models import TkModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {'version': version, 'msg': "窗口预览服务已启动"}


@app.post("/")
def post(tk: TkModel):
    for p in active_children():
        if p.name == "preview":
            p.kill()
    Process(target=preview, args=(tk,), name="preview").start()
    return {'msg': "发送成功"}


def preview(tk):
    try:
        tk_json_obj = GenerateWin(tk)
        tk_json_obj.build()
    except Exception as e:
        logger.exception("创建预览窗口出错", e)
