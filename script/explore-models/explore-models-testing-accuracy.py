#! /usr/bin/python
import ck.kernel as ck
import copy
import re


# Framework tag.
framework_tag='kann'

# Platform tag.
platform_tag='kalray-emb02'

# Maximum number of images (> 1).
max_num_images=5

# Number of statistical repetitions.
num_repetitions=1


def do(i):
    # Detect basic platform info.
    ii={'action':'detect',
        'module_uoa':'platform',
        'out':'out'}
    r=ck.access(ii)
    if r['return']>0: return r

    # Host and target OS params.
    hos=r['host_os_uoa']
    hosd=r['host_os_dict']

    tos=r['os_uoa']
    tosd=r['os_dict']
    tdid=r['device_id']

    # Program and command.
    program='kann'
    cmd_key='default'

    # Load KaNN program meta and desc to check deps.
    ii={'action':'load',
        'module_uoa':'program',
        'data_uoa':program}
    rx=ck.access(ii)
    if rx['return']>0: return rx
    mm=rx['dict']

    # Get compile-time and run-time deps.
    cdeps=mm.get('compile_deps',{})
    rdeps=mm.get('run_deps',{})

    # Merge rdeps with cdeps for setting up the pipeline (which uses
    # common deps), but tag them as "for_run_time".
    for k in rdeps:
        cdeps[k]=rdeps[k]
        cdeps[k]['for_run_time']='yes'

    # KaNN datasets.
    depd=copy.deepcopy(cdeps['kanndataset'])
    ii={'action':'resolve',
        'module_uoa':'env',
        'quiet':'yes', # any dataset
        'out':'con',
        'deps':{'kanndataset':depd}
    }
    r=ck.access(ii)
    if r['return']>0: return r

    udepd=r['deps']['kanndataset'].get('choices',[]) # All UOAs of env for KaNN datasets.
    if len(udepd)==0:
        return {'return':1, 'error':'no installed KaNN datasets'}

    max_num_images=r['deps']['kanndataset'].get('dict',{}).get('customize',{}).get('features',{}).get('number_of_original_images',1)
    print (r['deps'])

    # KaNN models.
    depm=copy.deepcopy(cdeps['kannmodel'])
    ii={'action':'resolve',
        'module_uoa':'env',
        'quiet':'yes', # any model
        'out':'con',
        'deps':{'kannmodel':depm}
    }
    r=ck.access(ii)
    if r['return']>0: return r

    udepm=r['deps']['kannmodel'].get('choices',[]) # All UOAs of env for KaNN models.
    if len(udepm)==0:
        return {'return':1, 'error':'no installed KaNN models'}

    # Prepare pipeline.
    cdeps['kanndataset']['uoa']=udepd[0]
    cdeps['kannmodel']['uoa']=udepm[0]

    ii={'action':'pipeline',
        'prepare':'yes',
        'dependencies':cdeps,

        'module_uoa':'program',
        'data_uoa':program,
        'cmd_key':cmd_key,

        'env': {
          'CK_KANN_MAX_NUMBER_IMAGES':max_num_images
        },

        'no_state_check':'yes',
        'no_compiler_description':'yes',
        'skip_calibration':'yes',

        'skip_print_timers':'yes',
        'skip_compile':'yes',
        'out':'con'
    }

    r=ck.access(ii)
    if r['return']>0: return r

    fail=r.get('fail','')
    if fail=='yes':
        return {'return':10, 'error':'pipeline failed ('+r.get('fail_reason','')+')'}

    ready=r.get('ready','')
    if ready!='yes':
        return {'return':11, 'error':'pipeline not ready'}

    state=r['state']
    tmp_dir=state['tmp_dir']

    # Remember resolved deps for this benchmarking session.
    xcdeps=r.get('dependencies',{})

    # Clean pipeline.
    if 'ready' in r: del(r['ready'])
    if 'fail' in r: del(r['fail'])
    if 'return' in r: del(r['return'])

    pipeline=copy.deepcopy(r)

    # For each KaNN dataset.****************************************************
    for uoad in udepd:
        # Load KaNN dataset.
        ii={'action':'load',
            'module_uoa':'env',
            'data_uoa':uoad}
        r=ck.access(ii)
        if r['return']>0: return r
        # Get version e.g. 'bvlc-alexnet'.
        verd=r['dict']['customize']['version']
        # Skip some datasets/models with "in [..]" or "not in [..]".
        if verd in []: continue

        # For each KaNN model.*************************************************
        for uoam in udepm:
            # Load KaNN model.
            ii={'action':'load',
                'module_uoa':'env',
                'data_uoa':uoam}
            r=ck.access(ii)
            if r['return']>0: return r
            # Get version e.g. 'bvlc-googlenet'.
            verm=r['dict']['customize']['version']
            if verd!=verm: continue
            version_tag = verd

            record_repo='local'
            record_uoa=version_tag+'-kann'+'-imagenet-ilsvrc2012-val'

            # Prepare pipeline.
            ck.out('---------------------------------------------------------------------------------------')
            ck.out('%s - %s' % ('Model', uoam))
            ck.out('%s - %s' % ('Dataset', uoad))
            ck.out('Experiment - %s:%s' % (record_repo, record_uoa))

            # Prepare autotuning input.
            cpipeline=copy.deepcopy(pipeline)

            # Reset deps and change UOA.
            new_deps={'kanndataset':copy.deepcopy(depd),
                      'kannmodel':copy.deepcopy(depm)}

            new_deps['kanndataset']['uoa']=uoad
            new_deps['kannmodel']['uoa']=uoam

            jj={'action':'resolve',
                'module_uoa':'env',
                'deps':new_deps}
            r=ck.access(jj)
            if r['return']>0: return r

            cpipeline['dependencies'].update(new_deps)

            ii={'action':'autotune',

                'module_uoa':'pipeline',
                'data_uoa':'program',

                'choices_order':[
                    [
                        '##choices#env#CK_CPU_FREQ'
                    ],
                    [
                        '##choices#env#CK_DDR_FREQ'
                    ]
                ],
                'choices_selection':[
                    {'type':'loop', 'choice':[ 500]},
                    {'type':'loop', 'choice':[1333]}
                ],

                'features_keys_to_process':[
                    '##choices#env#CK_CPU_FREQ',
                    '##choices#env#CK_DDR_FREQ'
                ],

                'iterations':-1,
                'repetitions':num_repetitions,

                'record':'yes',
                'record_failed':'yes',
                'record_params':{
                    'search_point_by_features':'yes'
                },
                'record_repo':record_repo,
                'record_uoa':record_uoa,

                'tags':[ 'explore-models-testing-accuracy', 'dataset-imagenet-ilsvrc2012-val', framework_tag, platform_tag, version_tag ],

                'pipeline':cpipeline,
                'out':'con'}

            r=ck.access(ii)
            if r['return']>0: return r

            fail=r.get('fail','')
            if fail=='yes':
                return {'return':10, 'error':'pipeline failed ('+r.get('fail_reason','')+')'}

    return {'return':0}


r=do({})
if r['return']>0: ck.err(r)
