#
# Collective Knowledge - KaNN model setup.
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Anton Lokhmotov, dividiti, 2017
#

import os

##############################################################################
# setup environment

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

    # Get CK variables.
    ck=i['ck_kernel']
    env=i['env']

    cus=i.get('customize',{})
    fp=cus.get('full_path','')
    ep=cus.get('env_prefix','')

    # The generated files get copied under '$CK_ENV_MODEL_KANN_ROOT/generated'.
    generated_dir=os.path.dirname(fp)
    env[ep+'_INPUT_PREPARATOR']=os.path.join(generated_dir, 'input_preparator.py')
    env[ep+'_MULTIBIN_BIN']=os.path.join(generated_dir, 'multibin_bin.mpk')
    env[ep+'_PARAMS_BIN']=os.path.join(generated_dir, 'params.bin')
    env[ep+'_HOST_BIN']=os.path.join(generated_dir, 'host_bin')
    env[ep+'_IO_BIN']=os.path.join(generated_dir, 'io_bin')
    env[ep+'_ROOT']=os.path.dirname(generated_dir)

    s=''
    return {'return':0, 'bat':s}
