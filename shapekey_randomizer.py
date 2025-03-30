import bpy
import random
from bpy.props import StringProperty, FloatProperty, BoolProperty, CollectionProperty
from bpy.types import Operator, Panel, PropertyGroup
from bpy.app.handlers import persistent

bl_info = {
    "name": "Shape Key Randomizer",
    "author": "Harrisoned",
    "version": (0, 0, 5),
    "blender": (4, 2, 0),
    "location": "Object Properties > Shape Key Randomizer Panel",
    "description": "Randomly creates keyframes for the selected shape keys based on specified parameters.",
    "warning": "",
    "doc_url": "",
    "category": "Animation",
}

def set_shapekey_keyframe(obj, shapekey_name, value, frame):
    if obj.data.shape_keys and shapekey_name in obj.data.shape_keys.key_blocks:
        sk = obj.data.shape_keys.key_blocks[shapekey_name]
        sk.value = value
        sk.keyframe_insert("value", frame=frame)

@persistent
def update_shapekeys(scene):
    for obj in bpy.data.objects:
        if not obj.get("shapekey_randomizer_running", False):
            continue
        
        for sk in obj.shapekey_randomizer:
            if not sk.enabled:
                continue
            
            frame = scene.frame_current
            interval = random.randint(int(sk.min_interval * scene.render.fps), int(sk.max_interval * scene.render.fps))
            duration = int(sk.act_duration * scene.render.fps)
            in_speed = int(sk.act_in_speed * scene.render.fps)
            out_speed = int(sk.act_out_speed * scene.render.fps)
            
            if frame % interval == 0:
                set_shapekey_keyframe(obj, sk.shapekey_name, sk.min_value, frame)
                set_shapekey_keyframe(obj, sk.shapekey_name, sk.max_value, frame + in_speed)
                set_shapekey_keyframe(obj, sk.shapekey_name, sk.max_value, frame + in_speed + duration)
                set_shapekey_keyframe(obj, sk.shapekey_name, sk.min_value, frame + in_speed + duration + out_speed)

class ShapekeyRandomizerProperty(PropertyGroup):
    shapekey_name: StringProperty(name="Shapekey Name")
    min_interval: FloatProperty(name="Min Interval", default=1.0, min=0.1)
    max_interval: FloatProperty(name="Max Interval", default=3.0, min=0.1)
    act_duration: FloatProperty(name="Duration", default=0.1, min=0.1)
    act_in_speed: FloatProperty(name="In Speed", default=0.15, min=0.01)
    act_out_speed: FloatProperty(name="Out Speed", default=0.15, min=0.01)
    max_value: FloatProperty(name="Max Value", default=1.0, min=0, max=1.0)
    min_value: FloatProperty(name="Min Value", default=0, min=0, max=1.0)
    enabled: BoolProperty(name="Enabled", default=True)

class OBJECT_PT_ShapeKeyRandomizer(Panel):
    bl_label = "Shapekey Randomizer"
    bl_idname = "OBJECT_PT_shapekey_randomizer"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if not obj or not obj.data.shape_keys:
            layout.label(text="No shapekeys found!")
            return

        row = layout.row()
        row.operator("shapekey.select_randomizer")
        
        for index, sk in enumerate(obj.shapekey_randomizer):
            box = layout.box()
            box.prop(sk, "shapekey_name")
            box.prop(sk, "min_interval")
            box.prop(sk, "max_interval")
            box.prop(sk, "act_duration")
            box.prop(sk, "act_in_speed")
            box.prop(sk, "act_out_speed")
            box.prop(sk, "max_value")
            box.prop(sk, "min_value")
            box.prop(sk, "enabled")
            box.operator("shapekey.remove_randomizer", text="Remove").index = index
        
        layout.operator("shapekey.start_randomizer")
        layout.operator("shapekey.stop_randomizer")

class SHAPEKEY_OT_RemoveRandomizer(Operator):
    bl_idname = "shapekey.remove_randomizer"
    bl_label = "Remove Shapekey Randomizer"
    index: bpy.props.IntProperty()

    def execute(self, context):
        obj = context.object
        if obj and 0 <= self.index < len(obj.shapekey_randomizer):
            obj.shapekey_randomizer.remove(self.index)
        return {'FINISHED'}

class SHAPEKEY_OT_SelectRandomizer(Operator):
    bl_idname = "shapekey.select_randomizer"
    bl_label = "Select Shapekeys"

    def execute(self, context):
        obj = context.object
        if obj and obj.data.shape_keys:
            existing_names = {item.shapekey_name for item in obj.shapekey_randomizer}
            def draw_menu(self, context):
                layout = self.layout
                for sk in obj.data.shape_keys.key_blocks:
                    if sk.name not in existing_names:
                        op = layout.operator("shapekey.add_randomizer", text=sk.name)
                        op.shapekey_name = sk.name
            
            bpy.context.window_manager.popup_menu(draw_menu, title="Select Shapekeys", icon='SHAPEKEY_DATA')
        return {'FINISHED'}

class SHAPEKEY_OT_AddRandomizer(Operator):
    bl_idname = "shapekey.add_randomizer"
    bl_label = "Add Selected Shapekey"
    shapekey_name: StringProperty()

    def execute(self, context):
        obj = context.object
        if obj and self.shapekey_name:
            new_item = obj.shapekey_randomizer.add()
            new_item.shapekey_name = self.shapekey_name
        return {'FINISHED'}

class SHAPEKEY_OT_StartRandomizer(Operator):
    bl_idname = "shapekey.start_randomizer"
    bl_label = "Start Randomizer"

    def execute(self, context):
        obj = context.object
        if obj:
            obj["shapekey_randomizer_running"] = True
            if update_shapekeys not in bpy.app.handlers.frame_change_pre:
                bpy.app.handlers.frame_change_pre.append(update_shapekeys)
        return {'FINISHED'}

class SHAPEKEY_OT_StopRandomizer(Operator):
    bl_idname = "shapekey.stop_randomizer"
    bl_label = "Stop Randomizer"

    def execute(self, context):
        obj = context.object
        if obj:
            obj["shapekey_randomizer_running"] = False
        if update_shapekeys in bpy.app.handlers.frame_change_pre:
            bpy.app.handlers.frame_change_pre.remove(update_shapekeys)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ShapekeyRandomizerProperty)
    bpy.utils.register_class(OBJECT_PT_ShapeKeyRandomizer)
    bpy.utils.register_class(SHAPEKEY_OT_SelectRandomizer)
    bpy.utils.register_class(SHAPEKEY_OT_RemoveRandomizer)
    bpy.utils.register_class(SHAPEKEY_OT_AddRandomizer)
    bpy.utils.register_class(SHAPEKEY_OT_StartRandomizer)
    bpy.utils.register_class(SHAPEKEY_OT_StopRandomizer)
    bpy.types.Object.shapekey_randomizer = CollectionProperty(type=ShapekeyRandomizerProperty)

def unregister():
    bpy.utils.unregister_class(ShapekeyRandomizerProperty)
    bpy.utils.unregister_class(OBJECT_PT_ShapeKeyRandomizer)
    bpy.utils.unregister_class(SHAPEKEY_OT_SelectRandomizer)
    bpy.utils.unregister_class(SHAPEKEY_OT_RemoveRandomizer)
    bpy.utils.unregister_class(SHAPEKEY_OT_AddRandomizer)
    bpy.utils.unregister_class(SHAPEKEY_OT_StartRandomizer)
    bpy.utils.unregister_class(SHAPEKEY_OT_StopRandomizer)
    del bpy.types.Object.shapekey_randomizer
    if update_shapekeys in bpy.app.handlers.frame_change_pre:
        bpy.app.handlers.frame_change_pre.remove(update_shapekeys)

if __name__ == "__main__":
    register()
