
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




# 2. HÀM DỰNG BIỂU ĐỒ


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
    r = scn.data3d_width * 0.25                     # Bán kính điểm
    values = [d[1] for d in data]
    vmin, vmax = min(values), max(values)
    last_frame = 1

    points = []   # Vị trí các điểm
    ts = []       # Giá trị màu t của từng điểm
    f_ends = []   # Khung hình mỗi điểm xuất hiện xong

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

    # Nối hai điểm liền kề bằng một khối trụ
    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i + 1]
        v = p2 - p1
        bpy.ops.mesh.primitive_cylinder_add(
            radius=r * 0.5, depth=v.length, location=(p1 + p2) / 2)
        seg = bpy.context.active_object
        seg.name = f"Doan_{i + 1}"
        # Quay trục Z của khối trụ theo hướng từ p1 đến p2
        seg.rotation_mode = 'QUATERNION'
        seg.rotation_quaternion = v.to_track_quat('Z', 'Y')
        color = gradient((ts[i] + ts[i + 1]) / 2)
        seg.data.materials.append(make_material(f"D3D_doan_{i + 1}", color))
        move_to_col(seg, col)
        if scn.data3d_animate:
            f1 = f_ends[i + 1]
            key_pop(seg, f1 - scn.data3d_duration, f1)

    return last_frame


# =====================================================================
# 3. CÁC OPERATOR (NÚT BẤM)
# =====================================================================

class DATA3D_OT_create(bpy.types.Operator):
    """Đọc file CSV và dựng biểu đồ 3D"""
    bl_idname = "data3d.create_chart"
    bl_label = "Tạo biểu đồ"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene

        # --- Bước 1: kiểm tra và đọc dữ liệu ---
        if not scn.data3d_path:
            self.report({'ERROR'}, "Chưa chọn file CSV")
            return {'CANCELLED'}

        data, err = read_csv(bpy.path.abspath(scn.data3d_path))
        if err:
            self.report({'ERROR'}, err)
            return {'CANCELLED'}

        if any(v < 0 for _, v, _ in data):
            self.report({'ERROR'}, "Hiện chưa hỗ trợ giá trị âm")
            return {'CANCELLED'}

        if len(data) > MAX_ROWS:
            self.report({'WARNING'}, f"Dữ liệu có {len(data)} dòng, biểu đồ sẽ rất dài")

        # --- Bước 2: chuẩn bị cảnh ---
        # Thêm đối tượng cần đang ở Object Mode
        if context.object and context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        clear_chart()
        col = get_collection(scn)
        font = load_font(scn.data3d_font)

        # --- Bước 3: dựng biểu đồ theo loại đã chọn ---
        if scn.data3d_type == 'LINE':
            last_frame = build_line_chart(scn, data, col, font)
        else:
            last_frame = build_bar_chart(scn, data, col, font)

        # --- Bước 4: thiết lập thời gian hoạt họa ---
        if scn.data3d_animate:
            scn.frame_start = 1
            scn.frame_end = last_frame + 15
            scn.frame_set(1)

        bpy.ops.object.select_all(action='DESELECT')
        frame_view(context)
        self.report({'INFO'}, f"Đã tạo biểu đồ từ {len(data)} dòng dữ liệu")
        return {'FINISHED'}


class DATA3D_OT_clear(bpy.types.Operator):
    """Xóa biểu đồ do Data3D tạo ra"""
    bl_idname = "data3d.clear_chart"
    bl_label = "Xóa biểu đồ"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        clear_chart()
        self.report({'INFO'}, "Đã xóa biểu đồ")
        return {'FINISHED'}


class DATA3D_OT_render(bpy.types.Operator):
    """Đặt camera nhìn vào biểu đồ và xuất ảnh"""
    bl_idname = "data3d.render_image"
    bl_label = "Xuất ảnh"

    def execute(self, context):
        scn = context.scene
        col = bpy.data.collections.get(COL_NAME)
        if col is None or len(col.objects) == 0:
            self.report({'ERROR'}, "Chưa có biểu đồ, hãy bấm Tạo biểu đồ trước")
            return {'CANCELLED'}

        # Đường dẫn "//" cần file .blend đã được lưu
        if scn.data3d_out_path.startswith("//") and not bpy.data.filepath:
            self.report({'ERROR'}, "Hãy lưu file .blend trước, hoặc nhập đường dẫn đầy đủ")
            return {'CANCELLED'}

        # Đảm bảo có camera và đèn
        if scn.camera is None:
            cam_data = bpy.data.cameras.new("Data3D_Camera")
            cam = bpy.data.objects.new("Data3D_Camera", cam_data)
            scn.collection.objects.link(cam)
            scn.camera = cam
        cam = scn.camera

        if not any(o.type == 'LIGHT' for o in scn.objects):
            sun_data = bpy.data.lights.new("Data3D_Sun", 'SUN')
            sun = bpy.data.objects.new("Data3D_Sun", sun_data)
            scn.collection.objects.link(sun)
            sun.location = (0, -10, 10)
            sun.rotation_euler = (math.radians(50), 0, math.radians(15))

        # Tính khung bao quanh toàn bộ biểu đồ
        context.view_layer.update()
        xs, ys, zs = [], [], []
        for obj in col.objects:
            for corner in obj.bound_box:
                w = obj.matrix_world @ Vector(corner)
                xs.append(w.x); ys.append(w.y); zs.append(w.z)
        width = max(xs) - min(xs)
        height = max(zs) - min(zs)
        cx = (min(xs) + max(xs)) / 2
        cz = (min(zs) + max(zs)) / 2

        # Tính khoảng cách camera để thấy đủ biểu đồ
        cam.data.lens = 35
        tan_h = (cam.data.sensor_width / 2) / cam.data.lens
        aspect = scn.render.resolution_x / scn.render.resolution_y
        tan_v = tan_h / aspect
        dist = max((width / 2) / tan_h, (height / 2) / tan_v) * 1.3 + 2
        # Hệ số 1.3 là lề an toàn, tăng lên nếu biểu đồ bị cắt

        cam.location = (cx, min(ys) - dist, cz)
        cam.rotation_euler = (math.radians(90), 0, 0)
        cam.data.clip_end = max(1000, dist * 4)

        # Xuất ảnh
        scn.render.filepath = bpy.path.abspath(scn.data3d_out_path)
        scn.render.image_settings.file_format = 'PNG'
        bpy.ops.render.render(write_still=True)
        self.report({'INFO'}, f"Đã lưu ảnh: {scn.render.filepath}")
        return {'FINISHED'}


classes = (DATA3D_OT_create, DATA3D_OT_clear, DATA3D_OT_render)

