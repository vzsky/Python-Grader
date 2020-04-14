from django import forms
from Problems.models import Probs


class Submission(forms.Form):
    CHOICES = []
    # NOTE: this sorta thing isn't going to work; putting dynamic fields in
    #       __init__ is the way to go.
    # all_pb = Probs.objects.all()
    # for each_pb in all_pb:
    #     Opt = (each_pb.id, each_pb.title)
    #     CHOICES.append(Opt)
    select_id = forms.ChoiceField(choices=CHOICES)
    uploaded_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(Submission, self).__init__(*args, **kwargs)
        self.fields["select_id"] = forms.ChoiceField(
            choices=[(pb.id, pb.title) for pb in Probs.objects.all()]
        )
