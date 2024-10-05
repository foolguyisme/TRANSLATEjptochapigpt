import openai
import os
import time

#OpenAI API金鑰
openai.api_key = "XXX"

def convert_audio_to_text(audio_file):
    with open(audio_file, "rb") as audio:
        try:
            response = openai.Audio.transcribe("whisper-1", audio, language="ja")  # 使用Whisper模型進行語音識別，指定語言為日文(你也能換其他的)
            print(f"Transcribed Text: {response['text']}")
            return response['text']
        except openai.error.OpenAIError as e:
            print(f"API請求失敗: {e}")
            return None

def save_as_srt(transcribed_text, filename="output.srt"):
    srt_content = []
    lines = transcribed_text.split('。')  #假設每句話結尾

    for i, line in enumerate(lines):
        #計算文本時間(每段)這邊假設3秒
        start_time = i * 3
        end_time = (i + 1) * 3

        start_time_str = f"00:00:{start_time:02},000"
        end_time_str = f"00:00:{end_time:02},000"

        srt_content.append(f"{i + 1}")
        srt_content.append(f"{start_time_str} --> {end_time_str}")
        srt_content.append(line.strip())
        srt_content.append("")  # 空行

    #將內容寫入SRT
    if srt_content:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(srt_content))
        print(f"SRT 文件已保存為 {filename}")
    else:
        print("沒有內容可保存到 SRT 文件。")

def translate_srt_to_chinese(input_srt, output_srt):
    translated_srt_content = []

    with open(input_srt, 'r', encoding='utf-8') as file:
        srt_content = file.readlines()

    for line in srt_content:
        #忽略空行與時間
        if "-->" not in line and not line.strip().isdigit():
            line_to_translate = line.strip()

            #使用GPT模型翻譯日文到中文
            response = openai.ChatCompletion.create(
                # model="gpt-4",使用 gpt-4模型
                model="gpt-3.5-turbo",  # 使用 gpt-3.5-turbo 模型
                messages=[
                    {"role": "system", "content": "你是一個專業的翻譯家，將日文翻譯成中文。"},
                    {"role": "user", "content": f"將以下日文翻譯成中文：{line_to_translate}"}
                ]
            )
            translated_text = response['choices'][0]['message']['content'].strip()
            translated_srt_content.append(translated_text)
        else:
            translated_srt_content.append(line.strip())

    #將翻譯內容寫入SRT
    with open(output_srt, 'w', encoding='utf-8') as file:
        file.write("\n".join(translated_srt_content))

    print(f"中文 SRT 文件已保存為 {output_srt}")

if __name__ == "__main__":
    audio_file = "C:/Users/User/Desktop/翻譯api/test.wav"  #替會為自身音頻路徑
    transcribed_text = convert_audio_to_text(audio_file)

    #減少頻率
    time.sleep(1)  # 延遲

    #將日文保存至SRT
    if transcribed_text:
        srt_filename = "C:/Users/User/Desktop/翻譯api/japanese_output.srt" 
        save_as_srt(transcribed_text, srt_filename)

        #翻譯SRT到中文
        translate_srt_to_chinese(srt_filename, "C:/Users/User/Desktop/翻譯api/chinese_output.srt")
    else: 
        print("未識別到任何文本。")
