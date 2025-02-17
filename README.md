# py-voice-clone

A simple application to clone voices. Audio is outputted to the default sound device instead
of being saved to a file.

Currently following along with the fine-tuning video in the references section
and architecting the code so that it can easily be re-used on other datasets without
a lot of manual steps

**Available Utilities**
* Audacity labeling and audio splitting automation
* Faster Whisper ljspeech dataset creation

There is some utilities available to use the audacity scripting API to automate
labeling audio and splitting it out into individual pieces of audio.


# Setup

Before you run the application, you need to make sure you have a dataset loaded in `lib/assets/training_data` in this repository.

a valid ljspeech dataset can be retrieved from the coqui-ai-tts repository [here](https://github.com/idiap/coqui-ai-TTS/tree/dev/tests/data/ljspeech)


> [!IMPORTANT]
> This project uses poetry to manage dependencies and python versions. Before using this project, you will need to [install it.](https://python-poetry.org/docs/#installing-with-pipx)

# Usage

```sh
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
poetry install

# Run the application
poetry run python main.py
```

# Fine tuning

According to nanomonad, who references the author of coqui-tts, a fine-tuned xtts_v2 should have decent samples after 1.3 epochs, assuming that training and testing data were set up properly.

## Dataset structure

Audio datasets should conform to the following format:

```
| project-root
| lib
|   --> assets
|       --> training_data
|           --> $speaker_name
|               --> wavs/*.wav
```

`training_data` can contain a variety of speakers, simply create a folder named after your speaker, and fill up the wavs folder

A speakers dataset folder should conform to the ljspeech dataset specification, which requires wav files to be in a `wavs` directory, with
some kind of metadata.txt file available which contains transcriptions of your wav audio.

## Good datasets

There's been some simple experimentation done to see what constitutes a good dataset. Currently, it seems like you can increase the quality in these ways:
* Combining multiple wav files into one wav file, for a single speaker
* Increasing the number of speaker samples available in the dataset
* Removing audio clips that do not have the tone of the speaker you wish to capture
* Until more research is done, it's recommended to keep audio clips for training below 10 seconds


## Capturing a speaker's tone

Models that are fine-tuned on a specific speaker are going to pick up on little idiosyncracies in a speakers voice. If you want uniform / consistent
output from the model, then you need to ensure that your audio dataset only contains the inflection's you wish the outputted audio to capture.

Through testing, it seems that deleting audio clips that contain unwanted speaker inflection and increasing the number of samples with the desired inflection / tone can increase the quality of the output. In this case, a subjective assessment is made on whether or not the output matches the inputted speaker's voice closely or not.


## Running the program

This python application uses poetry to manage its dependencies. Please install poetry before continuing

```
poetry run python main.py
```

## Fine tuning the model

In order to fine tune the model, you will need to download the model from huggingface [here](https://huggingface.co/coqui/XTTS-v2)



## XTTSv2 Config


To do real time audio streaming, you should have an xtts config json. The one used in the project was first grabbed from [here](https://huggingface.co/coqui/XTTS-v2/blob/main/config.json)


## Leveraging CUDA

Helpful links
* https://docs.nvidia.com/cuda/wsl-user-guide/index.html

**tldr for CUDA on WSL**
Visit [this site](https://developer.nvidia.com/cuda-downloads)
And click: Linux -> x86_64 (or whatever your architecture is) -> WSL-Ubuntu -> 2.0

Although it says ubuntu, it should also theoretically work for Debian. YMMV.

There seems to be an issue with the version of deepspeed used: "0.10.3" on amd CPUs. Needs more investigation. Current plans are to enable
the user to flag whether or not they want to use deepspeed

You should go [here](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html) and make sure that you're able to leverage the CUDA toolkit before running this program


# Troubleshooting

**Text length exceeding 250 characters**
This might be an issue with the length of the audio files in your training dataset. 
Please try using the util script `delete-long-audio-files.sh` to take out the long audio files from your dataset. 
Afterwards, you can use the `diff_ljspeech_metadata_csv.py` file to create a new metadata.csv with the deleted files excluded.

# References and related work
* [Fine tuning xttsv2 Model](https://www.youtube.com/watch?v=dzvW4QZamm8)

# Latest run
run/training/GPT_XTTS_v2.0_LJSpeech_FT-single_channel_wavs-July-28-2024_01+59PM-9f8773b