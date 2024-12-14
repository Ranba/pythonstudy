from typing import List

from pydantic import BaseModel


# 所有组件都有
class WidgetBaseInfo(BaseModel):
    id: str
    type: str
    frame: bool = False
    event_bind_list: list = []


# 大小定位相关
class PlaceInfo(WidgetBaseInfo):
    top: int
    left: int
    width: int
    height: int


class WidgetModel(PlaceInfo):
    boot_color: str
    boot_type: str
    text: str = ""
    elements: List['WidgetModel'] = []
    vbar: bool = False
    hbar: bool = False
    options: list = []
    columns: list = []
    tabs: list = []
    tab: int = 0
    styles: dict = None
    # Meter
    sub_text: str = ""
    text_left: str = ""
    text_right: str = ""
    interactive: bool = False
    #
    color: str = ''
    icon: str = ''


class WinModel(PlaceInfo):
    elements: List['WidgetModel'] = []
    is_auto_size: bool
    is_ttkbootstrap: bool
    menus: list = []
    text: str
    top_level: bool
    ttkbootstrap_theme: str


class TkModel(BaseModel):
    win: WinModel
