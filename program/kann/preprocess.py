#
# Prepare temporary KaNN input by concatenating several images.
#
# Developer(s):
# - Anton Lokhmotov, dividiti, 2017
#

import glob
import os
import shutil
import subprocess


def ck_preprocess(i):

    ck=i['ck_kernel']
    deps=i['deps']
    env=i['env']

    # Get the maximum number of images.
    max_num_images=int(env.get('CK_KANN_MAX_NUMBER_IMAGES', 1))

    # Create temporary input using random max_num_images from the kann-val dataset.
    # TODO: Use images with consecutive numbering?
    imagenet_val=deps['kanndataset']
    imagenet_val_dir=imagenet_val['dict']['env']['CK_ENV_DATASET_IMAGENET_VAL_KANN']
    imagenet_val_files=glob.glob(imagenet_val_dir+'/ILSVRC2012_val_*.kann_input')

    kann_input_file=os.path.join(os.getcwd(), 'tmp-kann-input.tmp')
    kann_paths_file=os.path.join(os.getcwd(), 'tmp-kann-paths.tmp')
    with open(kann_input_file, 'wb') as kann_input_f, open(kann_paths_file, 'w') as kann_paths_f:
        num_images = 0
        for imagenet_val_file in imagenet_val_files:
            with open(imagenet_val_file, 'rb') as imagenet_val_f:
                shutil.copyfileobj(imagenet_val_f, kann_input_f)
            kann_paths_f.write(os.path.basename(imagenet_val_file) + '\n')
            num_images += 1
            if num_images >= max_num_images: break

    b=''
    return {'return':0, 'bat':b}

# Do not add anything here!
