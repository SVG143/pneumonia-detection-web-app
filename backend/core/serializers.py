from rest_framework import serializers
from .models import User,Analysis,Review

class UserSerializer(serializers.ModelSerializer):
    class Meta: model=User; fields=['id','username','email','first_name','last_name','role','is_approved']
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=8)
    class Meta: model=User; fields=['username','email','password','first_name','last_name','role']
    def create(self,data): return User.objects.create_user(**data,is_approved=data.get('role')=='patient')
class ReviewSerializer(serializers.ModelSerializer):
    doctor_name=serializers.CharField(source='doctor.get_full_name',read_only=True)
    class Meta: model=Review; fields=['id','doctor','doctor_name','notes','reviewed_at']; read_only_fields=['doctor']
class AnalysisSerializer(serializers.ModelSerializer):
    review=ReviewSerializer(read_only=True)
    patient_name=serializers.CharField(source='patient.get_full_name',read_only=True)
    class Meta: model=Analysis; fields=['id','patient','patient_name','image','predicted_class','confidence','status','model_version','created_at','review']; read_only_fields=['patient','predicted_class','confidence','status','model_version']
