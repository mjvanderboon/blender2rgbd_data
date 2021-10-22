import bpy
import os
import sys
import numpy as np
import mathutils
import math

def random_color(min=0., max=255.):
    return np.random.uniform(min, max, 3).tolist() + [255.]

def randomize_head_pose(head, hmd):
    x, y, z = np.random.uniform(-math.pi / 4, math.pi / 4, 3)
    rotate_obj_euler(head, x, y, z)
    rotate_obj_euler(hmd, x, y, z)


def rotate_obj_euler(obj, x, y, z):
    # rotate around global Z-axis
    obj.rotation_mode = 'XYZ'
    obj.rotation_euler = (np.pi/2 + x, y, z)


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


def sample_spherical_uniform_angles(n, min_pitch=-90, radius=1., radius_range=0):
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
