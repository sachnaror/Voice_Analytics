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


from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render

from .your_analysis_module import \
    analyze_voice_file  # Import your analysis function


def upload_file(request):
    if request.method == 'POST' and request.FILES.get('voice_file'):
        voice_file = request.FILES['voice_file']
        fs = FileSystemStorage()
        filename = fs.save(voice_file.name, voice_file)

        # Call the analysis function with the file path
        analysis_results = analyze_voice_file(fs.url(filename))

        # Pass the results to the results page
        return render(request, 'results.html', {'results': analysis_results})

    return render(request, 'upload.html')


# your_analysis_module.py
def analyze_voice_file(file_path):
    # Implement your analysis logic here
    # This function should return the analysis results
    # For example, it could return a dictionary of results
    results = {
        'transcription': 'Sample transcription of the audio',
        'duration': '5 seconds',
        'keywords': ['keyword1', 'keyword2'],
    }
    return results
