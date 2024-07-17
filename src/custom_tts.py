# import os
import pyaudio
import numpy as np
import time
import sounddevice as sd
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

class CustomTTS:

    def text_to_speech(self, text_to_speechify: str):
        self.__run_model_inference(text_to_speechify)

    def __init__(self, config_path: str, model_path: str, speaker_wav: str) -> None:
        print("Initializing TTS client")
        self.model = self.__init_model(config_path, model_path)        
        self.conditioning_latents = self.__compute_speaker_latent_embeddings(speaker_wav)

    # Wrappers

    # Wrapper for audio playback
    def __play_audio(self, wav, sample_rate):
      self.__play_sounddeviceaudio(wav, sample_rate)

    # Wrapper for model initialization
    # This method currently initiates an xtts_v2 text to speech model, but is meant to house logic for future models
    def __init_model(self, config_path: str, model_path: str):
        config = self.__get_xtts_config(config_path)
       
        return self.__init_xtts_model(config, model_path)

    # Specifically gets xtts model config
    def __get_xtts_config(self, config_path: str):
        config = XttsConfig()
        config.load_json(config_path)
        return config
    
    # Initializes xtts model
    def __init_xtts_model(self, config, model_path):
        model = Xtts.init_from_config(config)

        # TODO: configurability for deepspeed and cuda
        model.load_checkpoint(config, checkpoint_dir=model_path, use_deepspeed=False)
        # model.cuda()

        return model

    def __compute_speaker_latent_embeddings(self, speaker_wav: str):
        return self.model.get_conditioning_latents(audio_path=[speaker_wav])

    def __play_pyaudio(self, wav, sample_rate):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=sample_rate,
                        output=True)
        
        # Convert PyTorch tensor to numpy array
        audio_data = wav.squeeze().numpy()
        
        # Play the audio
        stream.write(audio_data.astype(np.float32).tobytes())
        
        stream.stop_stream()
        stream.close()
        p.terminate()

    # Sound device supposedly installs easier on most systems. Will need to test
    def __play_sounddeviceaudio(self, wav, sample_rate):
      sd.play(wav, samplerate=sample_rate)
      sd.wait()
    

    def __run_model_inference(self, text_to_speechify):
        gpt_cond_latent, speaker_embedding = self.conditioning_latents
        t0 = time.time()
        chunks = self.model.inference_stream(text_to_speechify, "en", gpt_cond_latent, speaker_embedding)

        wav_chunks = []
        for i, chunk in enumerate(chunks):
            if i == 0:
                print(f"Time to first chunk: {time.time() - t0}")
            print(f"Received chunk {i} of audio length {chunk.shape[-1]}")
            wav_chunks.append(chunk)
        wav = np.concatenate(wav_chunks, axis=0)
        self.__play_audio(wav, 24000)