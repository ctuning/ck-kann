#! /bin/bash

#
# Installation script for the 2012 ImageNet Large Scale Visual Recognition
# Challenge (ILSVRC'12) validation dataset.
#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Anton Lokhmotov, anton@dividiti.com, 2016-2017
# - Grigori Fursin, Grigori.Fursin@cTuning.org, 2016

# PACKAGE_DIR
# INSTALL_DIR

export CK_KANN_INPUT_PREPARATOR=${CK_ENV_MODEL_KANN_INPUT_PREPARATOR}
export CK_KANN_IMAGENET_VAL=${INSTALL_DIR}/data/
mkdir -p ${CK_KANN_IMAGENET_VAL}

################################################################################
echo ""
echo "Converting images ..."
echo "- from directory: ${CK_CAFFE_IMAGENET_VAL}"
echo "- to directory: ${CK_KANN_IMAGENET_VAL}"
echo "- using script: ${CK_KANN_INPUT_PREPARATOR}"
echo ""

for filename in ${CK_CAFFE_IMAGENET_VAL}/ILSVRC2012_val_*.JPEG; do
  echo "Converting '$(basename "$filename")' ..."
  python ${CK_KANN_INPUT_PREPARATOR} $(basename "$filename" .JPEG).kann_input "$filename"
done
echo ""

################################################################################
if [ "${?}" != "0" ] ; then
  echo "Error: Converting one or more images in ${PWD} failed!"
  exit 1
fi

echo "Successfully converted images ..."
exit 0
