#
# Convert raw output of a KaNN sample to the CK format.
#
# Developers:
#   - Anton Lokhmotov, dividiti, 2017
#

import json
import os
import re
import struct

def ck_postprocess(i):
    ck=i['ck_kernel']
    rt=i['run_time']

    deps=i['deps']
    version=deps['kannmodel']['cus']['version']

    env=i['env']
    max_num_images=int(env.get('CK_KANN_MAX_NUMBER_IMAGES',-1))

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

    # Match e.g. "[io_0] frame 1: 19.48 ms - 051.34 fps".
    frame_regex = \
        '\[(?P<unit>[\w_]+)\] frame ' + \
        '(?P<idx>\d+): ' + \
        '(?P<ms>\d*\.?\d*) ms - ' + \
        '(?P<fps>\d*\.?\d*) fps'
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
    # Match e.g. '21.0ms 03.3ms(15.6%) 00.7ms(03.5%) ...'.
    last_frame_regex = \
        '(?P<total_ms>\d*\.?\d*)ms ' + \
        '(?P<wait_clus_ms>\d*\.?\d*)ms\((?P<wait_clus_pc>\d*\.?\d*)%\) ' + \
        '(?P<send_clus_ms>\d*\.?\d*)ms\((?P<send_clus_pc>\d*\.?\d*)%\) ' + \
        '(?P<wait_io_ms>\d*\.?\d*)ms\((?P<wait_io_pc>\d*\.?\d*)%\) ' + \
        '(?P<send_io_ms>\d*\.?\d*)ms\((?P<send_io_pc>\d*\.?\d*)%\) ' + \
        '(?P<conv_ms>\d*\.?\d*)ms\((?P<conv_pc>\d*\.?\d*)%\) ' + \
        '(?P<relu_ms>\d*\.?\d*)ms\((?P<relu_pc>\d*\.?\d*)%\) ' + \
        '(?P<copy_ms>\d*\.?\d*)ms\((?P<copy_pc>\d*\.?\d*)%\) ' + \
        '(?P<max_pool_ms>\d*\.?\d*)ms\((?P<max_pool_pc>\d*\.?\d*)%\) ' + \
        '(?P<avg_pool_ms>\d*\.?\d*)ms\((?P<avg_pool_pc>\d*\.?\d*)%\) ' + \
        '(?P<lrn_ms>\d*\.?\d*)ms\((?P<lrn_pc>\d*\.?\d*)%\) ' + \
        '(?P<softmax_ms>\d*\.?\d*)ms\((?P<softmax_pc>\d*\.?\d*)%\) ' + \
        '(?P<other_ms>\d*\.?\d*)ms\((?P<other_pc>\d*\.?\d*)%\)'
    # Match e.g. 'MPPA 400 MHz 5.96 FPS 167.83 ms' (deprecated).
    mppa_mhz_fps_ms_regex = \
        'MPPA ' + \
    	'(?P<mhz>\d*) MHz ' + \
    	'(?P<fps>\d*\.?\d*) FPS ' + \
    	'(?P<ms>\d*\.?\d*) ms'

    d={}
    d['version'] = version
    d['max_num_images'] = max_num_images
    d['params'] = {}
    d['args'] = {}
    d['frame_timings'] = []
    d['last_frame'] = []
    d['mppa_mhz_fps_ms'] = {}
    for line in lst:
        # Match io or host frame timing.
        match = re.search(frame_regex, line)
        if match:
            frame = {}
            frame['unit'] = match.group('unit')
            frame['idx'] = int(match.group('idx'))
            frame['ms'] = float(match.group('ms'))
            frame['fps'] = float(match.group('fps'))
            d['frame_timings'].append(frame)
        # Match params (net topology and weights).
        match = re.search(params_regex, line)
        if match:
            d['params']['path'] = match.group('path')
            d['params']['bytes'] = int(match.group('bytes'))
        # Match arguments (paths, number of images).
        match = re.search(arg_regex, line)
        if match:
            d['args'][match.group('idx')] = match.group('val')
        # Match timings on clusters for the last frame.
        match = re.search(last_frame_regex, line)
        if match:
            timings = {}
            timings['total_ms'] = float(match.group('total_ms'))
            timings['total_pc'] = float(100)
            timings['wait_clus_ms'] = float(match.group('wait_clus_ms'))
            timings['wait_clus_pc'] = float(match.group('wait_clus_pc'))
            timings['send_clus_ms'] = float(match.group('send_clus_ms'))
            timings['send_clus_pc'] = float(match.group('send_clus_pc'))
            timings['wait_io_ms'] = float(match.group('wait_io_ms'))
            timings['wait_io_pc'] = float(match.group('wait_io_pc'))
            timings['send_io_ms'] = float(match.group('send_io_ms'))
            timings['send_io_pc'] = float(match.group('send_io_pc'))
            timings['conv_ms'] = float(match.group('conv_ms'))
            timings['conv_pc'] = float(match.group('conv_pc'))
            timings['relu_ms'] = float(match.group('relu_ms'))
            timings['relu_pc'] = float(match.group('relu_pc'))
            timings['copy_ms'] = float(match.group('copy_ms'))
            timings['copy_pc'] = float(match.group('copy_pc'))
            timings['max_pool_ms'] = float(match.group('max_pool_ms'))
            timings['max_pool_pc'] = float(match.group('max_pool_pc'))
            timings['avg_pool_ms'] = float(match.group('avg_pool_ms'))
            timings['avg_pool_pc'] = float(match.group('avg_pool_pc'))
            timings['lrn_ms'] = float(match.group('lrn_ms'))
            timings['lrn_pc'] = float(match.group('lrn_pc'))
            timings['softmax_ms'] = float(match.group('softmax_ms'))
            timings['softmax_pc'] = float(match.group('softmax_pc'))
            timings['other_ms'] = float(match.group('other_ms'))
            timings['other_pc'] = float(match.group('other_pc'))
            d['last_frame'].append(timings)
        # Match a single line with 3 metrics (inaccurate).
        match = re.search(mppa_mhz_fps_ms_regex, line)
        if match:
            d['mppa_mhz_fps_ms']['mhz'] = int(match.group('mhz'))
            d['mppa_mhz_fps_ms']['fps'] = float(match.group('fps'))
            d['mppa_mhz_fps_ms']['ms']  = float(match.group('ms'))
            d['post_processed'] = 'yes'

    rr={}
    rr['return']=0

    d['frame_predictions'] = []
    imagenet_num_classes = 1000
    sizeof_fp32 = 4
    kann_output_file = 'tmp-kann-output.tmp'
    kann_paths_file = 'tmp-kann-paths.tmp'
    with open(kann_output_file, 'rb') as kann_output_f, open(kann_paths_file, 'r') as kann_paths_f:
        num_elems = imagenet_num_classes*max_num_images
        kann_output_as_binary = kann_output_f.read(sizeof_fp32*num_elems)
        kann_output_as_floats = struct.unpack('f'*num_elems, kann_output_as_binary)
        kann_paths = kann_paths_f.readlines()
    for image_idx in range(max_num_images):
        image_start = image_idx * imagenet_num_classes
        image_end = image_start + imagenet_num_classes
        image_probs = kann_output_as_floats[image_start:image_end]
        image_path = kann_paths[image_idx].rstrip('\n').replace('kann_input', 'JPEG')
        frame_predictions = {}
        frame_predictions['file_name'] = image_path
        frame_predictions['probs'] = image_probs
        # TODO: Access class labels. Calculate top1 and top5 accuracy.
        d['frame_predictions'].append(frame_predictions)

    if d.get('post_processed','')=='yes':
        # Save to fine-grain-timer file.
        r=ck.save_json_to_file({'json_file':'tmp-ck-timer.json', 'dict':d})
        if r['return']>0: return r
    else:
        rr['return']=1
        rr['error']='failed to match required info in KaNN output!'

    return rr

# Do not add anything here!
