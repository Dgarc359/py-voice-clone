 
 assets_dir="lib/assets/training_data"
 out_dir="lib/out"
 speaker_file="wheatley-01-kill-you.wav"
 sf_02="Wheatley_bw_a4_finale01_smash02.wav"
 sf_03="Wheatley_bw_a4_finale02_turrettrap_nags01.wav"

 tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
     --text "$1" \
     --speaker_wav "$assets_dir/$speaker_file" "$assets_dir/$sf_02" "$assets_dir/$sf_03" \
     --language_idx en \
     --use_cuda true