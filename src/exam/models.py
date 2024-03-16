import json

from django.db import models, transaction
from django.contrib.auth import get_user_model
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from courses.models import UserCourse
class Exam(models.Model):
    TYPE=[
        (1,'4-7'),
        (2,'8-11'),
        (3,'12-15'),
        (4,"PARENT"),
    ]
    type=models.SmallIntegerField(choices=TYPE)
    name=models.CharField(max_length=200)
    is_last=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name}"



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


    def __str__(self):
        return f"{self.question}"

    @classmethod
    def get_question_types(cls):
        return cls.TYPE

class AnswerQuestion(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    answer=models.SmallIntegerField()
    exam=models.ForeignKey(Exam,on_delete=models.CASCADE,blank=True,null=True)
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
    grade=models.FloatField()
    talent=models.SmallIntegerField(choices=TALENT,default=1)
    def __str__(self):
        return f"{self.user} -- {self.grade} -- {self.exam}"

    @classmethod
    def evaluate_exam(cls,request, exam_id, course_id):
        types = Question.TYPE
        print(course_id)
        # request = get_user_model().objects.get(national_code=request.user.national_code)
        user_answers = AnswerQuestion.objects.filter(user=request.user, exam=exam_id)
        exam_obj = Exam.objects.get(id=exam_id)
        try:
            with transaction.atomic():
                for i in range(len(types)):
                    answers = []
                    points=0
                    for user_answer in user_answers:
                        if user_answer.question.type==i+1 and user_answer.answer != 9:
                            answers.append(user_answer)
                            print(f"answers {answers} ")
                    for j in answers:
                        points += int(j.answer)
                    if points == 0 :
                        grade=0
                    else:
                        grade=float(points/len(answers))
                    Evaluation.objects.create(
                        user=request.user, exam=exam_obj, grade=grade,
                        talent=i + 1
                    )
            return True
        except Exception as e:
            return False















"""
{
    'user':1,
    answers:{
        "1":9,
        "2":10,
        ...
    }

}




"""