from django.db import models
from django.contrib.auth import get_user_model

class Type(models.Model):
    choices=models.CharField(max_length=200)

    def __str__(self):
        return f"{self.choices}"
class Exam(models.Model):
    subject=models.CharField(max_length=200)
    sluge=models.SlugField()
    type=models.ForeignKey(Type,on_delete=models.PROTECT)
    def __str__(self):
        return f"{self.subject}"
class Question(models.Model):
    exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
    question=models.CharField(max_length=400)
    user_answer=models.SmallIntegerField(null=True,blank=True)
    def __str__(self):
        return f"{self.question}"

class AnswerQuestion(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    answer=models.SmallIntegerField()
class Evaluation(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    exam=models.ForeignKey(Exam,on_delete=models.PROTECT)
    grade=models.SmallIntegerField()
    def __str__(self):
        return f"{self.user} -- {self.grade} -- {self.exam}"
