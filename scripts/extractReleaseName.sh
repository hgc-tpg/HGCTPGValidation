#!/usr/bin/env bash

# $1 is the target branch name $CHANGE_TARGET

########################################################
IFS="-"
for i in $1
do
  s=$i
  IFS="_"
  for j in $s
  do
    rel=$j
    if [ "$rel" == "CMSSW" ]
    then
    #echo "===The name of the release rel is $s"
    export REF_RELEASE=$s
    break
  fi
  done
done
echo "The name of the release is $refrel"
