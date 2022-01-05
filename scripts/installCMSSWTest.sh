
#!/bin/bash

# installCMSSWTest.sh $RELEASE
# $1 name of the release, it is taken from the $CHANGE_TARGET
# $2 name of the change branch $CHANGE_BRANCH

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc900
echo $SCRAM_ARCH
module purge
scramv1 p -n $1_HGCalTPGValidation_test $1
cd $1_HGCalTPGValidation_test/src
echo $PWD
eval `scramv1 runtime -sh`
git cms-merge-topic ebecheva:$2
git checkout -b local_$2 ebecheva/$2
scram b -j8
