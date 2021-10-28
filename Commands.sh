# Run local blender render
C:\Users\boonmjvd\AppData\Local\Microsoft\AppV\Client\Integration\6BB3246B-25D3-457C-BC2F-A7C6E871088F\Root\blender.exe hmd_male_composite.blend --background --python main.py


# Connect to gcloud instance
gcloud beta compute ssh --zone "europe-west4-b" "blender-render"  --project "prime-pod-327819"

# scp from local to remote
gcloud compute scp --recurse .\blender2rgb_data\ boonmjvd@blender-render:blender2rgb_data/

# scp from remote to local
gcloud compute scp --recurse boonmjvd@blender-render:blender2rgb_data/output ./blender2rgb_data/

# Download and install Blender
 wget 'https://download.blender.org/release/Blender2.91/blender-2.91.2-linux64.tar.xz'
 tar -vxf blender-2.91.2-linux64.tar.xz

# Install necessary libraries
sudo apt-get update
sudo apt install libboost-all-dev
sudo apt install libgl1-mesa-dev

# Download background image dataset
wget http://groups.csail.mit.edu/vision/LabelMe/NewImages/indoorCVPR_09.tar
tar -vxf indoorCVPR_09.tar

# TODO: make this from the get go.
cd blender2rgb_data/data
mkdir indoorCVPR_09
cd ../..
mv Images/ blender2rgb_data/data/indoorCVPR_09

# [IMPORTANT]
# Change blend file stetings to render on gpu

#Instal nvidia-drivers 460 / CUDA on remote (installation script from gcp)
wget https://raw.githubusercontent.com/GoogleCloudPlatform/compute-gpu-installation/main/linux/install_gpu_driver.py --output install_gpu_driver.py
sudo python3 install_gpu_driver.py


# Run remote blender render (from blender2rgb_data folder)
sudo ~/blender-2.91.2-linux64/blender -b hmd_male_composite.blend --python main.py