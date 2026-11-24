
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


def load_font(path):
    """Nạp font từ file. Trả về None nếu không có hoặc lỗi."""
    if not path:
        return None
    try:
        return bpy.data.fonts.load(bpy.path.abspath(path), check_existing=True)
    except Exception:
        return None


def add_label(text, location, size, col, font=None):
    """Tạo chữ 3D dựng đứng, canh giữa. Trả về đối tượng chữ."""
    bpy.ops.object.text_add(location=location)
    t = bpy.context.active_object
    t.data.body = text
    t.data.size = size
    t.data.align_x = 'CENTER'
    if font:
        t.data.font = font
    t.rotation_euler = (math.radians(90), 0, 0)  # Quay đứng, hướng về camera
    move_to_col(t, col)
    return t


def read_csv(path):
    """
    Đọc file CSV. Trả về (danh_sách, None) nếu đúng,
    hoặc (None, "thông báo lỗi") nếu sai.
    Mỗi phần tử danh sách là (tên, giá_trị, emoji).
    """
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            lines = f.read().splitlines()
    except OSError as e:
        return None, f"Không mở được file: {e}"
    except UnicodeDecodeError:
        return None, "File không phải UTF-8. Hãy lưu lại với mã hóa UTF-8"

    if not lines:
        return None, "File rỗng"

    # Excel tiếng Việt hay dùng dấu ; làm dấu phân cách -> tự nhận biết
    delim = ";" if lines[0].count(";") > lines[0].count(",") else ","
    reader = csv.DictReader(lines, delimiter=delim)
    if not reader.fieldnames:
        return None, "Không đọc được dòng tiêu đề"

    # Chuẩn hóa tên cột: bỏ khoảng trắng, viết thường
    reader.fieldnames = [h.strip().lower() for h in reader.fieldnames]
    if "name" not in reader.fieldnames or "value" not in reader.fieldnames:
        return None, "File CSV cần có cột 'name' và 'value'"

    data = []
    for n, row in enumerate(reader, start=2):   # dòng 1 là tiêu đề
        name = (row.get("name") or "").strip()
        raw = (row.get("value") or "").strip().replace(",", ".")
        if not name and not raw:
            continue                             # bỏ qua dòng trống
        try:
            value = float(raw)
        except ValueError:
            return None, f"Dòng {n}: '{raw}' không phải là số"
        emoji = (row.get("emoji") or "").strip()
        data.append((name or f"Muc {n - 1}", value, emoji))

    if not data:
        return None, "File không có dòng dữ liệu nào"
    return data, None


def frame_view(context):
    """Zoom khung 3D để thấy toàn biểu đồ và bật chế độ xem màu."""
    try:
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                if area.type != 'VIEW_3D':
                    continue
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'MATERIAL'
                region = next((r for r in area.regions if r.type == 'WINDOW'), None)
                if region:
                    with context.temp_override(window=window, area=area, region=region):
                        bpy.ops.view3d.view_all()
    except Exception:
        pass  # Zoom không được cũng không sao, người dùng bấm Home


