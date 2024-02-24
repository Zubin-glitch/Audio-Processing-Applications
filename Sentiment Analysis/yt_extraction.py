from fileinput import filename
import ffmpeg
from pytube import YouTube
import os
from moviepy.editor import AudioFileClip
import moviepy.editor as mp
import imageio_ffmpeg as ffmpeg  


def create_audio_file(video_url):
    
    # Create a YouTube object and get the stream with audio.
    print(f"Creating YouTube object...")
    yt = YouTube(video_url)
    video_title = yt.title
    print("Generating audio file from given video url...")
    audio_stream = yt.streams.filter(only_audio=True).first()

    ffmpeg.get_ffmpeg_exe()

    # Download the audio stream to a file.
    print("Downloading audio file...")
    audio_stream.download(output_path= os.getcwd())

    # Load the downloaded audio file (replace 'audio_file.mp4' with your file).
    output_file_path = os.getcwd() + os.sep + video_title + ".mp4"
    audio_clip = AudioFileClip(output_file_path)

    output_filename = video_title + '_audio.wav'
    output_file_path = os.getcwd() + os.sep + output_filename
    # Convert to .wav format (pcm_s16le codec)
    print(f"Converting the audio file to requisite format for transcription and sentiment analysis...")
    audio_clip.write_audiofile(output_file_path, codec='pcm_s16le')
    print(f"Please find the audio file generated here:{output_file_path} \nWith name: {output_filename}")
    return output_filename, video_title

# main conditional guard
if __name__ == '__main__':
    video_url = "https://www.youtube.com/watch?v=oetTlR3k85I&ab_channel=TheCanadianLad"
    filename, audio_title = create_audio_file(video_url)
    print(f"Filename generated: {filename}\nIt's title is: {audio_title}")




