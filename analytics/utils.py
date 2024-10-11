import speech_recognition as sr


def speech_to_text(audio_path):
    recognizer = sr.Recognizer()
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

from pyAudioAnalysis import audioFeatureExtraction


def extract_emotion_features(audio_path):
    [Fs, x] = audioBasicIO.read_audio_file(audio_path)
    F, f_names = audioFeatureExtraction.st_feature_extraction(x, Fs, 0.050 * Fs, 0.025 * Fs)
    return F  # You can process these features further for emotion detection.


def analyze_audio(audio_path):
    # Convert speech to text
    text = speech_to_text(audio_path)

    # Sentiment Analysis
    sentiment_result = analyze_sentiment(text)

    # Emotion detection (optionally use pyAudioAnalysis or librosa)
    emotion_features = extract_emotion_features(audio_path)

    return {
        "transcription": text,
        "sentiment": sentiment_result,
        "emotion_features": emotion_features
    }
