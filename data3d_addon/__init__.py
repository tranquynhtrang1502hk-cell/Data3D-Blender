"""
Data3D - Add-on Blender vẽ biểu đồ 3D từ file CSV.
File này là "cửa vào" của add-on: khai báo thông tin (bl_info)
và đăng ký / hủy đăng ký các module con.
"""

bl_info = {
    "name": "Data3D",
    "author": "Trần Quỳnh Trang",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar (phím N) > Data3D",
    "description": "Vẽ biểu đồ cột / đường 3D từ file CSV",
    "category": "3D View",
}

import importlib

from . import properties, operators, panels

# Khi bật/tắt lại add-on lúc đang phát triển, nạp lại code mới nhất
if "_da_nap" in globals():
    importlib.reload(properties)
    importlib.reload(operators)
    importlib.reload(panels)
_da_nap = True

# Thứ tự đăng ký: thuộc tính -> thao tác -> giao diện
modules = (properties, operators, panels)


def register():
    for m in modules:
        m.register()


def unregister():
    # Hủy theo thứ tự ngược lại
    for m in reversed(modules):
        m.unregister()