source .env
training_data_dir=$training_data_dir
assets_dir="./lib/assets/training_data"

rm -rf $assets_dir

if  [ -z "$1" ]; then
    echo "no argument supplied, please give a target directory"
    exit 1
fi

mkdir $assets_dir
cp -r $training_data_dir/$1/ $assets_dir/$1