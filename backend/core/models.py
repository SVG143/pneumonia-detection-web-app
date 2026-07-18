from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices): PATIENT='patient','Patient'; DOCTOR='doctor','Doctor'; ADMIN='admin','Admin'
    role=models.CharField(max_length=10,choices=Role.choices,default=Role.PATIENT)
    is_approved=models.BooleanField(default=False)

class Analysis(models.Model):
    class Status(models.TextChoices): PENDING='pending','Pending'; COMPLETE='complete','Complete'; FAILED='failed','Failed'
    patient=models.ForeignKey(User,on_delete=models.CASCADE,related_name='analyses')
    image=models.ImageField(upload_to='xrays/%Y/%m/')
    predicted_class=models.CharField(max_length=20,blank=True)
    confidence=models.FloatField(null=True,blank=True)
    status=models.CharField(max_length=10,choices=Status.choices,default=Status.PENDING)
    model_version=models.CharField(max_length=50,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    analysis=models.OneToOneField(Analysis,on_delete=models.CASCADE,related_name='review')
    doctor=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviews')
    notes=models.TextField()
    reviewed_at=models.DateTimeField(auto_now=True)
