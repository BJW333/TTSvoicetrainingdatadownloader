import yt_dlp
from pathlib import Path
from pydub import AudioSegment, silence

script_dir = Path(__file__).parent
output_audio_dir = script_dir / "downloaded_audio"
clipped_audio_dir = script_dir / "clipped_audio"
output_audio_dir.mkdir(exist_ok=True)
clipped_audio_dir.mkdir(exist_ok=True)

#configure yt-dlp for downloading audio
def download_audio(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_audio_dir / '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

#process and segment pieces of audio based on silence detection
def process_audio(file_path, silence_thresh=-40, min_silence_len=500, segment_duration_ms=5000):
    audio = AudioSegment.from_wav(file_path)
    chunks = silence.split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    
    for i, chunk in enumerate(chunks):
        segment_filename = clipped_audio_dir / f"{file_path.stem}_clip_{i+1}.wav"
        chunk.export(segment_filename, format="wav")
        print(f"Saved clip: {segment_filename}")

def download_and_process_youtube_audio(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch',
        'max_downloads': 3,
        'outtmpl': str(output_audio_dir / '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])
        
    #process all downloaded audio files
    for audio_file in output_audio_dir.glob("*.wav"):
        process_audio(audio_file)

if __name__ == "__main__":
    query = input("Put in whoevers voice you want to gather wav files on ex(robert downey jr interview): ")
    download_and_process_youtube_audio(query)
