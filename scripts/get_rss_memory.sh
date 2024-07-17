#!/bin/bash

# Usage: call the script in HGCTPGValidation/scripts/produceData_multiconfiguration.py immediately after cmsRun
# get_rss_memory.sh $! interval limit
# 1rst argument: "$!" is the PID of python produceData_multiconfiguration.py process
# 2nd argument: interval in seconds
# 3th argument: memory limit

# Check if process name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 PID"
    exit 1
fi

# Get the PID of the process
INTERVAL=$2
RSS_limit=$3

while true; do
    echo "LastProcess PID= " $1
    p_all=$(ps -eo pid,user,comm | grep cmsRun | grep jenkins | awk '{print}')
    echo $p_all
    PID=$(ps -eo pid,user,comm | grep cmsRun | grep jenkins | awk '{print $1}')
    echo "PID=" $PID
    
    if [ -z "$PID" ]; then
        echo "Process $PID not found."
    else
        # Get the RSS (Resident Set Size) memory usage
        cp /proc/$PID/status ./status_${PID}
        ps
        echo "Get RSS value "
        RSS=$(grep -i vmrss /proc/$PID/status | awk '{print $2}')
        echo "===> RSS memory ${RSS}"
        if [ "${RSS}" -gt "${RSS_limit}" ]; then
            kill -9 $PID;
            echo "===> RSS memory ${RSS} > RSS limit ${RSS_limit}";
            break;
        fi
        
        # Output the RSS memory usage
        if [ -e /proc/$PID/status ]; then
            echo "Free memory (RSS) for process $1 (PID: $PID): ${RSS} kB"
        else
            echo "ProduceData_multiconfiguration.py process finished. PID = $PID"
            break;
        fi
    fi
    
    sleep $INTERVAL
done
