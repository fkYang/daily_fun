import os,shutil
import subprocess
import ffmpeg
import torch
import whisper

def convert_wem_to_wav(input_wem_path, output_wav_path):
    try:
        # 下载的vgmstream地址
        command = [r"D:\SoftWare\tools\video\vgmstream\vgmstream-cli", input_wem_path, "-o", output_wav_path]
        subprocess.run(command, check=True)
        # 调用 FFmpeg 进行转换
        #ffmpeg.input(input_wem_path).output(output_wav_path, acodec='pcm_s16le').run()
        print(f"转换完成: {output_wav_path}")
    except ffmpeg.Error as e:
        print(f"转换失败: {e.stderr.decode()}")

def process_dir(file_dir, target_path):
    for dir_path, dirs, files in os.walk(file_dir):
        wem_files = [f for f in files if f.endswith(".wem")]
        print(wem_files)
        for wem_file in wem_files:
            current_target_path = target_path
            if dir_path != file_dir:
                current_target_path = os.path.join(target_path, os.path.relpath(dir_path, file_dir))
            print("file: cu " + os.path.join(dir_path, wem_file))
            print("file: target " + os.path.join(target_path, current_target_path, wem_file))
            try:
                process_file(dir_path, wem_file, current_target_path)
            except Exception  as e:
                print(f"发生异常: {e}")

def process_file(file_pre_dir, file_name, target_path):  # 获取文件
    # 读取音频，tts，重命名
    video_title = os.path.splitext(os.path.basename(file_name))[0]
    target_wav_file_path = os.path.join(target_path, "wav", video_title + ".wav")
    if not os.path.exists(os.path.join(target_path, "wav")):
        os.makedirs(os.path.join(target_path, "wav"))

    print("file final: target" + target_wav_file_path)
    convert_wem_to_wav(os.path.join(file_pre_dir, file_name), target_wav_file_path)

    result = model.transcribe(target_wav_file_path, language="zh")
    new_title= video_title
    if result["text"]:
        new_title = new_title + "_" + result["text"]

    new_title = new_title[: 50]
    final_fil_path = os.path.join(target_path, new_title + ".wav")
    print("file final: target" + final_fil_path)
    shutil.copy(target_wav_file_path, final_fil_path)


def main():
    wem_path = r"D:\data\video\soundData\myth_unpark\Exports\b1\Content\00Main\Audio\SoundBank\Media\Chinese"
    #wem_path = r"C:\Users\yfk\Videos\temp\ffmtp\origin"
    target_path = r"C:\Users\yfk\Videos\temp\ffmtp\ttarget"
    target_path = r"D:\data\video\soundData\myth_wav"
    process_dir(wem_path, target_path)

if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("small", device=device)
    main()
