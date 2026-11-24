
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


# ---- Hàm tạo hoạt họa (keyframe) ----

def key_bar_grow(bar, h, f0, f1):
    """Cột mọc từ đáy: animate cả chiều cao và vị trí z (vì tâm ở giữa khối)."""
    bar.scale.z = 0.001
    bar.location.z = 0.0005
    bar.keyframe_insert("scale", index=2, frame=f0)
    bar.keyframe_insert("location", index=2, frame=f0)
    bar.scale.z = h
    bar.location.z = h / 2
    bar.keyframe_insert("scale", index=2, frame=f1)
    bar.keyframe_insert("location", index=2, frame=f1)


def key_rise(obj, z_end, f0, f1):
    """Nhãn trượt từ dưới lên vị trí cuối."""
    obj.location.z = 0
    obj.keyframe_insert("location", index=2, frame=f0)
    obj.location.z = z_end
    obj.keyframe_insert("location", index=2, frame=f1)


def key_pop(obj, f0, f1):
    """Đối tượng phóng to từ gần 0 lên kích thước hiện tại."""
    final = obj.scale.copy()
    obj.scale = (0.001, 0.001, 0.001)
    obj.keyframe_insert("scale", frame=f0)
    obj.scale = final
    obj.keyframe_insert("scale", frame=f1)



# =====================================================================
# 2. HÀM DỰNG BIỂU ĐỒ
# =====================================================================

def build_bar_chart(scn, data, col, font):
    """Dựng biểu đồ cột. Trả về khung hình cuối của hoạt họa."""
    gap = scn.data3d_spacing
    width = scn.data3d_width
    hscale = scn.data3d_height
    values = [d[1] for d in data]
    vmin, vmax = min(values), max(values)
    last_frame = 1

    for i, (name, value, emoji) in enumerate(data):
        h = max(value * hscale, 0.01)               # Tránh cột cao 0
        t = (value - vmin) / (vmax - vmin) if vmax > vmin else 0.5
        x = i * gap

        # Tạo cột: khối vuông cạnh 1, kéo giãn theo (rộng, rộng, cao)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, h / 2))
        bar = bpy.context.active_object
        bar.scale = (width, width, h)
        bar.name = name
        bar.data.materials.append(make_material("D3D_" + name, gradient(t)))
        move_to_col(bar, col)

        # Nhãn: tên ở chân cột, giá trị (kèm emoji) trên đỉnh cột
        value_label = None
        if scn.data3d_labels:
            add_label(name, (x, -width, -0.8), 0.45, col, font)
            text = f"{emoji} {value:g}".strip()
            value_label = add_label(text, (x, 0, h + 0.3), 0.6, col, font)

        # Hoạt họa: mỗi cột bắt đầu trễ hơn cột trước một chút
        if scn.data3d_animate:
            f0 = 1 + i * scn.data3d_stagger
            f1 = f0 + scn.data3d_duration
            key_bar_grow(bar, h, f0, f1)
            if value_label:
                key_rise(value_label, h + 0.3, f0, f1)
            last_frame = f1

    return last_frame


def build_line_chart(scn, data, col, font):
    """Dựng biểu đồ đường: quả cầu tại mỗi điểm, nối bằng khối trụ."""
    gap = scn.data3d_spacing
    hscale = scn.data3d_height
    r = scn.data3d_width * 0.25                     
    values = [d[1] for d in data]
    vmin, vmax = min(values), max(values)
    last_frame = 1

    points = []  
    ts = []    
    f_ends = []   

    for i, (name, value, emoji) in enumerate(data):
        h = value * hscale
        t = (value - vmin) / (vmax - vmin) if vmax > vmin else 0.5
        p = Vector((i * gap, 0, h))
        points.append(p)
        ts.append(t)

        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=p)
        dot = bpy.context.active_object
        dot.name = name
        dot.data.materials.append(make_material("D3D_" + name, gradient(t)))
        move_to_col(dot, col)

        value_label = None
        if scn.data3d_labels:
            add_label(name, (p.x, -r, -0.8), 0.45, col, font)
            text = f"{emoji} {value:g}".strip()
            value_label = add_label(text, (p.x, 0, h + r + 0.4), 0.6, col, font)

        f0 = 1 + i * scn.data3d_stagger
        f1 = f0 + scn.data3d_duration
        f_ends.append(f1)
        if scn.data3d_animate:
            key_pop(dot, f0, f1)
            if value_label:
                key_pop(value_label, f0, f1)
            last_frame = f1

    