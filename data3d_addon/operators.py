
# pylint: disable=import-error,no-member,invalid-name

"""
Phần xử lý chính: đọc CSV, dựng biểu đồ, hoạt họa, xuất ảnh.
Gồm 3 nhóm: hàm hỗ trợ -> hàm dựng biểu đồ -> các Operator (nút bấm).
"""

import math
import csv

import bpy
from mathutils import Vector

COL_NAME = "Data3D"   
MAX_ROWS = 50         



# 1. HÀM HỖ TRỢ


def gradient(t):
    """Đổi số t (0..1) thành màu RGBA: xanh dương -> xanh lá -> đỏ."""
    if t < 0.5:
        k = t * 2
        return (0.0, k, 1.0 - k, 1.0)
    k = (t - 0.5) * 2
    return (k, 1.0 - k, 0.0, 1.0)


def make_material(name, color):
    """Tạo vật liệu có màu. diffuse_color hiện ở viewport, node dùng khi render."""
    mat = bpy.data.materials.new(name=name)
    mat.diffuse_color = color
    try:
        if mat.node_tree is None:
            mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = color
    except Exception:
        pass  # Không có node thì vẫn còn diffuse_color
    return mat


def get_collection(scene):
    """Lấy Collection Data3D, chưa có thì tạo mới."""
    col = bpy.data.collections.get(COL_NAME)
    if col is None:
        col = bpy.data.collections.new(COL_NAME)
        scene.collection.children.link(col)
    return col


def clear_chart():
    """Xóa biểu đồ cũ (chỉ trong Collection Data3D, không đụng camera/đèn)."""
    col = bpy.data.collections.get(COL_NAME)
    if col is None:
        return
    for obj in list(col.objects):
        data = obj.data
        bpy.data.objects.remove(obj, do_unlink=True)
        # Dọn dữ liệu hình khối không còn ai dùng
        if data is not None and data.users == 0:
            if isinstance(data, bpy.types.Mesh):
                bpy.data.meshes.remove(data)
            elif isinstance(data, bpy.types.Curve):
                bpy.data.curves.remove(data)
    # Dọn vật liệu của add-on không còn ai dùng
    for mat in list(bpy.data.materials):
        if mat.name.startswith("D3D_") and mat.users == 0:
            bpy.data.materials.remove(mat)


def move_to_col(obj, col):
    """Chuyển đối tượng vào Collection chỉ định."""
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)

