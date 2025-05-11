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

# The inference code is adopted from https://github.com/coqui-ai/TTS/blob/dev/TTS/demos/xtts_ft_demo/xtts_demo.py
# @title 2. 🤗 **Sử dụng**
# @markdown 👈 Nhấn để chạy.
# @markdown Nếu gặp lỗi thì cũng nhấn nút này nhé!



# @markdown Kết quả sẽ được lưu vào `/content/output`

text_file_path = "PythonBE/RogerPenroseEn.txt"
with open(text_file_path, 'r', encoding='utf-8') as file:
    input_text = file.read()

# @markdown Chọn ngôn ngữ:
language = "Tiếng Anh" # @param ["Tiếng Việt", "Tiếng Anh","Tiếng Tây Ban Nha", "Tiếng Pháp","Tiếng Đức","Tiếng Ý", "Tiếng Bồ Đào Nha", "Tiếng Ba Lan", "Tiếng Thổ Nhĩ Kỳ", "Tiếng Nga", "Tiếng Hà Lan", "Tiếng Séc", "Tiếng Ả Rập", "Tiếng Trung (giản thể)", "Tiếng Nhật", "Tiếng Hungary", "Tiếng Hàn", "Tiếng Hindi"]
# @markdown Văn bản để đọc. Độ dài tối thiểu mỗi câu nên từ 10 từ để đặt kết quả tốt nhất.
text_file_path = "PythonBE/RogerPenroseEn.txt"
with open(text_file_path, 'r', encoding='utf-8') as file:
    text = file.read()
# @markdown Chọn giọng mẫu:
reference_audio = "PythonBE/GiangVoiceEn.wav" # @param [ "model/user_sample.wav",  "model/vi_sample.wav",  "model/samples/nam-calm.wav",  "model/samples/nam-cham.wav",  "model/samples/nam-nhanh.wav",  "model/samples/nam-truyen-cam.wav",  "model/samples/nu-calm.wav",  "model/samples/nu-cham.wav",  "model/samples/nu-luu-loat.wav",  "model/samples/nu-nhan-nha.wav",  "model/samples/nu-nhe-nhang.wav"]
# @markdown Tự động chuẩn hóa chữ (VD: 20/11 -> hai mươi tháng mười một)
normalize_text = True # @param {type:"boolean"}
# @markdown In chi tiết xử lý
verbose = False # @param {type:"boolean"}
# @markdown Lưu từng câu thành file riêng lẻ.
output_chunks = False # @param {type:"boolean"}



from IPython.display import clear_output


import os
import string
import unicodedata
from datetime import datetime
from pprint import pprint

import torch
import torchaudio
from tqdm import tqdm
from underthesea import sent_tokenize
from unidecode import unidecode

def cry_and_quit():
    clear_output()
    print("> Lỗi rồi huhu 😭😭, bạn hãy nhấn chạy lại phần này nhé!")
    quit()
try:
    from vinorm import TTSnorm
    from TTS.tts.configs.xtts_config import XttsConfig
    from TTS.tts.models.xtts import Xtts
except:
    cry_and_quit()


def clear_gpu_cache():
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

# Load model
def load_model(xtts_checkpoint, xtts_config, xtts_vocab):
    clear_gpu_cache()
    if not xtts_checkpoint or not xtts_config or not xtts_vocab:
        return "You need to run the previous steps or manually set the `XTTS checkpoint path`, `XTTS config path`, and `XTTS vocab path` fields !!"
    config = XttsConfig()
    config.load_json(xtts_config)
    XTTS_MODEL = Xtts.init_from_config(config)
    print("Loading XTTS model! ")
    XTTS_MODEL.load_checkpoint(config,
                               checkpoint_path=xtts_checkpoint,
                               vocab_path=xtts_vocab,
                               use_deepspeed=False)
    if torch.cuda.is_available():
        XTTS_MODEL.cuda()

    print("Model Loaded!")
    return XTTS_MODEL


def get_file_name():

    global text_file_path
    
    filename = os.path.splitext(os.path.basename(text_file_path))[0]
    current_datetime = datetime.now().strftime("%y%m%d%H%M%S")
    filename = f"{current_datetime}_{filename}"
    return filename

def get_file_name1(text, max_char=50):
    filename = text[:max_char]
    filename = filename.lower()
    filename = filename.replace(" ", "_")
    filename = filename.translate(str.maketrans("", "", string.punctuation.replace("_", "")))
    filename = unidecode(filename)
    current_datetime = datetime.now().strftime("%m%d%H%M%S")
    filename = f"{current_datetime}_{filename}"
    return filename


def calculate_keep_len(text, lang):
    if lang in ["ja", "zh-cn"]:
        return -1

    word_count = len(text.split())
    num_punct = (
        text.count(".")
        + text.count("!")
        + text.count("?")
        + text.count(",")
    )

    if word_count < 5:
        return 15000 * word_count + 2000 * num_punct
    elif word_count < 10:
        return 13000 * word_count + 2000 * num_punct
    return -1


def normalize_vietnamese_text(text):
    text = (
        TTSnorm(text, unknown=False, lower=False, rule=True)
        .replace("..", ".")
        .replace("!.", "!")
        .replace("?.", "?")
        .replace(" .", ".")
        .replace(" ,", ",")
        .replace('"', "")
        .replace("'", "")
        .replace("AI", "Ây Ai")
        .replace("A.I", "Ây Ai")
    )
    return text


def run_tts(XTTS_MODEL, lang, tts_text, speaker_audio_file,
            normalize_text= True,
            verbose=False,
            output_chunks=False):
    """
    Run text-to-speech (TTS) synthesis using the provided XTTS_MODEL.

    Args:
        XTTS_MODEL: A pre-trained TTS model.
        lang (str): The language of the input text.
        tts_text (str): The text to be synthesized into speech.
        speaker_audio_file (str): Path to the audio file of the speaker to condition the synthesis on.
        normalize_text (bool, optional): Whether to normalize the input text. Defaults to True.
        verbose (bool, optional): Whether to print verbose information. Defaults to False.
        output_chunks (bool, optional): Whether to save synthesized speech chunks separately. Defaults to False.

    Returns:
        str: Path to the synthesized audio file.
    """

    if XTTS_MODEL is None or not speaker_audio_file:
        return "You need to run the previous step to load the model !!", None, None

    output_dir = "PythonBE/AudioOutputs"
    os.makedirs(output_dir, exist_ok=True)

    gpt_cond_latent, speaker_embedding = XTTS_MODEL.get_conditioning_latents(
        audio_path=speaker_audio_file,
        gpt_cond_len=XTTS_MODEL.config.gpt_cond_len,
        max_ref_length=XTTS_MODEL.config.max_ref_len,
        sound_norm_refs=XTTS_MODEL.config.sound_norm_refs,
    )

    if normalize_text and lang == "vi":
        # Bug on google colab
        try:
            tts_text = normalize_vietnamese_text(tts_text)
        except:
            cry_and_quit()

    if lang in ["ja", "zh-cn"]:
        tts_texts = tts_text.split("。")
    else:
        tts_texts = sent_tokenize(tts_text)

    if verbose:
        print("Text for TTS:")
        pprint(tts_texts)

    wav_chunks = []
    for text in tqdm(tts_texts):
        if text.strip() == "":
            continue

        wav_chunk = XTTS_MODEL.inference(
            text=text,
            language=lang,
            gpt_cond_latent=gpt_cond_latent,
            speaker_embedding=speaker_embedding,
            temperature=0.3,
            length_penalty=1.0,
            repetition_penalty=10.0,
            top_k=30,
            top_p=0.85,
        )

        # Quick hack for short sentences
        keep_len = calculate_keep_len(text, lang)
        wav_chunk["wav"] = torch.tensor(wav_chunk["wav"][:keep_len])

        if output_chunks:
            out_path = os.path.join(output_dir, f"{get_file_name()}.wav")
            torchaudio.save(out_path, wav_chunk["wav"].unsqueeze(0), 24000)
            if verbose:
                print(f"Saved chunk to {out_path}")

        wav_chunks.append(wav_chunk["wav"])

    out_wav = torch.cat(wav_chunks, dim=0).unsqueeze(0)
    out_path = os.path.join(output_dir, f"{get_file_name()}.wav")
    torchaudio.save(out_path, out_wav, 24000)

    if verbose:
        print(f"Saved final file to {out_path}")

    return out_path


language_code_map = {
    "Tiếng Việt": "vi",
    "Tiếng Anh": "en",
    "Tiếng Tây Ban Nha": "es",
    "Tiếng Pháp": "fr",
    "Tiếng Đức": "de",
    "Tiếng Ý": "it",
    "Tiếng Bồ Đào Nha": "pt",
    "Tiếng Ba Lan": "pl",
    "Tiếng Thổ Nhĩ Kỳ": "tr",
    "Tiếng Nga": "ru",
    "Tiếng Hà Lan": "nl",
    "Tiếng Séc": "cs",
    "Tiếng Ả Rập": "ar",
    "Tiếng Trung (giản thể)": "zh-cn",
    "Tiếng Nhật": "ja",
    "Tiếng Hungary": "hu",
    "Tiếng Hàn": "ko",
    "Tiếng Hindi": "hi"
}

print("> Đang nạp mô hình...")
try:
    vixtts_model = None
    if not vixtts_model:
        vixtts_model = load_model(xtts_checkpoint="vixtts-demo/model/model.pth",
                                xtts_config="vixtts-demo/config.json",
                                xtts_vocab="vixtts-demo/vocab.json")
except:
    vixtts_model = load_model(xtts_checkpoint="vixtts-demo/model/model.pth",
                                xtts_config="vixtts-demo/model/config.json",
                                xtts_vocab="vixtts-demo/model/vocab.json")
clear_output()
print("> Đã nạp mô hình")

if not os.path.exists(reference_audio):
    print("⚠️⚠️⚠️Bạn chưa tải file âm thanh lên. Hãy chọn giọng khác, hoặc tải file của bạn lên ở bên dưới.⚠️⚠️⚠️")
    audio_file="/content/model/vi_sample.wav"
else:
    audio_file = run_tts(vixtts_model,
            lang=language_code_map[language],
            tts_text=input_text,
            speaker_audio_file=reference_audio,
            normalize_text=normalize_text,
            verbose=verbose,
            output_chunks=output_chunks,)

from IPython.display import Audio
Audio(audio_file)


# import torch
# from TTS.api import TTS

# # Get device
# device = "cuda" if torch.cuda.is_available() else "cpu"

# # List available 🐸TTS models
# print(TTS().list_models())

# # Init TTS
# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# # Run TTS
# # Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# # Text to speech list of amplitude values as output

# wav = tts.tts(text, speaker_wav="PythonBE/GiangVoiceEn.wav", language="en")
# # Text to speech to a file
# tts.tts_to_file(text, speaker_wav="PythonBE/GiangVoiceEn.wav", language="en", file_path="PythonBE/RogerPenroseEn_output2.wav")
