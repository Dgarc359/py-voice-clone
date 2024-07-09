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

## Running the program

This python application uses poetry to manage its dependencies. Please install poetry before continuing

```
poetry run python main.py
```
