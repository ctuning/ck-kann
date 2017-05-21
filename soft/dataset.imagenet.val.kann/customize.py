#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer(s):
# - Grigori Fursin, Grigori.Fursin@cTuning.org, 2016
# - Anton Lokhmotov, anton@dividiti.com, 2017
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
    s=''

	# Even if the original is removed, we still have a copy to figure out the number of images.
    cdeps=i['deps_copy']

    # Check the host platform.
    hosd=i['host_os_dict']
    hplat=hosd.get('ck_name','')
    hproc=hosd.get('processor','')
    #sdirs=hosd.get('dir_sep','')

    cus=i.get('customize',{})
    fp=cus.get('full_path','')
    pi=os.path.dirname(fp)

    ep=cus.get('env_prefix','')
    env=i['env']
    env[ep]=pi
    env['CK_KANN_IMAGENET_VAL']=pi

    # Check the number of images.
    pff=cus['ck_features_file']
    pf=os.path.join(pi, pff)
    features=cus.get('features',{})

    pim=cdeps.get('dataset-imagenet-raw',{}).get('dict',{}).get('env',{}).get('CK_CAFFE_IMAGENET_VAL','')
    if pim=='':
      if os.path.isfile(pf):
        r=ck.load_json_file({'json_file':pf})
        if r['return']>0: return r
        cus['features']=r['dict']
      else:
        return {'return':1, 'error':'CK features for KaNN input dataset are not defined and file \''+pff+'\' does not exist'}
    else:
      num=cus.get('first_images','')
      if num!='':
        num=int(num)
      else:
        dl=os.listdir(pim)
        num=0
        for fn in dl:
          if fn.endswith('.JPEG') or fn.endswith('.jpeg'):
            num+=1
      features['number_of_original_images']=num

    cus['features']=features

    # Get the KaNN model name from the Caffe model version.
    version=cdeps.get('kannmodel',{}).get('dict',{}).get('customize',{}).get('version')
    print(version)

    r=ck.save_json_to_file({'json_file':pf, 'dict':features})
    if r['return']>0: return r

    return {'return':0, 'bat':s}
