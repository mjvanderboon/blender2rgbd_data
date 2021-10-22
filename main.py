import bpy
import os
import sys
import numpy as np
import mathutils
import math
import shutil

# Make python able to import from scripts in current working directory # TODO: fix this with __init__
dir = os.getcwd()
if not dir in sys.path:
    sys.path.append(dir)
from utils import *

idx = 0

bpy.context.scene.render.use_compositing = True
bpy.context.scene.use_nodes = True

# Output directory
OUTPUT_DIR = os.path.join(os.getcwd(), 'output')
GT_IMAGE = 'output/Image0076.png'

# Scene objects
cam = bpy.data.objects['Camera']
obj = bpy.data.objects['FaceTS_OBJ']
hmd = bpy.data.objects['HMD']

def render_scene_handler(*args, **kwargs):
    """
    Handler that runs on render completion to start new render. The scene can
    be randomized here for different objects location, lighting, etc.

    :param args:
    :param kwargs:
    :return:
    """
    global idx, cam, obj

    scene = bpy.context.scene
    render = scene.render

    x, y, z = np.random.uniform(-math.pi / 8, math.pi / 8, 3)
    rotate_obj_euler(obj, x, y, z)
    rotate_obj_euler(hmd, x, y, z)

    # Render image
    print(f'########## RENDERING FILE: {idx} ##############')
    render.image_settings.file_format = 'PNG'
    render.filepath = os.path.join(OUTPUT_DIR, 'rgb', f'{idx}.png')
    idx += 1
    bpy.ops.render.render(write_still=True)


def save_semseg_handler(*args, **kwargs):
    """ Save the previously rendered semantic segmentation image to correct file. """
    global idx
    # Copy ground truth image
    dst_file = os.path.join(OUTPUT_DIR, 'gt', f'{idx - 1}.png')
    shutil.copy(GT_IMAGE, dst_file)

    print(f'########## SAVED GT FILE: {idx - 1} ##############')

bpy.app.handlers.render_complete.append(render_scene_handler)
bpy.app.handlers.render_post.append(save_semseg_handler)
render_scene_handler()