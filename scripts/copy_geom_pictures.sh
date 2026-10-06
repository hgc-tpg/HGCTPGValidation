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
PATH_GEOM="../${DATA_DIR}/${PRCHANGE_ID}/${GEOM_CHECK_DIR}"

if [ ! -d $PATH_GEOM ] ; then
    mkdir -p $PATH_GEOM
else
    echo "The folder $PATH_GEOM exists."
    # Remove the content of ${GEOM_CHECK_DIR} directory including hidden files
    rm -rf $PATH_GEOM/* $PATH_GEOM/.[!.]*
fi

FILE="../${DATA_DIR}/${PRCHANGE_ID}/validation_webpages.txt"
# Checks if the FILE exists and if it contains the link to the Geom_check web page
if [ -f "$FILE" ] && ! grep -q "^$GEOM_CHECK_DIR" "$FILE"; then
    # Write the link to the Geom_check web page
    printf "${GEOM_CHECK_DIR} : Geometry check" >> "$FILE"
fi

# Copy the pictures and the html page from GeomCheck stage
cp -rf ./HGCTPGGeometryTools/results/test_triggergeom/plot_errors_files $PATH_GEOM/
cp ./HGCTPGGeometryTools/results/test_triggergeom/plot_errors.html $PATH_GEOM/index.html
