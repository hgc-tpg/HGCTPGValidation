#!/bin/bash

# ./installCMSSW.sh $SCRAM_ARCH $RELEASE $CHANGE_TARGET $LABEL
# 
# $1 SCRAM_ARCH
# $2 release name
# $3 target branch name
# $4 label "ref" or "test"

export SCRAM_ARCH=$1
echo $SCRAM_ARCH
relversion=$2
echo $relversion
branch=$3
echo $branch
label=$4
echo $label

source /cvmfs/cms.cern.ch/cmsset_default.sh
module purge
scramv1 p -n $relversion_HGCalTPGValidation_$label CMSSW $relversion
cd $relversion_HGCalTPGValidation_$label/src
echo $PWD
eval `scramv1 runtime -sh`
git cms-merge-topic hgc-tpg:$branch
git checkout -b local_$branch hgc-tpg/$branch
scram b -j8
