#!/bin/bash

# installCMSSWRef.sh $RELEASE
# $1 name of the release

echo $1
echo $2

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc900
echo $SCRAM_ARCH
module purge
scramv1 p -n $1_HGCalTPGValidation_ref CMSSW $1
cd $1_HGCalTPGValidation_ref/src
echo $PWD
eval `scramv1 runtime -sh`
#git config --global user.name "Emilia Becheva"
#git config --global user.email emilia.becheva@llr.in2p3.fr
git cms-merge-topic ebecheva:$2
git checkout -b local_$2 ebecheva/$2
scram b -j8
