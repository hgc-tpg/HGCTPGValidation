#!/bin/bash
# Usage: ./HGCTPGValidation/scripts/quality_checks.sh ${REF_RELEASE} ${LABEL_TEST}

# Check if there are 2 arguments supplied to the script
if (( $# != 2 ))
then
  echo "Usage: ./HGCTPGValidation/scripts/quality_checks.sh ${REF_RELEASE} ${LABEL_TEST}"
  exit 1
fi

REF_RELEASE=$1
LABEL_TEST=$2

set +x
echo '===> Quality checks'
exec >> log_Jenkins
echo '===> Quality checks'
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd test_dir/${REF_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src
scram build code-checks
scram build code-format
GIT_STATUS=`git status --porcelain`
if [ ! -z "$GIT_STATUS" ]; then
    echo "Code-checks or code-format failed."
    exit 1;
fi
echo '    '
