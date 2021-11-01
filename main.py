import bpy
import os
import sys
import numpy as np
import mathutils
import math
import shutil
from bpy.app.handlers import persistent

# Make python able to import from scripts in current working directory # TODO: fix this with __init__
dir = os.getcwd()
if not dir in sys.path:
    sys.path.append(dir)
from utils import *

bpy.context.preferences.addons["cycles"].preferences.get_devices()

# Set blender settings
bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "CUDA"
bpy.context.scene.cycles.device = "GPU"

print('Cycles compute device data (should be CUDA)')
print(bpy.context.preferences.addons["cycles"].preferences.compute_device_type)

print('All devices:')
for d in bpy.context.preferences.addons["cycles"].preferences.devices:
    print(d["name"], str(d["use"]))


# Set blender scene parameters
bpy.context.scene.render.use_compositing = True
bpy.context.scene.use_nodes = True
scene = bpy.context.scene
scene.cycles.device = "GPU"
render = scene.render

# Output directory
OUTPUT_DIR = os.path.join(os.getcwd(), 'HmdSegmentation')
if os.path.exists(OUTPUT_DIR) and os.path.isdir(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.mkdir(OUTPUT_DIR)
SAVE_DIRECTORY = ''

GT_IMAGE = os.path.join(os.getcwd(), 'HmdSegmentation', 'Image0000.png')
BACKGROUND_DIR = os.path.join(os.pardir, 'indoorCVPR_09', 'Images', 'meeting_room') # TODO: add arg/yml for this
#GT_IMAGE = 'HmdSegmentation/Image0000.png'
#BACKGROUND_DIR = 'C:\data\indoorCVPR_09\Images\meeting_room'

# Scene objects
cam = bpy.data.objects['Camera']
head = bpy.data.objects['FaceTS_OBJ']
hmd = bpy.data.objects['HMD']
scene_lights = [obj for obj in scene.objects if obj.type == 'LIGHT']
print(scene_lights)
# Dataset of background images
background_images = [os.path.join(BACKGROUND_DIR, file) for file in os.listdir(BACKGROUND_DIR)]


def randomize_scene_handler(*args, **kwargs):
    """
    Handler that runs on render completion to start new render. The scene can
    be randomized here for different objects location, lighting, etc.

    :param args:
    :param kwargs:
    :return:
    """

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


def save_semseg_handler(*args, **kwargs):
    dst_file = os.path.join(SAVE_DIRECTORY, 'labels', f'{idx}.png')
    os.makedirs(os.path.dirname(dst_file), exist_ok=True)  # Create directory if it doesn't already exist
    shutil.copy(GT_IMAGE, dst_file)
    print(f'########## SAVED GROUND TRUTH FILE: {idx} ##############')


bpy.app.handlers.render_complete.append(randomize_scene_handler)
bpy.app.handlers.render_post.append(save_semseg_handler)

NR_OF_RENDERS = 40000

for idx in range(NR_OF_RENDERS):
    scene = bpy.context.scene
    render = scene.render

    # Set dataset split
    SAVE_DIRECTORY = os.path.join(OUTPUT_DIR, get_split_dir(idx))

    # Render image
    print(f'########## RENDERING FILE: {idx} ##############')
    render.image_settings.file_format = 'PNG'
    render.filepath = os.path.join(SAVE_DIRECTORY, 'images', f'{idx}.png')
    bpy.ops.render.render(write_still=True)
    idx += 1
