#!/bin/bash
# Usage: ./copy_geom_pictures.sh ${DATA_DIR} PR$CHANGE_ID

# Check if there are 2 arguments supplied to the script
if (( $# != 2 ))
then
  echo "Usage: ./copy_geom_pictures.sh ${DATA_DIR} PR$CHANGE_ID"
  exit 1
fi

DATA_DIR=$1
PRCHANGE_ID=$2

echo "DATA_DIR = " $DATA_DIR
echo "PRCHANGE_ID = " $PRCHANGE_ID
pwd

GEOM_CHECK_DIR="Geom_check"

if [ ! -d "../${DATA_DIR}/${PRCHANGE_ID}/${GEOM_CHECK_DIR}" ] ; then
    mkdir ../${DATA_DIR}/${PRCHANGE_ID}/${GEOM_CHECK_DIR}
else
    echo "The folder" ../${DATA_DIR}/${PRCHANGE_ID}/${GEOM_CHECK_DIR} " exists."
fi

printf "${GEOM_CHECK_DIR} : Geometry check" >> "../${DATA_DIR}/${PRCHANGE_ID}/validation_webpages.txt"

# Copy the pictures and the html page from GeomCheck stage
cp -rf ./HGCTPGGeometryTools/results/test_triggergeom/plot_errors_files ../${DATA_DIR}/${PRCHANGE_ID}/${GEOM_CHECK_DIR}/
cp ./HGCTPGGeometryTools/results/test_triggergeom/plot_errors.html ../${DATA_DIR}/${PRCHANGE_ID}/${GEOM_CHECK_DIR}/index.html
