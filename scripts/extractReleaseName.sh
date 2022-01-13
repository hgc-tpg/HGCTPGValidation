#!/usr/bin/env bash

STR="hgc-tpg-devel-CMSSW_12_1_0_pre3-test"

########################################################
IFS="-"
for i in $STR
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
echo "release after for => $refrel"
