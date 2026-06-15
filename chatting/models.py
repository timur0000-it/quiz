from django.db import models
from users.models import CustomerUser

# Create your models here.
class Room(models.Model):
    title = models.CharField()
    teacher = models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    students = models.ManyToManyField(CustomerUser,related_name="student_rooms")
    category = models.CharField(null=True,blank=True)
    dificulty = models.CharField(null=True,blank=True)
    question = models.URLField(default='https://opentdb.com/api.php?amount=1&category=25&difficulty=easy')
   
class Answer(models.Model):
    student = models.ForeignKey(CustomerUser,on_delete=models.CASCADE,related_name="student_answers")
    room = models.ForeignKey(Room,on_delete=models.CASCADE,default=None)
    right = models.IntegerField(default=0)
    total_count = models.IntegerField(default=0)

