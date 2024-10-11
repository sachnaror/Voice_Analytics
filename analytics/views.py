# analytics/views.py
from django.shortcuts import redirect, render
from pyAudioAnalysis import ShortTermFeatures as audioFeatureExtraction

from .forms import AudioFileForm
from .utils import analyze_audio


def upload_audio(request):
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            audio_path = form.instance.audio_file.path
            analysis_result = analyze_audio(audio_path)
            return render(request, 'analytics/result.html', {'result': analysis_result})
    else:
        form = AudioFileForm()
    return render(request, 'analytics/upload.html', {'form': form})
