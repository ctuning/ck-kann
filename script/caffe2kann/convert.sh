#!/bin/bash

#
# Generate KaNN model from Caffe model.
#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
#
# Developer(s):
# - Anton Lokhmotov, anton@dividiti.com, 2017
#

#
# CK defines the following variables automatically:
#
# ORIGINAL_PACKAGE_DIR - kannmodel package dir (where the kannmodel meta resides)
# PACKAGE_DIR - caffe2kann script dir (where this script resides)
# INSTALL_DIR - installation dir (where the generated model will reside)
# CK_ENV_SDK_KANN_RUNTIME_MPPA - dir with mppa runtime from sdk-kann dependency
# CK_ENV_SDK_KANN_PYTHON_CAFFE_TO_KANN - python script from sdk-kann dependency
# CK_ENV_MODEL_CAFFE - dir containing topology from caffemodel dependency
# CK_ENV_MODEL_CAFFE_WEIGHTS - weights file from caffemodel dependency
#

export KANNMODEL_MAKEFILE_DIR=${CK_ENV_SDK_KANN_RUNTIME_MPPA}
export KANNMODEL_GENERATOR_TOOL=${CK_ENV_SDK_KANN_PYTHON_CAFFE_TO_KANN}
export KANNMODEL_INPUT_CAFFE_WEIGHTS_FILE=${CK_ENV_MODEL_CAFFE_WEIGHTS}
export KANNMODEL_OUTPUT_DIR=${INSTALL_DIR}/generated/

################################################################################
echo "Preparing Caffe topology file ..."
echo

export KANNMODEL_TOPOLOGY_FILE=${ORIGINAL_PACKAGE_DIR}/deploy.prototxt
export CAFFEMODEL_TOPOLOGY_FILE=${CK_ENV_MODEL_CAFFE}/deploy.prototxt

if [[ -e ${KANNMODEL_TOPOLOGY_FILE} ]]
then
  export KANNMODEL_INPUT_CAFFE_TOPOLOGY_FILE=${KANNMODEL_TOPOLOGY_FILE}
  # Do nothing else.
else
  export KANNMODEL_INPUT_CAFFE_TOPOLOGY_FILE=${INSTALL_DIR}/deploy.prototxt
  # Set the batch size to 1 (the only batch size currently supported by KaNN).
  cat ${CAFFEMODEL_TOPOLOGY_FILE} | sed 's/$#batch_size#\$/1/' > ${KANNMODEL_INPUT_CAFFE_TOPOLOGY_FILE}
  if [ "${?}" != "0" ] ; then
    echo "Error: Setting the batch size to 1 failed!"
    exit 1
  fi
fi

################################################################################
echo "Generating KaNN model from Caffe model ..."
echo "- Generator tool: '${KANNMODEL_GENERATOR_TOOL}'"
echo "- Input Caffe topology: '${KANNMODEL_INPUT_CAFFE_TOPOLOGY_FILE}'"
echo "- Input Caffe weights: '${KANNMODEL_INPUT_CAFFE_WEIGHTS_FILE}'"
echo "- Output dir: '${KANNMODEL_OUTPUT_DIR}'"
echo

################################################################################
echo "Generating KaNN model ..."
echo

rm -rf ${KANNMODEL_OUTPUT_DIR}
mkdir -p ${KANNMODEL_OUTPUT_DIR}

# TODO: Add python dependency.
python ${KANNMODEL_GENERATOR_TOOL} ${KANNMODEL_OUTPUT_DIR} ${KANNMODEL_INPUT_CAFFE_TOPOLOGY_FILE} ${KANNMODEL_INPUT_CAFFE_WEIGHTS_FILE}

if [ "${?}" != "0" ]
then
  echo "Error: Generating KaNN model failed!"
  exit 1
fi

################################################################################
echo "Compiling KaNN model ..."
echo

# TODO: Add make dependency.
codegen_path=${KANNMODEL_OUTPUT_DIR} make -j32 -C ${KANNMODEL_MAKEFILE_DIR}

if [ "${?}" != "0" ]
then
  echo "Error: Compiling KaNN model failed!"
  exit 1
fi

################################################################################
echo "Installing KaNN model ..."
echo

export KANNMODEL_BIN_DIR=${CK_ENV_SDK_KANN_RUNTIME_MPPA}/output/bin

cp ${KANNMODEL_BIN_DIR}/io_bin ${KANNMODEL_OUTPUT_DIR}
cp ${KANNMODEL_BIN_DIR}/host_bin ${KANNMODEL_OUTPUT_DIR}
cp ${KANNMODEL_BIN_DIR}/multibin_bin.mpk ${KANNMODEL_OUTPUT_DIR}

if [ "${?}" != "0" ]
then
  echo "Error: Installing KaNN model failed!"
  exit 1
fi

################################################################################
exit 0
