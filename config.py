"""
    Adapted from https://raw.githubusercontent.com/mcordts/cityscapesScripts/master/cityscapesscripts/helpers/labels.py
    Edited by:
"""

from collections import namedtuple


Label = namedtuple('Label', [
    'name',    # The identifier of this label, e.g. 'car', 'person', ... .
    'id',       # An integer ID that is associated with this label.
                # The IDs are used to represent the label in ground truth images
                # An ID of -1 means that this label does not have an ID and thus
                # is ignored when creating ground truth images (e.g. license plate).
                # Do not modify these IDs, since exactly these IDs are expected by the
                # evaluation server.
    'color',
    'ignoreInEval',

])

labels = [
    #       name            id      color       ignoreInEval
    Label(  'unlabeled',    0,     (0, 0, 0),   True),
    Label(  'face',         1,     (255, 0, 0), True),
    Label(  'hmd',          2,     (0, 0, 255), True)
]

# Create dictionaries for a fast lookup

# Please refer to the main method below for example usages!

# name to label object
name2label      = { label.name    : label for label in labels           }
# id to label object
id2label        = { label.id      : label for label in labels           }