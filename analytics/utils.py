import os

import speech_recognition as sr
from pyAudioAnalysis import ShortTermFeatures
from pydub import AudioSegment

# Removed redundant import of ShortTermFeatures as audioFeatureExtraction


def convert_to_wav(audio_path):
    # Load audio file using pydub
    audio = AudioSegment.from_file(audio_path)
    wav_path = os.path.splitext(audio_path)[0] + '.wav'

    # Export the audio file in WAV format
    audio.export(wav_path, format='wav')

    return wav_path

def speech_to_text(audio_path):
    recognizer = sr.Recognizer()

    # Convert the file to WAV if not already in WAV format
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
from transformers import pipeline


def analyze_sentiment(text):
    sentiment_analyzer = pipeline('sentiment-analysis')
    result = sentiment_analyzer(text)
    return result

# Import pyAudioAnalysis correctly and remove duplicates
from pyAudioAnalysis import ShortTermFeatures


def extract_emotion_features(audio_path):
    # Load the audio file
    [Fs, x] = ShortTermFeatures.wavfile.read(audio_path)

    # Extract short-term features using pyAudioAnalysis
    features, _ = ShortTermFeatures.feature_extraction(x, Fs, 0.050 * Fs, 0.025 * Fs)

    return features

# Speaker diarization using pyannote.audio
from pyannote.audio import Pipeline


def speaker_diarization(audio_path):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")
    diarization = pipeline({"uri": "filename", "audio": audio_path})
    speaker_segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        speaker_segments.append(f"Speaker {speaker}: {turn.start:.1f}s to {turn.end:.1f}s")
    return speaker_segments

def analyze_audio(audio_path):
    # Convert speech to text
    text = speech_to_text(audio_path)

    # Sentiment Analysis
    sentiment_result = analyze_sentiment(text)

    # Speaker Diarization
    speakers = speaker_diarization(audio_path)

    # Emotion detection using pyAudioAnalysis
    emotion_features = extract_emotion_features(audio_path)

    return {
        "transcription": text,
        "sentiment": sentiment_result,
        "emotion_features": emotion_features,
        "speaker_segments": speakers
    }

# Optionally, if you prefer librosa over pyAudioAnalysis for emotion features:
import librosa


def extract_emotion_features_librosa(audio_path):
    y, sr = librosa.load(audio_path)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    # Add emotion classification model here, based on extracted MFCCs
    return mfcc
