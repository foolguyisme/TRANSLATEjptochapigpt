import openai
import speech_recognition as sr
from pydub import AudioSegment
import os
import imageio_ffmpeg as ffmpeg
import time

# FFmpeg路徑
ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
print(f"FFmpeg executable path: {ffmpeg_exe}")

# 設置FFmpeg的路徑
AudioSegment.converter = ffmpeg_exe

# OpenAI API
openai.api_key = 'XXX'

def convert_audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="ja-JP")
            print(f"Recognized Text: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition 無法理解音頻")
        except sr.RequestError as e:
            print(f"無法請求結果; {e}")

    return None

def translate_text(text, target_language="zh"):
    if text:
        prompt = f"Translate the following Japanese text to Chinese: {text}"

        try:
            # 使用的gpt模型
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )
            translated_text = response['choices'][0]['message']['content'].strip()
            print(f"Translated Text: {translated_text}")
            return translated_text
        
        except openai.error.RateLimitError:
            print("API額度")
            return None
    else:
        print("無法翻譯")
        return None

def save_as_srt(translated_text_list, filename="output.srt"):
    srt_content = []
    for i, translated_text in enumerate(translated_text_list):
        start_time = i * 5
        end_time = (i + 1) * 5
        start_time_str = f"00:00:{start_time:02},000"
        end_time_str = f"00:00:{end_time:02},000"

        srt_content.append(f"{i + 1}")
        srt_content.append(f"{start_time_str} --> {end_time_str}")
        srt_content.append(translated_text)
        srt_content.append("")

    # 將內容寫入SRT
    if srt_content:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(srt_content))
        print(f"SRT 文件已保存為 {filename}")
    else:
        print("沒有內容可保存到 SRT 文件。")

if __name__ == "__main__":
    audio_file = "C:/Users/User/Desktop/翻譯api/test.wav"  # 替換為你的音頻文件的正確路徑

    text = convert_audio_to_text(audio_file)

    # 減少頻率雖然我不知道有沒有用
    time.sleep(1)  # 延遲

    translated_text_list = []

    translated_text = translate_text(text, target_language="zh")
    if translated_text:
        translated_text_list.append(translated_text)  # 將翻譯文本添加到列表

    time.sleep(1)

    # 保存翻譯結果
    save_as_srt(translated_text_list, "C:/Users/User/Desktop/翻譯api/translated_output.srt")

    if os.path.exists("temp.wav"):
        os.remove("temp.wav")
