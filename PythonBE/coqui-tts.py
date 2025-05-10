# import torch
# from TTS.api import TTS
# from TTS.tts.configs.xtts_config import XttsConfig
# from TTS.utils.synthesizer import Synthesizer
# import os

# # Allow the config class to be safely loaded
# torch.serialization.add_safe_globals([XttsConfig])

# # Get device
# device = "cuda" if torch.cuda.is_available() else "cpu"

# # List available 🐸TTS models
# print(TTS().list_models())

# # Init TTS
# #tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


# # Define the path to your .txt file
# text_file_path = "PythonBE/RogerPenroseEn.txt"
# text_file_path_vi = "PythonBE/EmDiHocSomVi.txt"
# tts_share_dir = "~/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2"

# # Read the contents of the file
# with open(text_file_path_vi, 'r', encoding='utf-8') as file:
#     text = file.read()

# synthesizer = Synthesizer(
#     tts_checkpoint="~/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2",
#     tts_config_path="~/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2/config.json",
#     #tts_speakers_file="path/to/speakers.json",   # optional
#     #tts_languages_file="path/to/languages.json", # optional
#     #vocoder_checkpoint=os.path.join(checkpoint_dir, "vocoder.pth"),    # if needed
#     #vocoder_config_path="path/to/vocoder_config.json",  # if needed
# )

# wav = synthesizer.tts(text, speaker_wav="PythonBE/GiangVoiceVi.wav", language="vi")

# # Run TTS
# # ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# # Text to speech list of amplitude values as output
# #wav = tts.tts(text, speaker_wav="PythonBE/GiangVoiceVi.wav", language="vi")
# # Text to speech to a file
# synthesizer.tts.tts_to_file(text, speaker_wav="PythonBE/GiangVoiceVi.wav", language="vi", file_path="PythonBE/EmDiHocSom.wav")


import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Text to speech list of amplitude values as output
text_file_path = "PythonBE/RogerPenroseEn.txt"
with open(text_file_path, 'r', encoding='utf-8') as file:
    text = file.read()
wav = tts.tts(text, speaker_wav="PythonBE/GiangVoiceEn.wav", language="en")
# Text to speech to a file
tts.tts_to_file(text, speaker_wav="PythonBE/GiangVoiceEn.wav", language="en", file_path="PythonBE/RogerPenroseEn_output2.wav")
