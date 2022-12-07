from django.shortcuts import render


# add here the functions handling the html pages. routing


def index(request):
    return render(request, 'index.html')


# Create your views here.

def input_processor(request):
    input_text = request.POST['input_text']
    new_input = input_text + ' shai'
    return render(request, 'input_processor.html', {'new_input': new_input})
