# py-voice-clone

A simple application to clone voices. Currently, real time cloned voice data streaming is not supported, but it is planned.

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


## Capturing a speaker's tone

Models that are fine-tuned on a specific speaker are going to pick up on little idiosyncracies in a speakers voice. If you want uniform / consistent
output from the model, then you need to ensure that your audio dataset only contains the inflection's you wish the outputted audio to capture.

Through testing, it seems that deleting audio clips that contain unwanted speaker inflection and increasing the number of samples with the desired inflection / tone can increase the quality of the output. In this case, a subjective assessment is made on whether or not the output matches the inputted speaker's voice closely or not.


## Running the program

This python application uses poetry to manage its dependencies. Please install poetry before continuing

```
poetry run python main.py
```
