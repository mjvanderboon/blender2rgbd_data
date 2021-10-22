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
scene = bpy.context.scene
render = scene.render

# Output directory
OUTPUT_DIR = os.path.join(os.getcwd(), 'output')
GT_IMAGE = 'output/Image0000.png'
BACKGROUND_DIR = 'C:\data\indoorCVPR_09\Images\meeting_room'

# Scene objects
cam = bpy.data.objects['Camera']
head = bpy.data.objects['FaceTS_OBJ']
hmd = bpy.data.objects['HMD']
scene_lights = [obj for obj in scene.objects if obj.type == 'LIGHT']
print(scene_lights)
# Dataset of background images
background_images = [os.path.join(BACKGROUND_DIR, file) for file in os.listdir(BACKGROUND_DIR)]


def render_scene_handler(*args, **kwargs):
    """
    Handler that runs on render completion to start new render. The scene can
    be randomized here for different objects location, lighting, etc.

    :param args:
    :param kwargs:
    :return:
    """
    global idx, cam

    scene = bpy.context.scene
    render = scene.render

    # Randomize head pose and color
    randomize_head_pose(head, hmd)
    bpy.data.materials["Face"].node_tree.nodes["Mix"].inputs["Fac"].default_value = np.random.uniform(0.2, 1)
    bpy.data.materials["hmd"].node_tree.nodes["Mix"].inputs["Fac"].default_value = np.random.uniform(0., 0.1)

    # Randomize background
    bg = np.random.choice(background_images)
    bpy.data.images["08.jpg"].filepath = bg

    # Randomize lighting
    for light in scene_lights:
        light.data.node_tree.nodes['Emission'].inputs['Color'].default_value = random_color(min=100., max=200.)
        light.data.node_tree.nodes['Emission'].inputs['Strength'].default_value = np.random.uniform(0., 0.1)

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

    print(f'########## SAVED GROUND TRUTH FILE: {idx - 1} ##############')

bpy.app.handlers.render_complete.append(render_scene_handler)
bpy.app.handlers.render_post.append(save_semseg_handler)
render_scene_handler()