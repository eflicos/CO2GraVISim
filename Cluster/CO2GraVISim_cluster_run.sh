#!/bin/bash

# CO2GraVISim_cluster_run (21/10/24)
# $1 is baseFolder
# $2 is run number
# This is performs a batch run of CO2GraVISim over the inputs stored in
# $1/run_$2/Input, with the resulting outputs stored in 
# $1/run_$2/Output


baseFolder=$1"/run_"$2
processScript="./CO2GraVISim_single_run"

echo "[ --- Run $2 starting --- ]"

inputPath="${baseFolder}/Input"
outputPath="${baseFolder}/Output"

echo "$processScript" -input "$inputPath" -output "$outputPath"
"$processScript" -input "$inputPath" -output "$outputPath"

# Copy Volumes.txt to the output folder for this run
cp "./Output/Other/Volumes.txt" "$outputPath/Other/Volumes.txt"
