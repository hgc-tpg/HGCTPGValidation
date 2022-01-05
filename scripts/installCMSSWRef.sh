#!/bin/bash

# installCMSSWRef.sh $RELEASE
# $1 name of the release
# $2 name of the change branch, $CHANGE_BRANCH

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc900
echo $SCRAM_ARCH
module purge
scramv1 p -n $1_HGCalTPGValidation_ref CMSSW $1
cd $1_HGCalTPGValidation_ref/src
echo $PWD
eval `scramv1 runtime -sh`
git cms-merge-topic hgc-tpg:$2
git checkout -b local_$2 hgc-tpg/$2
scram b -j8
