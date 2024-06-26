import proglog
from moviepy.editor import VideoFileClip

import tkinter
import tkinter.ttk as ttk

class ProgressBar():
    def __init__(self, progress_bar: ttk.Progressbar, log_label: tkinter.Label, cancel_button: tkinter.Button):
        self.progress_bar = progress_bar
        self.log_label = log_label
        self.cancel_button = cancel_button

class WriteVideoProgress(proglog.ProgressBarLogger):
    def __init__(self, progress_bar: ProgressBar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.progress = progress_bar.progress_bar
        self.log_label = progress_bar.log_label
        self.cancel_button = progress_bar.cancel_button
        self.reading_audio = False

    def callback(self, *_, **__):
        pass

    def bars_callback(self, bar, attr, value, old_value=None):
        total = self.bars[bar]["total"]
        progress_value = int(value / total * 100)
        progress_value = 99 if 100 <= progress_value else progress_value
        if old_value is None:
            self.reading_audio = not self.reading_audio
        if self.reading_audio:
            msg = "音声の読み込み中...  {}/{}".format(value, total)
        else:
            msg = "\n動画の書き出し中...  {}/{}".format(value, total)
            if value == total:
                msg = "完了しました！"
                progress_value = 100
                self.cancel_button["text"] = "閉じる"
        self.log_label["text"] = msg
        self.log_label.update()
        self.progress.configure(value=float(progress_value))
        self.progress.update()

def build(input_file, output_file):

    root = tkinter.Tk()
    root.title(u"TransTube - MOV to MP4")

    # 動画情報を取得
    video_clip = VideoFileClip(input_file)

    # 解像度を取得
    width = video_clip.size[0]
    height = video_clip.size[1]
    rotation = video_clip.rotation
    fps = video_clip.fps
    duration = video_clip.duration
    print("video_clip.size:", width, height, rotation, fps, duration)
    
    label = tkinter.Label(root, text="音声の読み込み中...")
    label.pack()

    # プログレスバー配置
    progbar = ttk.Progressbar(root, length=400, mode="determinate", maximum=100)
    progbar.pack(side=tkinter.LEFT)

    cancel_button = tkinter.Button(root, text="キャンセル")
    cancel_button.pack(side=tkinter.RIGHT)
    
    progress_bar = ProgressBar(progbar, label, cancel_button)

    # MOV動画をMP4に変換して保存
    scale = f"scale={width}:{height}"
    if rotation == 90:
        scale = f"scale={height}:{width}"
    video_clip.write_videofile(output_file, codec='libx264', ffmpeg_params=["-vf", scale], logger=WriteVideoProgress(progress_bar))

    root.mainloop()
