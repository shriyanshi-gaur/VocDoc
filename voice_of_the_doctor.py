from dotenv import load_dotenv
load_dotenv()

import os
import platform
import subprocess
from gtts import gTTS

# ✅ Step 1a: Basic gTTS TTS (for use without playback)
def text_to_speech_with_gtts_old(input_text, output_filepath):
    tts = gTTS(text=input_text, lang="en", slow=False)
    tts.save(output_filepath)

# ✅ Step 2: gTTS with Auto Playback (cross-platform)
def text_to_speech_with_gtts(input_text, output_filepath="gtts_output.mp3"):
    tts = gTTS(text=input_text, lang="en", slow=False)
    tts.save(output_filepath)

    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run([
                'powershell',
                '-c',
                f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'
            ])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])  # or mpg123, ffplay
        else:
            raise OSError("Unsupported OS")
    except Exception as e:
        print(f"[Audio Error] {e}")

    return output_filepath  # important for Gradio return


# ✅ Manual test
# if __name__ == "__main__":
#     text_to_speech_with_gtts("Hi Shriyanshi! gTTS with autoplay is working.", "gtts_test_output.mp3")
