#!/bin/bash

# Delete audio files of X length, length should be given in seconds, default for now will be 11.6 seconds

if  [ -z "$1" ]; then
    echo "no argument supplied, please give a target directory"
    exit 1
fi

threshold=${2:-9.0}  # Use second argument as threshold, or 11.6 if not provided

for file in $1/wavs/*.wav; do
    audio_length=$(ffprobe -i $file -show_entries format=duration -v quiet -of csv="p=0")

    echo $audio_length
    echo "$audio_length > $threshold"
    # if (( "$audio_length" > 11.6 )); then
    if (( $(echo "$audio_length > $threshold" | bc -l) )); then
        echo "found a disturbingly long audio clip.. $file"
        # rm -rf $1/wavs/$file
        rm -rf $file
    fi

done