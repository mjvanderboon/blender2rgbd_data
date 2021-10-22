import bpy
import os
import sys
import numpy as np
import mathutils
import math


# Make python able to import from scripts in current working directory
dir = os.getcwd()
if not dir in sys.path:
    sys.path.append(dir)
from utils import *

idx = 0
GT_render_pass = False

bpy.context.scene.render.use_compositing = True
bpy.context.scene.use_nodes = True

# Output directory
OUTPUT_DIR = 'C:/dev/mesh2rgbd_dataset_generation/output'
subfolder = {
    True: 'rgb',
    False: 'gt'
}

# Scene objects
cam = bpy.data.objects['Camera']
obj = bpy.data.objects['FaceTS_OBJ']
hmd = bpy.data.objects['HMD']

# Scene nodes
rl_node = bpy.data.scenes['Scene'].node_tree.nodes["Render Layers"]
composite_node = bpy.data.scenes['Scene'].node_tree.nodes["Composite"]
semseg_node = bpy.data.scenes['Scene'].node_tree.nodes["Math"]

def my_handler(*args, **kwargs):
    global idx, cam, obj, GT_render_pass

    scene = bpy.context.scene
    render = scene.render
    node_tree = scene.node_tree

    if GT_render_pass:
        print('GT render pass')
        GT_render_pass = False
        render.image_settings.color_mode = "BW"
        render.image_settings.save_as_render = False
        node_tree.links.new(semseg_node.outputs["Value"], composite_node.inputs["Image"])
    else:
        print('RGB render pass')
        idx += 1
        GT_render_pass = True
        render.image_settings.color_mode = "RGB"
        render.image_settings.save_as_render = True
        node_tree.links.new(rl_node.outputs["Image"], composite_node.inputs["Image"])

        x, y, z = np.random.uniform(-math.pi / 8, math.pi / 8, 3)
        rotate_obj_euler(obj, x, y, z)
        rotate_obj_euler(hmd, x, y, z)

    # Render image
    render.image_settings.file_format = 'PNG'
    render.filepath = os.path.join(OUTPUT_DIR, subfolder[GT_render_pass], f'{idx}.png')
    bpy.ops.render.render(write_still=True)

    print('#####################################################################################')
    print(f'########## RENDERED FILE: {idx} ##############')
    print('#####################################################################################')


bpy.app.handlers.render_complete.append(my_handler)
my_handler()