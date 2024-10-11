# analytics/views.py
from django.contrib import messages  # For user notifications
from django.shortcuts import redirect, render

from .forms import AudioFileForm
from .utils import analyze_audio


def upload_audio(request):
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                # Save the uploaded audio file
                form.save()
                audio_path = form.instance.audio_file.path

                # Analyze the audio
                analysis_result = analyze_audio(audio_path)

                # Render results page
                return render(request, 'analytics/result.html', {'result': analysis_result})
            except Exception as e:
                # Handle any errors that occur during analysis
                messages.error(request, f"An error occurred while processing the audio: {str(e)}")
                return redirect('upload_audio')  # Redirect to the upload page for another attempt
        else:
            messages.error(request, "There was an error with your form submission.")
    else:
        form = AudioFileForm()

    return render(request, 'analytics/upload.html', {'form': form})
