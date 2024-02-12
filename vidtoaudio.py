from moviepy.video.io.VideoFileClip import VideoFileClip

def video_to_audio(video_path, audio_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)


video_to_audio('input2.mp4','output.wav')