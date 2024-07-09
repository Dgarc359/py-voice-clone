training_data_dir="/home/dvd/development/machine-learning/datasets/ljspeech"
assets_dir="./lib/assets/training_data"

rm -rf $assets_dir
cp -r $training_data_dir/$1/ $assets_dir