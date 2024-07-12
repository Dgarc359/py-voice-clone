# import os
# import time
# import torch
# import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts


class CustomTTS:

    def __init__(self, config_path: str, model_path: str) -> None:
        print("Initializing TTS client")
        self.model = self.init_model(config_path, model_path)        

    # This method currently initiates an xtts_v2 text to speech model, but is meant to house logic for future models
    def init_model(self, config_path: str, model_path: str):
        config = self.get_xtts_config(config_path)
       
        return self.init_xtts_model(config, model_path)

    def get_xtts_config(self, config_path: str):
        config = XttsConfig()
        config.load_json(config_path)
        return config
    
    def init_xtts_model(self, config, model_path):
        model = Xtts.init_from_config(config)

        model.load_checkpoint(config, checkpoint_dir=model_path, use_deepspeed=True)
        model.cuda()

        return model
