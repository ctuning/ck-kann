#
# Convert raw output of a KaNN sample to the CK format.
#
# Developers:
#   - Anton Lokhmotov, dividiti, 2017
#

import json
import os
import re

def ck_postprocess(i):
    ck=i['ck_kernel']
    rt=i['run_time']

    deps=i['deps']
    version=deps['kannmodel']['cus']['version']

    # Load and concatenate stdout and stderr.
    lst=[]
    stdout=rt['run_cmd_out1']
    stderr=rt['run_cmd_out2']
    if os.path.isfile(stdout):
       r=ck.load_text_file({'text_file':stdout,'split_to_list':'yes'})
       if r['return']>0: return r
       lst+=r['lst']
    if os.path.isfile(stderr):
       r=ck.load_text_file({'text_file':stderr,'split_to_list':'yes'})
       if r['return']>0: return r
       lst+=r['lst']

    # Match e.g. '[host] reading parameters from "/home/accesscore/KaNN_Evaluation_Package_v1.2/GoogLeNet_imagenet/params.bin": 14013664 bytes read'.
    params_regex = \
        '\[host\] reading parameters from ' + \
        '\"(?P<path>[\w\./_-]*)\"' + \
        ': (?P<bytes>\d+) bytes read'
    # Match e.g. '[clus_00] Arg 2: io_bin'.
    arg_regex = \
        '\[clus_00\] Arg ' + \
        '(?P<idx>\d+): ' + \
        '(?P<val>[\w\./_-]*)'
    # Match e.g. 'MPPA 400 MHz 5.96 FPS 167.83 ms' (deprecated).
    mppa_mhz_fps_ms_regex = \
        'MPPA ' + \
    	'(?P<mhz>\d*) MHz ' + \
    	'(?P<fps>\d*\.?\d*) FPS ' + \
    	'(?P<ms>\d*\.?\d*) ms'

    d={}
    d['version'] = version
    d['params'] = {}
    d['args'] = {}
    d['mppa_mhz_fps_ms'] = {}
    for line in lst:
        # Match params (net topology and weights).
        match = re.search(params_regex, line)
        if match:
            d['params']['path'] = match.group('path')
            d['params']['bytes'] = int(match.group('bytes'))
        # Match arguments (paths, number of images).
        match = re.search(arg_regex, line)
        if match:
            d['args'][match.group('idx')] = match.group('val')
        # Match a single line with 3 metrics (inaccurate).
        match = re.search(mppa_mhz_fps_ms_regex, line)
        if match:
            d['mppa_mhz_fps_ms']['mhz'] = int(match.group('mhz'))
            d['mppa_mhz_fps_ms']['fps'] = float(match.group('fps'))
            d['mppa_mhz_fps_ms']['ms']  = float(match.group('ms'))
            d['post_processed'] = 'yes'

    rr={}
    rr['return']=0

    if d.get('post_processed','')=='yes':
        # Save to fine-grain-timer file.
        r=ck.save_json_to_file({'json_file':'tmp-ck-timer.json', 'dict':d})
        if r['return']>0: return r
    else:
        rr['return']=1
        rr['error']='failed to match required info in KaNN output!'

    return rr

# Do not add anything here!
