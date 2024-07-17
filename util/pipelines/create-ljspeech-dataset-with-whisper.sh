#!/bin/bash
source .env

# convert audio directory to single channel 22k hz
./util/scripts/create-single-channel-wavs.sh $directory_to_single_channel

# TODO: Explicit call to whisper dataset creation pipeline
