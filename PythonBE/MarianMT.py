from transformers import MarianMTModel, MarianTokenizer

model_name = 'Helsinki-NLP/opus-mt-en-vi'  # Example: English to Vietnamese
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Define the path to your .txt file
file_path = "./Experiments/whisper.cpp/samples/RogerPenrose.wav.txt"

# Read the contents of the file
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

#text = "Einstein is a theoretical physicist, who created the theory of general relativity."
batch = tokenizer([text], return_tensors="pt")
gen = model.generate(**batch)
translation = tokenizer.decode(gen[0], skip_special_tokens=True)

print(translation)
