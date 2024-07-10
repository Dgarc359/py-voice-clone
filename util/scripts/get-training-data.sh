source .env
training_data_dir=$training_data_dir
assets_dir="./lib/assets/training_data"

rm -rf $assets_dir

mkdir $assets_dir
cp -r $training_data_dir/$1/ $assets_dir/$1