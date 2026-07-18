import os
from django.core.management.base import BaseCommand
from core.models import User
class Command(BaseCommand):
    help='Create local demo accounts'
    def handle(self,*args,**kwargs):
        password=os.getenv('DEMO_PASSWORD','DemoPass123!')
        for username,role,approved in [('patient_demo','patient',True),('doctor_demo','doctor',True),('admin_demo','admin',True)]:
            user,_=User.objects.get_or_create(username=username,defaults={'email':f'{username}@example.com','first_name':role.title(),'last_name':'Demo','role':role,'is_approved':approved})
            user.role=role; user.is_approved=approved; user.set_password(password); user.save()
        self.stdout.write(self.style.SUCCESS('Created demo users. Set DEMO_PASSWORD to override the local default.'))
