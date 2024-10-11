import os
import wave

import librosa
import nltk
import speech_recognition as sr
import torch
from nltk.sentiment import SentimentIntensityAnalyzer
from pyannote.audio import Pipeline
from pyAudioAnalysis import ShortTermFeatures
from pydub import AudioSegment
from scipy.io import wavfile
from transformers import pipeline

# Download VADER lexicon if not already downloaded
nltk.download('vader_lexicon')

# Set device to GPU if available, otherwise use CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

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

# Analyze sentiment using VADER
def analyze_sentiment(transcription):
    """Analyze sentiment of the given transcription."""
    sia = SentimentIntensityAnalyzer()
    sentiment_dict = sia.polarity_scores(transcription)

    score = sentiment_dict['compound']  # Overall sentiment score
    sentiment_label = 'Neutral'

    if score >= 0.05:
        sentiment_label = 'Positive'
    elif score <= -0.05:
        sentiment_label = 'Negative'

    return {
        'score': score,
        'label': sentiment_label
    }

# Perform speaker diarization on the audio file
def speaker_diarization(audio_path):
    """Perform speaker diarization on the audio file."""
    pipeline_diarization = Pipeline.from_pretrained(
        "pyannote/speaker-diarization",
        use_auth_token=os.getenv('HUGGINGFACE_TOKEN'),
        device=device
    )
    diarization = pipeline_diarization({"uri": "filename", "audio": audio_path})
    speaker_segments = []

    for turn, _, speaker in diarization.itertracks(yield_label=True):
        speaker_segments.append(f"Speaker {speaker}: {turn.start:.1f}s to {turn.end:.1f}s")

    return speaker_segments

def extract_keywords(transcription):
    """Extract unique keywords from transcription."""
    words = transcription.split()
    keywords = list(set(words))  # Example: unique words as keywords
    return keywords

# Extract emotion features using pyAudioAnalysis
def extract_emotion_features(audio_path):
    """Extract emotion features from the audio file."""
    try:
        [Fs, x] = wavfile.read(audio_path)
        features, _ = ShortTermFeatures.feature_extraction(x, Fs, 0.050 * Fs, 0.025 * Fs)
        return features
    except Exception as e:
        raise ValueError(f"Error extracting emotion features: {str(e)}")

# Main function to analyze audio
def analyze_audio(file_path):
    """Analyze the audio file and return transcription, duration, keywords, and sentiment."""
    audio_file = AudioSegment.from_file(file_path)
    duration = len(audio_file) / 1000  # duration in seconds

    # Transcribe audio
    transcription = speech_to_text(file_path)

    # Perform sentiment analysis
    sentiment_score = analyze_sentiment(transcription)

    # Get keywords
    keywords = extract_keywords(transcription)

    results = {
        'transcription': transcription,
        'duration': f"{duration:.2f} seconds",
        'keywords': keywords,
        'sentiment': sentiment_score,
    }

    return results

# Optionally, use librosa for emotion features extraction
def extract_emotion_features_librosa(audio_path):
    """Extract MFCC features using librosa."""
    try:
        y, sr = librosa.load(audio_path, sr=None)  # Use original sampling rate
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        return mfcc
    except Exception as e:
        raise ValueError(f"Error extracting MFCC features: {str(e)}")
