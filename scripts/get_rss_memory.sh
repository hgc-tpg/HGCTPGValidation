#!/bin/bash

# Usage: call the script in Jenkinsfile immediately after 
# python ../../../HGCTPGValidation/scripts/produceData_multiconfiguration.py --subsetconfig ${CONFIG_SUBSET} --label ${LABEL_REF}
# get_rss_memory.sh $! interval
# 1rst argument: "$!" is the PID of python produceData_multiconfiguration.py process
# 2nd argument: interval in seconds

# Check if process name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 PID"
    exit 1
fi

# Get the PID of the process
PID=$1
echo $PID
INTERVAL=$2

while true; do
    PID=$1
    
    if [ -z "$PID" ]; then
        echo "Process $PID not found."
    else
        # Get the RSS (Resident Set Size) memory usage
        RSS=$(grep -i vmrss /proc/$PID/status | awk '{print $2}')
        
        # Output the RSS memory usage
        if [ -e /proc/$PID/status ]; then
            echo "Free memory (RSS) for process $1 (PID: $PID): ${RSS} kB"
        else
            echo "ProduceData_multiconfiguration.py process finished."
            break;
        fi
    fi
    
    sleep $INTERVAL
done
