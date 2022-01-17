#!/usr/bin/env bash

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
