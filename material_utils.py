"""
    Adapted from https://github.com/DIYer22/bpycv/
"""

import boxx
from boxx import *
from boxx import listdir, pathjoin

import bpy
import random

from .utils import encode_inst_id
from statu_recover import StatuRecover
from .node_graph import activate_node_tree, Node



class set_inst_material(StatuRecover):
    def __init__(self):
        StatuRecover.__init__(self)

        self.set_attr(bpy.data.worlds[0], "use_nodes", False)
        objs = [obj for obj in bpy.data.objects if obj.type in ("MESH", "CURVE")]
        for obj_idx, obj in enumerate(objs):
            inst_id = obj.get("inst_id", 0)  # default inst_id is 0
            color = tuple(encode_inst_id.id_to_rgb(inst_id)) + (1,)

            material_name = "auto.inst_material." + obj.name
            material = bpy.data.materials.new(material_name)
            material["is_auto"] = True
            material.use_nodes = True
            material.node_tree.nodes.clear()
            with activate_node_tree(material.node_tree):
                Node("ShaderNodeOutputMaterial").Surface = Node(
                    "ShaderNodeEmission", Color=color
                ).Emission

            self.replace_collection(obj.data.materials, [material])
