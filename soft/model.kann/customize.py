#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Anton Lokhmotov, dividiti, 2017
#

import os

##############################################################################
# setup environment setup

def setup(i):
    """
    Input:  {
              cfg              - meta of this soft entry
              self_cfg         - meta of module soft
              ck_kernel        - import CK kernel module (to reuse functions)

              host_os_uoa      - host OS UOA
              host_os_uid      - host OS UID
              host_os_dict     - host OS meta

              target_os_uoa    - target OS UOA
              target_os_uid    - target OS UID
              target_os_dict   - target OS meta

              target_device_id - target device ID (if via ADB)

              tags             - list of tags used to search this entry

              env              - updated environment vars from meta
              customize        - updated customize vars from meta

              deps             - resolved dependencies for this soft

              interactive      - if 'yes', can ask questions, otherwise quiet
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
            }

    """

    import os

    # Get variables
    ck=i['ck_kernel']
    s=''

    iv=i.get('interactive','')

    cus=i.get('customize',{})
    fp=cus.get('full_path','')

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    sdirs=hosd.get('dir_sep','')

    # Check platform
    hplat=hosd.get('ck_name','')

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    remote=tosd.get('remote','')
    tbits=tosd.get('bits','')

    env=i['env']
    ep=cus.get('env_prefix','')

	# Example: KaNN_Evaluation_Package_v1.2/SqueezeNetv11_imagenet/bin/multibin_bin.mpk
    bin_dir=os.path.dirname(fp)
    model_dir=os.path.dirname(bin_dir)
    # Files under model_dir.
    env[ep]=model_dir
    env[ep+'MODEL_DIR']=model_dir
    env[ep+'IMAGENET_CLASSES']=os.path.join(model_dir, 'imagenet-classes.txt')
    env[ep+'INPUT_PREPARATOR']=os.path.join(model_dir, 'input_preparator.py')
    env[ep+'PARAMS_BIN']=os.path.join(model_dir, 'params.bin')
    # Files under bin_dir.
    env[ep+'BIN_DIR']=bin_dir
    env[ep+'HOST_BIN']=os.path.join(bin_dir, 'host_bin')
    env[ep+'MULTIBIN_BIN']=fp

    return {'return':0, 'bat':s}
