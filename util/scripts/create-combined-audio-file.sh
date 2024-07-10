cd lib/assets/training_data/$1/wavs

files=$(ls)

directory="../../combined-$1"
rm -rf $directory
mkdir $directory
mkdir $directory/wavs

sox $files $directory/wavs/output.wav
