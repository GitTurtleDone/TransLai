import torch
from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig

# Allow the config class to be safely loaded
torch.serialization.add_safe_globals([XttsConfig])

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


# Define the path to your .txt file
text_file_path = "PythonBE/RogerPenroseEn.txt"
text_file_path_vi = "PythonBE/EmDiHocSomVI.txt"

# Read the contents of the file
with open(text_file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Text to speech list of amplitude values as output
wav = tts.tts(text, speaker_wav="PythonBE/GiangVoiceEn1.wav", language="en")
# Text to speech to a file
tts.tts_to_file(text, speaker_wav="PythonBE/GiangVoiceEn1.wav", language="en", file_path="PythonBE/RogerPenrose_tts_output1.wav")