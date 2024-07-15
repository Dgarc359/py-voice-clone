from faster_whisper import WhisperModel
import os


class FasterWhisperClient():
  # distil-large-v3 or large-v3
  model_size: str

  def __init__(
      self,
      model_size: str = "distil-large-v3",
    ):
    self.model_size = model_size

    self.model = WhisperModel(
      model_size_or_path=model_size,
      # TODO: configurability for cuda
      device="cpu",
      compute_type="float32"
    )

  def transcribe_directory(self, audio_dir):
     for filename in os.listdir(audio_dir):
      if filename.endswith(".wav"):
          audio_file = os.path.join(audio_dir, filename)
          self.__text_to_speech(audio_file, audio_dir)

  def __text_to_speech(self, audio_file, audio_dir):
    base_filename, _ = os.path.splitext(os.path.basename(audio_file))
    try:
        segments, _ = self.model.transcribe(audio_file, beam_size=5, language="en", condition_on_previous_text=False)
        transcript = " ".join(segment.text.lstrip() for segment in segments)
        print(f"Transcribed and saved: {audio_file}")
        with open(os.path.join(audio_dir, "metadata.csv"), "a", encoding="utf-8") as csvfile:
            csvfile.write(f"{base_filename}|{transcript}|{transcript}\n")
    except Exception as e:
        print(f"Error transcribing {audio_file}: {e}")