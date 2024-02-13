# from celery import shared_task
# from django.db import transaction
# from accounts.models import User
# from exam.models import AnswerQuestion, Evaluation, Exam
# from exam.models import Question
#
# @shared_task
# def evaluate_exam(user_national_code,exam_id,course_id):
#     types=Question.TYPE
#
#     print(course_id)
#     user_national_code=User.objects.get(national_code=user_national_code)
#     user_answers=AnswerQuestion.objects.filter(user=user_national_code,exam=exam_id)
#     exam_obj=Exam.objects.get(id=exam_id)
#     # with transaction.atomic():
#     #     for i in range(len(types)):
#     #         answers = []
#     #         points=0
#     #         for user_answer in user_answers:
#     #             if user_answer.question.type==i+1 and user_answer.answer != 9:
#     #                 answers.append(user_answer)
#     #                 print(f"answers {answers} ")
#     #         for j in answers:
#     #             points += int(j.answer)
#     #         if points == 0 :
#     #             grade=0
#     #         else:
#     #             grade=float(points/len(answers))
#     #         Evaluation.objects.create(
#     #             user=user_national_code, exam=exam_obj, grade=grade,
#     #             talent=i + 1
#     #         )
#
