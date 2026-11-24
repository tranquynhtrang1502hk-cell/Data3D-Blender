# pylint: disable=import-error,no-member,invalid-name

"""
Các thuộc tính (property) lưu lựa chọn của người dùng.
Gắn vào bpy.types.Scene nên được lưu cùng file .blend.
"""

import bpy
from bpy.props import (
    StringProperty,
    FloatProperty,
    IntProperty,
    BoolProperty,
    EnumProperty,
)

# Danh sách tên thuộc tính, dùng để xóa gọn khi unregister
_TEN_THUOC_TINH = (
    "data3d_path", "data3d_type", "data3d_spacing", "data3d_width",
    "data3d_height", "data3d_labels", "data3d_font", "data3d_animate",
    "data3d_duration", "data3d_stagger", "data3d_out_path",
)


def register():
    S = bpy.types.Scene

    # --- Dữ liệu vào ---
    S.data3d_path = StringProperty(
        name="File CSV",
        description="Chọn file CSV có cột name, value (và emoji nếu muốn)",
        subtype='FILE_PATH',
        default="",
    )

    # --- Loại biểu đồ ---
    S.data3d_type = EnumProperty(
        name="Loại",
        description="Chọn kiểu biểu đồ",
        items=[
            ('BAR', "Cột", "Biểu đồ cột 3D"),
            ('LINE', "Đường", "Biểu đồ đường 3D"),
        ],
        default='BAR',
    )

    # --- Kích thước ---
    S.data3d_spacing = FloatProperty(
        name="Khoảng cách", description="Khoảng cách giữa các cột/điểm",
        default=2.0, min=0.5, max=10.0)
    S.data3d_width = FloatProperty(
        name="Độ rộng", description="Độ rộng cột (hoặc kích thước điểm)",
        default=1.0, min=0.1, max=5.0)
    S.data3d_height = FloatProperty(
        name="Tỉ lệ chiều cao", description="Nhân chiều cao với hệ số này",
        default=1.0, min=0.1, max=10.0)
    
    # --- Nhãn chữ ---
    S.data3d_labels = BoolProperty(
        name="Hiện nhãn", description="Hiện tên và giá trị", default=True)
    S.data3d_font = StringProperty(
        name="Font",
        description="Tùy chọn: file font .ttf/.otf (để hiện tiếng Việt, emoji)",
        subtype='FILE_PATH',
        default="",
    )

    # --- Hoạt họa ---
    S.data3d_animate = BoolProperty(
        name="Hoạt họa", description="Cột/điểm xuất hiện lần lượt", default=False)
    S.data3d_duration = IntProperty(
        name="Số khung mỗi cột", description="Thời gian một cột mọc lên",
        default=30, min=5, max=200)
    S.data3d_stagger = IntProperty(
        name="Trễ giữa các cột", description="Khoảng trễ giữa hai cột liên tiếp",
        default=8, min=0, max=60)

    # --- Xuất ảnh ---
    S.data3d_out_path = StringProperty(
        name="Ảnh xuất",
        description="Nơi lưu ảnh (// = cạnh file .blend, cần lưu file trước)",
        subtype='FILE_PATH',
        default="//data3d_chart.png",
    )


def unregister():
    for ten in _TEN_THUOC_TINH:
        if hasattr(bpy.types.Scene, ten):
            delattr(bpy.types.Scene, ten)
            
            
            
            
