
import os
import subprocess

folder = 'ProcessFiles'

# delete all the files in the ProcessFiles folder

# for filename in os.listdir(folder):
#     file_path = os.path.join(folder, filename)
#     print(file_path)
#     if os.path.isfile(file_path):
#         os.remove(file_path)


# # record an audio file

# def record_audio(output_path="ProcessFiles/to_be_translated.wav"):
#     command = [
#         "ffmpeg",
#         "-f", "alsa",
#         "-i", "default",
#         output_path
#     ]
#     subprocess.run(command)
# to_be_translated_file_path = os.path.join(folder, "to_be_translated.wav")
# record_audio(to_be_translated_file_path)

to_be_translated_file_path = os.path.join("..", folder, "to_be_translated.wav") # ".." is for signing out of the whisper.cpp folder

# Define the command
command = [
    "./build/bin/whisper-cli",
    "-m", "models/ggml-tiny.bin",
    "-f", to_be_translated_file_path,
    "-otxt",
    "-l", "en"
]

# Set working directory to where whisper.cpp is located
working_dir = "whisper.cpp"  # ← change this to your actual path

# Run the command
result = subprocess.run(command, cwd=working_dir, capture_output=True, text=True)

# Print output or error
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
