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
# setup software environment

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

	# Example: KaNN_Development_Package_v1.2/python/caffe_to_kann.py
    python_dir=os.path.dirname(fp)
    sdk_dir=os.path.dirname(python_dir)
    runtime_dir=os.path.join(sdk_dir, 'runtime')
    runtime_mppa_dir=os.path.join(runtime_dir, 'mppa')
    env[ep]=sdk_dir
    env[ep+'PYTHON_CAFFE_TO_KANN']=fp
    env[ep+'RUNTIME_MPPA']=runtime_mppa_dir
    # Version. TODO: Do not prompt for version - use this one.
    prefix='KaNN_Development_Package_'
    version=os.path.basename(sdk_dir)[len(prefix):]
    env[ep+'VERSION']=version

    return {'return':0, 'bat':s}
