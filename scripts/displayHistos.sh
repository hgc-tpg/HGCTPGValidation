#!/bin/bash

echo 'Run displayHistos.sh'
echo $#
echo $1
echo $2
echo $3
echo $simu_env

if [ $simu_env -eq 1 ]
then
    # Config at Cern
    echo 'Config at Cern'
    source /opt/rh/python27/enable
    source /cvmfs/sft.cern.ch/lcg/releases/gcc/4.9.3/x86_64-slc6-gcc49-opt/setup.sh
    source /cvmfs/sft.cern.ch/lcg/releases/ROOT/6.06.06-a2c9d/x86_64-slc6-gcc49-opt/bin/thisroot.sh
elif [ $simu_env -eq 2 ]
then
    # Config at LLR in sl6, switch to python2
    echo 'Config at LLR in sl6, switch to python2'
    source /usr/share/Modules/init/bash
    module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles
    module purge
    module load python/2.7.9
    source /opt/exp_soft/llr/root/v6.06.00-el6-gcc48/etc/init.sh
else [ $simu_env -eq 3 ]
    # Config at LLR in sl7, python3
     echo 'Config at LLR in sl7'
fi

echo 'The Python version is: '
python -V
echo 'The ROOT version is:'
root-config --version

# Extract Time information for all modules
find . -name "out_ref.log" | xargs grep "TimeModule>" > TimingInfo_ref.txt
find . -name "out_test.log" | xargs grep "TimeModule>" > TimingInfo_test.txt
# Extract Memory Check information and global Time information
python ../HGCTPGValidation/hgctpgvalidation/display/extractTimeMemoryInfos.py --reffile out.log --testfile out.log --refdir $1 --testdir $2
# Create histograms Time/event/producer from TimingInfo_.txt 
python ../HGCTPGValidation/hgctpgvalidation/display/timing.py --reffile TimingInfo_ref.txt --testfile TimingInfo_test.txt --refdir $1 --testdir $2
# Compare histograms for the two releases and create pages
python ../HGCTPGValidation/hgctpgvalidation/display/standAloneHGCALTPGhistosCompare.py --refdir $1 --testdir $2 --webdir $3
