from django.db import models
from django.contrib.auth import get_user_model
from courses.models import UserCourse
class Exam(models.Model):
    TYPE=[
        (1,'4-7'),
        (2,'8-11'),
        (3,'12-15'),
        (4,"PARENT"),
    ]
    type=models.SmallIntegerField(choices=TYPE)
    subject=models.CharField(max_length=200)
    def __str__(self):
        return f"{self.subject}"
class Question(models.Model):
    TYPE = [
        (1, "Verbal talent"),
        (2, "math talent"),
        (3, "space talent"),
        (4, "Science talent"),
        (5, "music talent"),
        (6, "Sports talent"),
        (7, "Social aptitude")
    ]
    exam=models.ForeignKey(Exam,on_delete=models.CASCADE,related_name="questions")
    question=models.CharField(max_length=400)
    type=models.SmallIntegerField(choices=TYPE,default=1)
    is_complete=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.question}"

class AnswerQuestion(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    answer=models.SmallIntegerField()
class Evaluation(models.Model):
    TALENT=[
        (1,"Verbal talent"),
        (2,"math talent"),
        (3,"space talent"),
        (4,"Science talent"),
        (5,"music talent"),
        (6,"Sports talent"),
        (7,"Social aptitude")
    ]
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    exam=models.ForeignKey(Exam,on_delete=models.PROTECT)
    grade=models.SmallIntegerField()
    talent=models.SmallIntegerField(choices=TALENT,default=1)
    def __str__(self):
        return f"{self.user} -- {self.grade} -- {self.exam}"
