from django import forms
from Problems.models import Probs

class Submission (forms.Form):
    all_pb = Probs.objects.all()
    CHOICES = []
    for each_pb in all_pb :
        Opt = (each_pb.id, each_pb.title)
        CHOICES.append(Opt)
    select_id = forms.ChoiceField(choices=CHOICES)
    uploaded_file = forms.FileField()