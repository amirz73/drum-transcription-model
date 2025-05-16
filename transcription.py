### transcription.py
#```python
import yt_dlp as youtube_dl
from pydub import AudioSegment
import os
from drum_model import TranscriptionModel  # from cloned repo
from music21 import converter, stream


def download_audio(youtube_url: str, output_dir: str) -> str:
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, 'audio.%(ext)s'),
        'quiet': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info)
    # convert to wav
    wav_path = os.path.splitext(filename)[0] + '.wav'
    audio = AudioSegment.from_file(filename)
    audio.export(wav_path, format='wav')
    return wav_path


def transcribe_and_generate_pdf(youtube_url: str, output_dir: str) -> str:
    # 1. Download audio
    wav_path = download_audio(youtube_url, output_dir)
    
    # 2. Transcribe drums
    model = TranscriptionModel()
    notes = model.transcribe(wav_path)  # returns list of (time, drum_type)

    # 3. Build MusicXML
    score = stream.Score()
    part = stream.Part()
    for onset, drum in notes:
        n = stream.Note()  # choose percussion note mapping
        n.duration.quarterLength = 0.25  # example
        part.append(n)
    score.append(part)

    xml_path = os.path.join(output_dir, 'drum_score.musicxml')
    score.write('musicxml', fp=xml_path)

    # 4. Convert to PDF via MuseScore CLI
    pdf_path = os.path.join(output_dir, 'drum_score.pdf')
    os.system(f"mscore '{xml_path}' -o '{pdf_path}'")

    return pdf_path
#```
