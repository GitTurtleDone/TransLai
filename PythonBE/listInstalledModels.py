import os
from pathlib import Path

def list_installed_coqui_models():
    tts_cache_dir = Path.home() / ".local" / "share" / "tts"
    
    if not tts_cache_dir.exists():
        print("❌ No models found. Coqui-TTS cache directory does not exist.")
        return

    print("📦 Installed Coqui-TTS models:\n")
    for model_dir in sorted(tts_cache_dir.iterdir()):
        if model_dir.is_dir():
            model_name = model_dir.name.replace("--", "/")
            print(f"✅ {model_name}\n   📁 {model_dir}\n")
    print(tts_cache_dir)
# Run it
list_installed_coqui_models()
