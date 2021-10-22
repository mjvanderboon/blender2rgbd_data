# Blender2rgb
A tool to generate rgb datasets for semantic segmentation from Blender scenes.

## Installation
Adjust the path to the Blender executable in render_dataset.sh. Run the command to generate a dataset of rgb and ground 
truth images in the output folder. Please see `main.py` for more details on the dataset generation. Inspect the dataset
using `img_utils.py`.

# IMPORTANT
Due to the naming convention blender uses the ground truth image is saved as {Image}{blender frame number}. By default
this is Image0000.png'. Changing the frame number in blender will change the name of this file and break the saving. 
The Blender API does not seem to have access to the full save path, unfortunately.