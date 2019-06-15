from django.db import models
from User.models import User

class Probs (models.Model) :
    title = models.CharField(max_length = 100)
    id = models.IntegerField(primary_key=True)
    test_cases_amount = models.IntegerField()


    def __int__ (self) :
        return self.id

    def __str__ (self) :
        return self.title

    class Meta:
        verbose_name = "Problem"
        verbose_name_plural = "Problems"

class ProbsResult (models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="results")
    probs = models.ForeignKey(Probs, on_delete=models.CASCADE)
    res = models.CharField(max_length = 30)
    
    @property
    def score (self) :
        one = int(100/self.probs.test_cases_amount)
        s = 0
        for r in self.res :
            if r == 'P':
                s+=one
        return s

    