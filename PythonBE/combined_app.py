
# for running ffmpeg and whisper.cpp
import os
import subprocess
# for running MarianMT
from transformers import MarianMTModel, MarianTokenizer
# for running vixtts
from pprint import pprint
import torch
import torchaudio
from tqdm import tqdm
from underthesea import sent_tokenize
# from unidecode import unidecode
from IPython.display import clear_output
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware 


# global variable
ipt_lang = 'en'
opt_lang = 'vi'
process_folder = 'ProcessFiles' # the folder where processing files are stored
#-------------------------------------
# clean process folder
def clean_process_folder():

    global process_folder
    
    for filename in os.listdir(process_folder):
        file_path = os.path.join(process_folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
#--------------------------------------

#--------------------------------------
# set up to record an audio
ipt_audio_file_path = os.path.join(process_folder, "ipt.wav")
opt_audio_file_path = os.path.join(process_folder, "opt.wav")


def record_audio(opt_audio_path):
    subprocess.run([
    "ffmpeg",
    "-f", "alsa",
    "-i", "default",
    opt_audio_path
    ], check=True)
#--------------------------------------


#--------------------------------------
# set up to transcribe the recorded audio
whisper_ipt_audio_file_path = os.path.join("..", process_folder, "ipt.wav") # ".." is for signing out of the whisper.cpp folder
# Define the command to be run from the terminal
whisper_command = [
    "./build/bin/whisper-cli",
    "-m", "models/ggml-tiny.bin",
    "-f", whisper_ipt_audio_file_path,
    "-otxt",
    "-l", ipt_lang
]

# set working directory to where whisper.cpp is located
whisper_working_dir = "whisper.cpp"  # ← change this to your actual path

def transcribe_input_audio():
    
    global whisper_command
    global whisper_working_dir
    # print('went in transcribe_input_audio')
    # Run the command
    result = subprocess.run(whisper_command, cwd=whisper_working_dir, capture_output=True, text=True)
    
    # Print output or error
    # print("STDOUT:", result.stdout)
    # print("STDERR:", result.stderr)
#--------------------------------------

#--------------------------------------
# set up to translate the input text using MarianMT
marianMT_model_name = 'Helsinki-NLP/opus-mt-' + ipt_lang + '-' + opt_lang
tokenizer = MarianTokenizer.from_pretrained(marianMT_model_name)
marianMT_model = MarianMTModel.from_pretrained(marianMT_model_name)

# define the path to the input.txt file
ipt_txt_file_path = os.path.join('.', process_folder, 'ipt.wav.txt')#"./ProcessFiles/ipt.wav.txt"
opt_txt_file_path = os.path.join(process_folder, "opt.txt")

def translate_text():

    # set up to translate the input text using MarianMT
    global marianMT_model_name
    global tokenizer
    global marianMT_model
    global ipt_txt_file_path
    global opt_txt_file_path

    # Read the contents of the file
    with open(ipt_txt_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

 
    batch = tokenizer([text], return_tensors="pt")
    gen = marianMT_model.generate(**batch)
    translation = tokenizer.decode(gen[0], skip_special_tokens=True)

    with open(opt_txt_file_path, 'w', encoding='utf-8') as file:
        file.write(translation)
#---------------------------------------

# set up to tts the translated text
# The inference code is adapted from https://github.com/coqui-ai/TTS/blob/dev/TTS/demos/xtts_ft_demo/xtts_demo.py
# and https://github.com/thinhlpg/vixtts-demo/blob/main/viXTTS_Demo.ipynb

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

# @markdown Chọn giọng mẫu:
reference_audio = "PythonBE/sample_voice_" + opt_lang+ ".wav" 
# @markdown Tự động chuẩn hóa chữ (VD: 20/11 -> hai mươi tháng mười một)
normalize_text = True # @param {type:"boolean"}
# @markdown In chi tiết xử lý
verbose = False # @param {type:"boolean"}
# @markdown Lưu từng câu thành file riêng lẻ.
output_chunks = False # @param {type:"boolean"}

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
    global process_folder

    if XTTS_MODEL is None or not speaker_audio_file:
        return "You need to run the previous step to load the model !!", None, None

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
            out_path = os.path.join(process_folder, "opt.wav")
            torchaudio.save(out_path, wav_chunk["wav"].unsqueeze(0), 24000)
            if verbose:
                print(f"Saved chunk to {out_path}")

        wav_chunks.append(wav_chunk["wav"])

    out_wav = torch.cat(wav_chunks, dim=0).unsqueeze(0)
    out_path = os.path.join(process_folder, "opt.wav")
    torchaudio.save(out_path, out_wav, 24000)

    if verbose:
        print(f"Saved final file to {out_path}")

    return out_path


def text_to_speech():
    global opt_txt_file_path 
    global reference_audio
    with open(opt_txt_file_path, 'r', encoding='utf-8') as file:
        opt_text = file.read()

    if not os.path.exists(reference_audio):
        print("⚠️⚠️⚠️Bạn chưa tải file âm thanh lên. Hãy chọn giọng khác, hoặc tải file của bạn lên ở bên dưới.⚠️⚠️⚠️")
        audio_file=reference_audio
    else:
        audio_file = run_tts(vixtts_model,
                lang=opt_lang,
                tts_text=opt_text,
                speaker_audio_file=reference_audio,
                normalize_text=normalize_text,
                verbose=verbose,
                output_chunks=output_chunks,)

    subprocess.run(["ffplay", "-nodisp", "-autoexit", audio_file])
#-----------------------------------



app = FastAPI()
class RecordTemplate(BaseModel):
    lang_code: str
class Translate(BaseModel):
    ipt_lang_code: str
    opt_lang_code: str
allowed_origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = allowed_origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

def update_languages(ipt, opt):
    global whisper_command
    global reference_audio
    global ipt_lang
    global opt_lang
    global marianMT_model_name
    global tokenizer
    global marianMT_model
    if (ipt_lang != ipt or opt_lang != opt):
        # reset whisper_command
        ipt_lang = ipt
        opt_lang = opt
        whisper_command[7] = ipt
        # reset MarianMT model
        marianMT_model_name = 'Helsinki-NLP/opus-mt-' + ipt_lang + '-' + opt_lang
        tokenizer = MarianTokenizer.from_pretrained(marianMT_model_name)
        marianMT_model = MarianMTModel.from_pretrained(marianMT_model_name)

        # reset template voice
        reference_audio = "PythonBE/sample_voice_" + opt_lang+ ".wav" 
        




@app.post('/record_template')
async def record_template(req: RecordTemplate):
    try:
        opt_audio_path = f'PythonBE/sample_voice_{req.lang_code}.wav'
        if os.path.exists(opt_audio_path):
            os.remove(opt_audio_path)
        record_audio(opt_audio_path)
        return {"message":f"Template voice saved at {opt_audio_path}"}
    except subprocess.CalledProcessError:
        return {"message": "Recording failed"}, 500

@app.post('/translate')
async def translate(req: Translate):
    # global ipt_lang
    # global opt_lang
    # global opt_audio_file_path
    global ipt_audio_file_path
    update_languages(req.ipt_lang_code, req.opt_lang_code)
    # print(whisper_command)
    try: 
        clean_process_folder()
        record_audio(ipt_audio_file_path)
        transcribe_input_audio()
        translate_text()
        text_to_speech()
        return {'message': 'Translated'}
    except subprocess.CalledProcessError:
        return {'message': 'Translating failed'}, 500
""""""
# # @markdown Chọn ngôn ngữ:
# language = "Tiếng Việt" # @param ["Tiếng Việt", "Tiếng Anh","Tiếng Tây Ban Nha", "Tiếng Pháp","Tiếng Đức","Tiếng Ý", "Tiếng Bồ Đào Nha", "Tiếng Ba Lan", "Tiếng Thổ Nhĩ Kỳ", "Tiếng Nga", "Tiếng Hà Lan", "Tiếng Séc", "Tiếng Ả Rập", "Tiếng Trung (giản thể)", "Tiếng Nhật", "Tiếng Hungary", "Tiếng Hàn", "Tiếng Hindi"]
# @markdown Văn bản để đọc. Độ dài tối thiểu mỗi câu nên từ 10 từ để đặt kết quả tốt nhất.

# language_code_map = {
#     "Tiếng Việt": "vi",
#     "Tiếng Anh": "en",
#     "Tiếng Tây Ban Nha": "es",
#     "Tiếng Pháp": "fr",
#     "Tiếng Đức": "de",
#     "Tiếng Ý": "it",
#     "Tiếng Bồ Đào Nha": "pt",
#     "Tiếng Ba Lan": "pl",
#     "Tiếng Thổ Nhĩ Kỳ": "tr",
#     "Tiếng Nga": "ru",
#     "Tiếng Hà Lan": "nl",
#     "Tiếng Séc": "cs",
#     "Tiếng Ả Rập": "ar",
#     "Tiếng Trung (giản thể)": "zh-cn",
#     "Tiếng Nhật": "ja",
#     "Tiếng Hungary": "hu",
#     "Tiếng Hàn": "ko",
#     "Tiếng Hindi": "hi"
# }
