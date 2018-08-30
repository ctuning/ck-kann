# [cknowledge.org/ai](http://cknowledge.org/ai): Crowdsourcing benchmarking and optimisation of AI

A suite of open-source tools for [collecting knowledge on optimising AI](http://bit.ly/hipeac49-ckdl):
* [Android app](http://cKnowledge.org/android-apps.html)
* [Desktop app](https://github.com/dividiti/ck-crowdsource-dnn-optimization)
* [CK-Caffe](https://github.com/dividiti/ck-caffe)
* [CK-Caffe2](https://github.com/ctuning/ck-caffe2)
* [CK-KaNN](https://github.com/dividiti/ck-kann)
* [CK-TensorFlow](https://github.com/ctuning/ck-tensorflow)
* [CK-TensorRT](https://github.com/dividiti/ck-tensorrt)
* [CK-TinyDNN](https://github.com/ctuning/ck-tiny-dnn)
* etc.

# Collective Knowledge repository for benchmarking and optimising deep learning applications on Kalray platforms

[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-powered-by-ck.png)](http://cKnowledge.org)
[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-validated-by-the-community-simple.png)](http://cTuning.org)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

## Introduction

[CK-KaNN](https://github.com/dividiti/ck-kann) is an open-source framework for
benchmarking and optimising deep learning applications on
[Kalray platforms](http://www.kalrayinc.com/kalray/products/).

It's based on the [Kalray Neural
Network](http://www.electronics-eetimes.com/Learning-center/kalray-deep-learning-high-performance-applications)
framework from [Kalray](http://www.kalrayinc.com) (KaNN) and
the [Collective Knowledge](http://cknowledge.org) framework for customisable
cross-platform builds and experimental workflows with JSON API from the
[cTuning Foundation](http://ctuning.org) and [dividiti](http://dividiti.com).

## Authors/contributors

* Anton Lokhmotov, [dividiti](http://dividiti.com)
* Grigori Fursin, [dividiti](http://dividiti.com) / [cTuning foundation](http://ctuning.org)

## Instructions

The following instructions were tested on an
[EMB02](http://www.kalrayinc.com/kalray/products/#platforms) development
platform from Kalray.

### Installing CK

Install CK via `pip` and check its version:
```
$ sudo pip install ck
$ ck version
V1.9.1.1
```

Add the following to `$HOME/.bashrc`:
```
export CK_REPOS=$HOME/CK_REPOS
export CK_TOOLS=$HOME/CK_TOOLS
```

### Installing CK-KaNN

Install the CK-KaNN repository from GitHub:
```
$ ck pull repo:ck-kann --url=https://github.com/dividiti/ck-kann
$ ck find repo:ck-kann
/home/accesscore/CK_REPOS/ck-kann
```

Register a KaNN development package ("SDK") with CK:

```
$ ck detect soft:sdk.kann
$ ck show env --tags=kann,sdk
Env UID:         Target OS: Bits: Name:                    Version:    Tags:

b361a26c4b778517   linux-64    64 KaNN Development Package 1.2.1_light 64bits,host-os-linux-64,kalray,kann,sdk,target-os-linux-64,v1,v1.2,v1.2.1,v1.2.1.0
```
**NB:** CK will search for a `KaNN_Development_Package_<version>` directory in the `$HOME` directory.

### Installing CK-KaNN models and datasets

Install the four KaNN models and converted datasets as follows:

```
$ ck install package:kanndataset-imagenet-val-deepscale-squeezenet-1.0
$ ck install package:kanndataset-imagenet-val-deepscale-squeezenet-1.1
$ ck install package:kanndataset-imagenet-val-bvlc-alexnet
$ ck install package:kanndataset-imagenet-val-bvlc-googlenet
```

**NB:** For the first KaNN model to be installed on the platform, you will be
prompted to select a package with the ImageNet validation dataset. Please
select `imagenet-2012-val-min` containing 500 images, and then press `Enter` to
confirm the default path.

**NB:** For the AlexNet and GoogleNet models, you will be prompted to choose
between two options. Please select the ones ending with `-fast-mirror` to
download faster.

**NB:** Each of the `ck install package:kanndataset*` commands performs the following:
1. Downloads the corresponding Caffe model.
1. Generates the KaNN model from the Caffe model.
(The conversion flow is in `$CK_REPOS/ck-kann/script/caffe2kann`.)
1. Converts the ImageNet validation dataset to the KaNN format. (The conversion
flow is in `$CK_REPOS/ck-kann/script/imagenet2kann`.)

You can search and view what's been installed by tags e.g.
```
$ ck show env --tags=bvlc,googlenet
Env UID:           Target OS: Bits: Name:                                           Version:       Tags:

89cf44da9fb31f1a   linux-64   64    KaNN model (net and weights) (bvlc, googlenet)  bvlc-googlenet 64bits,bvlc,googlenet,host-os-linux-64,kalray,kann,kannmodel,net,target-os-linux-64,v0,v0.0,weights
bef89fc9a14962b3   linux-64   64    ImageNet dataset (validation, KaNN)             bvlc-googlenet 64bits,bvlc,dataset,googlenet,host-os-linux-64,imagenet,kann,target-os-linux-64,v0,v0.0,val,val-kann
f45b591e389c372f   linux-64   64    Caffe model (net and weights) (bvlc, googlenet) trunk          64bits,bvlc,caffe,caffemodel,googlenet,host-os-linux-64,mirror,net,target-os-linux-64,v0,weights
```

**NB:** For the other three models, the tags are: `bvlc,alexnet`,
`deepscale,squeezenet,v1.0`, `deepscale,squeezenet,v1.1`.

### Evaluating one of the installed KaNN models

To quickly evaluate one of the installed KaNN models under the current system
conditions (CPU and DDR frequencies), run:
```
$ ck run program:kann
```

**NB:** When prompted the first time, select one of the KaNN models e.g.
GoogleNet. When prompted the second time, select the corresponding converted
dataset e.g. again GoogleNet.

**NB:** If you select a wrong dataset, execution might fail. Using a CK
workflow below eliminates the chance for inconsistency.

You can specify the maximum number of images to process using the
`CK_KANN_MAX_NUMBER_IMAGES` environment variable. For example, to process
all the 500 images in the `imagenet-2012-val-min` dataset, run:

```
$ ck run program:kann --env.CK_KANN_MAX_NUMBER_IMAGES=500
```

You can specify MPPA and DDR frequencies to use for evaluation. For example, to set the MPPA
frequency to 400 MHz and the DDR frequency to 1066 MHz, run:
```
$ ck run program:kann --env.CK_CPU_FREQ=400 --env.CK_DDR_FREQ=1066
```

**NB:** The supported MPPA frequencies are 400 and 500 MHz. The supported DDR
frequencies are 1066 MHz and 1333 MHz. If you specify an unsupported frequency,
the current frequency will be used.

### Evaluating all the installed KaNN models

#### Running a workflow

You can evaluate all the installed KaNN models by running a special CK workflow:
```
$ ck find ck-kann:script:explore-models
/home/accesscore/CK_REPOS/ck-kann/script/explore-models
$ python /home/accesscore/CK_REPOS/ck-kann/script/explore-models/explore-models-benchmarking.py
```

#### Inspecting experimental results

This workflow processes a small number of images (e.g. 5) via CK-KaNN for each installed model, while varying the MPPA and DDR frequencies at the supported levels.
It produces 4 `experiment` entries, one of each model:
```
$ ck list experiment:*-kann
bvlc-googlenet-kann
bvlc-alexnet-kann
deepscale-squeezenet-1.1-kann
deepscale-squeezenet-1.0-kann
```

Each experiment has 4 "points" for the Cartesian product of the supported MPPA and DDR frequencies e.g.
```
ck find experiment:bvlc-alexnet-kann
/home/accesscore/CK_REPOS/local/experiment/bvlc-alexnet-kann
[accesscore@emb02 ck-kann]$ ls -la /home/accesscore/CK_REPOS/local/experiment/bvlc-alexnet-kann
total 2692
drwxrwxr-x. 3 accesscore accesscore   4096 Jun  1 01:49 .
drwxrwxr-x. 7 accesscore accesscore   4096 Jun  1 01:49 ..
-rw-rw-r--. 1 accesscore accesscore  66494 Jun  1 01:49 ckp-1a57d14a0224ad29.0001.json
-rw-rw-r--. 1 accesscore accesscore     77 Jun  1 01:49 ckp-1a57d14a0224ad29.features_flat.json
-rw-rw-r--. 1 accesscore accesscore  14114 Jun  1 01:49 ckp-1a57d14a0224ad29.features.json
-rw-rw-r--. 1 accesscore accesscore 586235 Jun  1 01:49 ckp-1a57d14a0224ad29.flat.json
-rw-rw-r--. 1 accesscore accesscore  66498 Jun  1 01:49 ckp-4e0bb2c8bde1d65a.0001.json
-rw-rw-r--. 1 accesscore accesscore     77 Jun  1 01:49 ckp-4e0bb2c8bde1d65a.features_flat.json
-rw-rw-r--. 1 accesscore accesscore  14114 Jun  1 01:49 ckp-4e0bb2c8bde1d65a.features.json
-rw-rw-r--. 1 accesscore accesscore 587324 Jun  1 01:49 ckp-4e0bb2c8bde1d65a.flat.json
-rw-rw-r--. 1 accesscore accesscore  66504 Jun  1 01:48 ckp-6ccb311474b98867.0001.json
-rw-rw-r--. 1 accesscore accesscore     77 Jun  1 01:48 ckp-6ccb311474b98867.features_flat.json
-rw-rw-r--. 1 accesscore accesscore  14114 Jun  1 01:48 ckp-6ccb311474b98867.features.json
-rw-rw-r--. 1 accesscore accesscore 586390 Jun  1 01:48 ckp-6ccb311474b98867.flat.json
-rw-rw-r--. 1 accesscore accesscore  66502 Jun  1 01:48 ckp-f21aa79f2464f9c9.0001.json
-rw-rw-r--. 1 accesscore accesscore     77 Jun  1 01:48 ckp-f21aa79f2464f9c9.features_flat.json
-rw-rw-r--. 1 accesscore accesscore  14114 Jun  1 01:48 ckp-f21aa79f2464f9c9.features.json
-rw-rw-r--. 1 accesscore accesscore 584808 Jun  1 01:48 ckp-f21aa79f2464f9c9.flat.json
drwxrwxr-x. 2 accesscore accesscore   4096 Jun  1 01:49 .cm
-rw-rw-r--. 1 accesscore accesscore     80 Jun  1 01:48 desc.json
-rw-rw-r--. 1 accesscore accesscore  23015 Jun  1 01:48 pipeline.json
```

#### Analysing experimental results

**TODO.**

## Feedback

Feel free to engage with our community via this mailing list:
* http://groups.google.com/group/collective-knowledge
