import os

import librosa
import speech_recognition as sr
import torch
from pyannote.audio import Pipeline
from pyAudioAnalysis import ShortTermFeatures
from pydub import AudioSegment
from scipy.io import wavfile  # Correct import for reading WAV files
from transformers import pipeline

# Set device to GPU if available, otherwise use CPU
device = 0 if torch.cuda.is_available() else -1

# Convert audio file to WAV format using pydub if necessary
def convert_to_wav(audio_path):
    """Convert audio file to WAV format."""
    try:
        audio = AudioSegment.from_file(audio_path)
        wav_path = os.path.splitext(audio_path)[0] + '.wav'
        audio.export(wav_path, format='wav')
        return wav_path
    except Exception as e:
        raise ValueError(f"Error converting file to WAV: {str(e)}")

# Convert speech to text using Google Web Speech API
def speech_to_text(audio_path):
    """Transcribe speech to text from an audio file."""
    recognizer = sr.Recognizer()

    # Convert to WAV format if the file is not in WAV
    if not audio_path.endswith('.wav'):
        audio_path = convert_to_wav(audio_path)

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "Could not request results; check your network connection."

# Analyze sentiment using Hugging Face Transformers pipeline
def analyze_sentiment(text):
    """Analyze sentiment of the given text."""
    sentiment_analyzer = pipeline(
        'sentiment-analysis',
        model='distilbert/distilbert-base-uncased-finetuned-sst-2-english',
        device=device  # Use GPU if available
    )
    result = sentiment_analyzer(text)
    return result

def speaker_diarization(audio_path):
    """Perform speaker diarization on the audio file."""
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization",
        use_auth_token=os.getenv('HUGGINGFACE_TOKEN'),  # Use environment variable for the token
        device=device  # Use GPU if available
    )
    diarization = pipeline({"uri": "filename", "audio": audio_path})
    speaker_segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        speaker_segments.append(f"Speaker {speaker}: {turn.start:.1f}s to {turn.end:.1f}s")
    return speaker_segments

# Extract emotion features using pyAudioAnalysis (short-term features)
def extract_emotion_features(audio_path):
    """Extract emotion features from the audio file."""
    try:
        [Fs, x] = wavfile.read(audio_path)

        # Extract short-term features
        features, _ = ShortTermFeatures.feature_extraction(x, Fs, 0.050 * Fs, 0.025 * Fs)
        return features
    except Exception as e:
        raise ValueError(f"Error extracting emotion features: {str(e)}")

# Main function to analyze audio
def analyze_audio(file_path):
    # Implement your analysis logic here
    # This function should return the analysis results
    # For example, it could return a dictionary of results
    results = {
        'transcription': 'Sample transcription of the audio',
        'duration': '5 seconds',
        'keywords': ['keyword1', 'keyword2'],
        'sentiment': [{'score': 0.75}],  # Example sentiment score
    }
    return results

# Optionally, use librosa for emotion features extraction
def extract_emotion_features_librosa(audio_path):
    """Extract MFCC features using librosa."""
    try:
        y, sr = librosa.load(audio_path)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        return mfcc
    except Exception as e:
        raise ValueError(f"Error extracting MFCC features: {str(e)}")
