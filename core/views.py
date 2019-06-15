from django.shortcuts import render, redirect
from Problems.models import Probs
from .forms import Submission
from .Grade import Grade

def home(request):
    if request.method == 'POST' and request.user.is_authenticated:

        form = Submission(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            code = request.FILES['uploaded_file']
            codeid = form.cleaned_data['select_id']

            try :
                prob = Probs.objects.get(pk=codeid)
                Grade(code, prob, request.user)
            except Exception as e :
                print(e)

            return redirect('home')

    all_pb = Probs.objects.all()

    res = request.user.results.all()
    score = 0

    for result in res :
        score += result.score

    

    form = Submission()
    return render(request, 'home.html', {"all_pb" : all_pb, "form" : form, "res" : res, "score" : score})