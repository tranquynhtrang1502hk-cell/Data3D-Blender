
# pylint: disable=import-error,no-member,invalid-name

"""
Hiển thị giao diện: bảng Data3D ở thanh bên khung 3D (nhấn N để mở).
"""

import bpy


class DATA3D_PT_panel(bpy.types.Panel):
    bl_label = "Data3D"
    bl_idname = "DATA3D_PT_panel"
    bl_space_type = 'VIEW_3D'     
    bl_region_type = 'UI'       
    bl_category = "Data3D"        

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        # Nhóm 1: dữ liệu và loại biểu đồ
        box = layout.box()
        box.label(text="Dữ liệu", icon='FILE')
        box.prop(scn, "data3d_path")
        box.prop(scn, "data3d_type")

        # Nhóm 2: kích thước
        box = layout.box()
        box.label(text="Kích thước", icon='MOD_ARRAY')
        box.prop(scn, "data3d_spacing")
        box.prop(scn, "data3d_width")
        box.prop(scn, "data3d_height")

        # Nhóm 3: nhãn chữ
        box = layout.box()
        box.label(text="Nhãn", icon='FONT_DATA')
        box.prop(scn, "data3d_labels")
        if scn.data3d_labels:
            box.prop(scn, "data3d_font")

        # Nhóm 4: hoạt họa (chỉ hiện chi tiết khi bật)
        box = layout.box()
        box.label(text="Hoạt họa", icon='PLAY')
        box.prop(scn, "data3d_animate")
        if scn.data3d_animate:
            box.prop(scn, "data3d_duration")
            box.prop(scn, "data3d_stagger")

        # Nút chính
        layout.separator()
        layout.operator("data3d.create_chart", icon='ADD')
        layout.operator("data3d.clear_chart", icon='TRASH')

        # Nhóm 5: xuất ảnh
        box = layout.box()
        box.label(text="Xuất ảnh", icon='RENDER_STILL')
        box.prop(scn, "data3d_out_path")
        box.operator("data3d.render_image", icon='RENDER_STILL')


def register():
    bpy.utils.register_class(DATA3D_PT_panel)


def unregister():
    bpy.utils.unregister_class(DATA3D_PT_panel)