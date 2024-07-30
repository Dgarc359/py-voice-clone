outdir=out/single_channel_wavs

rm -rf $outdir
mkdir $outdir

if  [ -z "$1" ]; then
    echo "no argument supplied, please give a target directory"
    exit 1
fi

for file in $1/*.wav; do
  filename=$(basename -- "$file")
  ffmpeg -i "$file" -vn -ar 22050 -ac 1 "$outdir/$filename"
done
