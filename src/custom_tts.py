# import os
import time
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
import sounddevice as sd
import numpy as np


class CustomTTS:

    def text_to_speech(self, text_to_speechify: str):
        self.__run_model_inference(text_to_speechify)

    def __init__(self, config_path: str, model_path: str, speaker_wav: str) -> None:
        print("Initializing TTS client")
        self.model = self.__init_model(config_path, model_path)        
        self.conditioning_latents = self.__compute_speaker_latent_embeddings(speaker_wav)

    # This method currently initiates an xtts_v2 text to speech model, but is meant to house logic for future models
    def __init_model(self, config_path: str, model_path: str):
        config = self.__get_xtts_config(config_path)
       
        return self.__init_xtts_model(config, model_path)


    def __get_xtts_config(self, config_path: str):
        config = XttsConfig()
        config.load_json(config_path)
        return config
    
    def __init_xtts_model(self, config, model_path):
        model = Xtts.init_from_config(config)

        model.load_checkpoint(config, checkpoint_dir=model_path, use_deepspeed=True)
        model.cuda()

        return model

    def __compute_speaker_latent_embeddings(self, speaker_wav: str):
        return self.model.get_conditioning_latents(audio_path=[speaker_wav])

    def __run_model_inference(self, text_to_speechify):
        gpt_cond_latent, speaker_embedding = self.conditioning_latents
        t0 = time.time()
        chunks = self.model.inference_stream(text_to_speechify, "en", gpt_cond_latent, speaker_embedding)

        wav_chunks = []
        for i, chunk in enumerate(chunks):
            if i == 0:
                print(f"Time to first chunck: {time.time() - t0}")
            print(f"Received chunk {i} of audio length {chunk.shape[-1]}")
            wav_chunks.append(chunk)
        wav = torch.cat(wav_chunks, dim=0)
        cpu_wav = wav.cpu()
        audio_numpy = cpu_wav.numpy().T

        sd.play(audio_numpy, 24000)
        sd.wait()
        torchaudio.save("xtts_streaming.wav", wav.squeeze().unsqueeze(0).cpu(), 24000)