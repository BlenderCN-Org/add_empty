import bpy
import mathutils
import bmesh

bl_info = {
    "name": "Add Empty",
    "category": "Edit > Add > Add Empty",
}


class AddEmpty(bpy.types.Operator):
    """Add Empty"""
    bl_idname = "object.add_empty"
    bl_label = "Add Empty"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if (bpy.context.object.mode == 'EDIT'):
            return True
        else:
            return False

    def execute(self, context):
        o = bpy.data.objects.new("bone_empty", None)
        bpy.context.scene.objects.link(o)
        o.empty_draw_size = 0.5
        o.empty_draw_type = 'PLAIN_AXES'

        mesh = bpy.context.object.data
        # selected_verts = list(filter(lambda v: v.select, mesh.vertices))

        bm = bmesh.from_edit_mesh(bpy.context.object.data)
        selected_verts = list(filter(lambda v: v.select, bm.verts))

        result = mathutils.Vector((0,0,0))
        for v in selected_verts:
            result = result + v.co

        result = result / len(selected_verts)

        mat_world = bpy.context.object.matrix_world

        result = mat_world * result

        print(result)

        o.location = result

        return {'FINISHED'}


# for menu to draw
# You can change this to Lambda
def menu_draw(self, context):
    self.layout.operator("object.add_empty")


# registering class and menu
def register():
    bpy.utils.register_class(AddEmpty)
    bpy.types.INFO_MT_mesh_add.append(menu_draw)
    # bpy.types.VIEW3D_MT_object_specials.append(menu_draw)
    # bpy.types.VIEW3D_PT_tools_add_mesh_edit.append(menu_drAAaw)


# Unregistering class and menu
def unregister():
    bpy.utils.unregister_class(AddEmpty)
    bpy.types.INFO_MT_mesh_add.remove(menu_draw)
    # bpy.types.VIEW3D_MT_object_specials.remove(menu_draw)


# Debug ---------------------------------------------------------------------
debug = 0
if debug == 1:
    try:
        unregister()
    except:
        pass
    finally:
        register()
# ---------------------------------------------------------------------------