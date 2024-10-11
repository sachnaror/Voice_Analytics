import os

import librosa
import speech_recognition as sr
from pyannote.audio import Pipeline
from pyAudioAnalysis import ShortTermFeatures
from pydub import AudioSegment
from scipy.io import wavfile  # Correct import for reading WAV files
from transformers import pipeline


# Convert audio file to WAV format using pydub if necessary
def convert_to_wav(audio_path):
    try:
        audio = AudioSegment.from_file(audio_path)
        wav_path = os.path.splitext(audio_path)[0] + '.wav'
        audio.export(wav_path, format='wav')
        return wav_path
    except Exception as e:
        raise ValueError(f"Error converting file to WAV: {str(e)}")

# Convert speech to text using Google Web Speech API
def speech_to_text(audio_path):
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
    sentiment_analyzer = pipeline('sentiment-analysis')
    result = sentiment_analyzer(text)
    return result

# Extract emotion features using pyAudioAnalysis (short-term features)
def extract_emotion_features(audio_path):
    try:
        # Load the audio file
        [Fs, x] = wavfile.read(audio_path)

        # Extract short-term features
        features, _ = ShortTermFeatures.feature_extraction(x, Fs, 0.050 * Fs, 0.025 * Fs)
        return features
    except Exception as e:
        raise ValueError(f"Error extracting emotion features: {str(e)}")

# Speaker diarization using pyannote.audio
def speaker_diarization(audio_path):
    try:
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")
        diarization = pipeline({"uri": "filename", "audio": audio_path})
        speaker_segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            speaker_segments.append(f"Speaker {speaker}: {turn.start:.1f}s to {turn.end:.1f}s")
        return speaker_segments
    except Exception as e:
        raise ValueError(f"Error during speaker diarization: {str(e)}")

# Main function to analyze audio
def analyze_audio(audio_path):
    # Speech-to-text
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

# Optionally, use librosa for emotion features extraction
def extract_emotion_features_librosa(audio_path):
    try:
        y, sr = librosa.load(audio_path)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        return mfcc
    except Exception as e:
        raise ValueError(f"Error extracting MFCC features: {str(e)}")
