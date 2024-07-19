import os
from TTS.api import TTS
from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.datasets import load_tts_samples
from src.custom_tts import CustomTTS
from src.thirdparty.whisper_client import FasterWhisperClient
from src.thirdparty.coqui_imported import main as coqui_main
ROOT_DIR = os.path.abspath(os.curdir)

speaker="portal2-wheatley"

def main():
  coqui_main(ROOT_DIR, "ljspeech")
    # print("instantiating whisper client")
    # whisper_client = FasterWhisperClient()
    # print("instantiated whisper client")

    # whisper_client.transcribe_directory(f"{ROOT_DIR}/out/single_channel_wavs")
    # print("transcribed directory")

  # speaker_wavs = get_speaker_wavs(speaker, ROOT_DIR)
  # # audacity_client = Audacity()

  # # audacity.label_sounds(audacity_client, speaker_wavs[0], ROOT_DIR)
  
  #   # train_model(speaker)
  #   # # # print(speaker_wavs)

  #   # generate_tts("On dark and lonely nights, George Bush is want to stare longingly into the moon while wearing his custom made fur-suit. The monster inside of him howls!?!?!? RAWWWRRR!!!! His little toes are cold in the snow of the first summer frost. He desperately seeks to find the one piece.", speaker_wavs)

  # model_dir= "model/XTTS-v2"
  # custom_tts = CustomTTS(f"{model_dir}/config.json", model_dir, speaker_wavs[0])
  # custom_tts.text_to_speech("On dark and lonely nights, George Bush is want to stare longingly into the moon while wearing his custom made fur-suit. The monster inside of him howls!?!?!? RAWWWRRR!!!! His little toes are cold in the snow of the first summer frost. He desperately seeks to find the one piece.")
  pass

# TODO: this doesn't do anything right now
def train_model(speaker):
    print("Training model...\n")
    training_dir= f"{ROOT_DIR}/lib/assets/training_data/{speaker}"

    # dataset config for one of the pre-defined datasets
    dataset_config = BaseDatasetConfig(
        formatter="vctk", meta_file_train="metadata.txt", language="en-us", path=training_dir, meta_file_val="metadata.txt"
    )


    # load training samples
    train_samples, eval_samples = load_tts_samples(dataset_config, eval_split=True, formatter=formatter, eval_split_size=0.071428571428571)
    # train_samples, eval_samples = load_tts_samples(dataset_config, eval_split=True)
    print(train_samples, eval_samples)


# get speaker wav files from an ljspeech structured directory
def get_speaker_wavs(speaker, root_path):
    training_dir= f"{root_path}/lib/assets/training_data/{speaker}"

    files = os.walk(training_dir)

    speaker_wavs = []

    for (dir_path, dir_names, file_names) in files:
        for file in file_names:
            if(file == 'metadata.txt'):
                continue
            speaker_wavs.append(f"{dir_path}/{file}")

    return speaker_wavs

def generate_tts(text, speaker_wavs):
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
    # generate speech by cloning a voice using default settings
    tts.tts_to_file(text=text,
                    file_path="output.wav",
                    speaker_wav=speaker_wavs,
                    language="en")

# custom formatter implementation
def formatter(root_path, manifest_file, **kwargs):  # pylint: disable=unused-argument
    """Assumes each line as ```<filename>|<transcription>```
    """
    txt_file = os.path.join(root_path, manifest_file)
    items = []
    speaker_name = speaker
    with open(txt_file, "r", encoding="utf-8") as ttf:
        for line in ttf:
            cols = line.split("|")
            wav_file = os.path.join(root_path, "wavs", cols[-1])
            text = cols[0]
            items.append({"text":text, "audio_file":wav_file, "speaker_name":speaker_name, "root_path": root_path})
    return items

if __name__ == "__main__":
    main()
