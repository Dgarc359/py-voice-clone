outdir=out/single_channel_wavs

rm -rf $outdir
mkdir $outdir

for file in $1/*.wav; do
  filename=$(basename -- "$file")
  ffmpeg -i "$file" -vn -ar 22050 -ac 1 "$outdir/$filename.wav"
done
