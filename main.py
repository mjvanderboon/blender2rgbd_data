import bpy
import os
import sys
import numpy as np
import mathutils
import math

def point_at(obj, target, roll=0):
    """
    Rotate obj to look at target
    :arg obj: the object to be rotated. Usually the camera
    :arg target: the location (3-tuple or Vector) to be looked at
    :arg roll: The angle of rotation about the axis from obj to target in radians.
    Based on: https://blender.stackexchange.com/a/5220/12947 (ideasman42)    """
    if not isinstance(target, mathutils.Vector):
        target = mathutils.Vector(target)
    loc = obj.location
    # direction points from the object to the target
    direction = target - loc

    quat = direction.to_track_quat('-Z', 'Y')

    # /usr/share/blender/scripts/addons/add_advanced_objects_menu/arrange_on_curve.py
    quat = quat.to_matrix().to_4x4()
    rollMatrix = mathutils.Matrix.Rotation(roll, 4, 'Z')

    # remember the current location, since assigning to obj.matrix_world changes it
    loc = loc.to_tuple()
    # obj.matrix_world = quat * rollMatrix
    # in blender 2.8 and above @ is used to multiply matrices
    # using * still works but results in unexpected behaviour!
    obj.matrix_world = quat @ rollMatrix
    obj.location = loc


def sample_sherical_uniform_angles(n, min_pitch=30, radius=1., radius_range=0):
    yaw = np.random.uniform(-math.pi, math.pi, n)
    pitch = np.random.uniform(math.radians(min_pitch), math.radians(90), n)
    radius = np.random.uniform(-radius_range, radius_range, n) + radius

    x = np.sin(yaw) * np.cos(pitch)
    z = np.sin(pitch)
    y = np.cos(yaw) * np.cos(pitch)

    x = np.expand_dims(x, axis=1)
    y = np.expand_dims(y, axis=1)
    z = np.expand_dims(z, axis=1)

    return np.concatenate((x, y, z), axis=1) * np.expand_dims(radius, axis=1)


idx = 0
cam = bpy.data.objects['Camera']
obj = bpy.data.objects['FaceTS_OBJ']

def my_handler(*args, **kwargs):
    global idx, cam, obj
    idx += 1

    xyz = sample_sherical_uniform_angles(2, min_pitch=30, radius=10.)[0]
    cam.location = xyz
    point_at(cam, obj.location)
    filepath = f"c:/Users/boonmjvd/Desktop/{idx}.png"

    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)

    print('#####################################################################################')
    print(f'########## RENDERED FILE: {idx} ##############')
    bpy.ops.render.render()

bpy.app.handlers.render_complete.append(my_handler)
my_handler()