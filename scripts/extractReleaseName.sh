#!/usr/bin/env bash

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
    echo "===The name of the release rel is $s"
    export REF_RELEASE=$s
    break
  fi
  done
done
echo "1 The name of the release is $REF_RELEASE"
unset IFS
echo "2 The name of the release is $REF_RELEASE"
