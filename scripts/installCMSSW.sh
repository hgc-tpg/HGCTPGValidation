#!/bin/bash

# This code is to use with Jenkins jobs triggering on Github Pull Request in the repository https://github.com/hgc-tpg
# ./installCMSSW.sh $SCRAM_ARCH $REF_RELEASE $REMOTE $BASE_REMOTE $CHANGE_BRANCH $CHANGE_TARGET ${LABEL_TEST}

# $1 SCRAM_ARCH
# $2 release name
# $3 remote name 
# $4 base remote name
# $5 branch name (corresponds to the branch containing the changes)
# $6 reference branch name (this is the target or base branch to which the change could be merged, it is in https://github.com/hgc-tpg repository)
# $7 label "ref" or "test"

set -x
export SCRAM_ARCH=$1
echo $SCRAM_ARCH
relversion=$2
echo $relversion
remote=$3
echo $remote
baseremote=$4
echo $baseremote
branch=$5
echo $branch
branch_ref=$6
echo $branch_ref
label=$7
echo $label

# Check the status after executing a command
get_status(){
if [ $? -eq 0 ]; 
then 
  echo "=== The command finished successfully: " $1
else 
  echo "===== > Error: " $1
  exit 1
fi
}

source /cvmfs/cms.cern.ch/cmsset_default.sh
module purge
# Install working directory for the release CMSSW $relversion
scramv1 p -n ${relversion}_HGCalTPGValidation_$label CMSSW $relversion
get_status
cd ${relversion}_HGCalTPGValidation_$label/src
eval `scramv1 runtime -sh`
# Get the reference (target) branch from the base remote
git cms-merge-topic $baseremote:$branch_ref
get_status
git checkout -b local_$branch_ref $baseremote/$branch_ref
get_status
# Merge the change branch into the reference branch
git cms-merge-topic $remote:$branch
get_status
# Compile
scram b -j8
get_status
