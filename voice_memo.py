import os
import speech_recognition as sr
import threading
import keyboard
import datetime

r = sr.Recognizer()

# outputディレクトリが存在しない場合は作成する
OUTPUT_DIR = "output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 現在の日時からファイル名を生成
now = datetime.datetime.now()
MEMO_FILE = os.path.join(OUTPUT_DIR, now.strftime("%Y-%m-%d_%H-%M-%S_memo.txt"))


def get_audio_from_mic():
    with sr.Microphone(sample_rate=16000) as source:
        audio = r.listen(source, timeout=None)
        return audio


def convert_audio_to_text(audio_data):
    try:
        text = r.recognize_google(audio_data, language="ja-JP")
        print(text)
        save_to_file(text)  # テキストをファイルに保存
    except sr.UnknownValueError:
        pass


def save_to_file(text):
    with open(MEMO_FILE, "a") as file:  # ファイルを追記モードで開く
        file.write(text + "\n")  # テキストをファイルに書き込む


# キーボードからの入力を監視して、'q'キーが押されたらループを抜ける
exit_loop = False


def on_key_event(event):
    global exit_loop
    if event.name == "q":
        exit_loop = True


keyboard.on_press(on_key_event)


def main():
    print("---メモ---")
    # 録音ループ
    while not exit_loop:
        audio_data = get_audio_from_mic()

        # マルチスレッドで音声をテキストに変換
        threading.Thread(target=convert_audio_to_text, args=(audio_data,)).start()


if __name__ == "__main__":
    main()
