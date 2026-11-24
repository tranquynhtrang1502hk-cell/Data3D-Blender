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
