#!/bin/bash
# Usage: ./HGCTPGValidation/scripts/clean_environment.sh ${DATA_DIR} PR$CHANGE_ID

# Check if there are 2 arguments supplied to the script
if (( $# != 2 ))
then
  echo "Usage: ./HGCTPGValidation/scripts/clean_environment.sh DATA_DIR PR_ID"
  exit 1
fi

DATA_DIR=$1
PRCHANGE_ID=$2

set +x
echo '==> Clean the working environment. ============================'
exec >> log_Jenkins
echo '==> Clean the working environment. ============================'
if [ -d "/data/jenkins/workspace/${DATA_DIR}/$PRCHANGE_ID" ]
then
    echo 'Remove the old directory ' /data/jenkins/workspace/${DATA_DIR}/${PRCHANGE_ID}
    rm -rf /data/jenkins/workspace/${DATA_DIR}/${PRCHANGE_ID}
fi
echo '   '
