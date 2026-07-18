from django.test import TestCase
from rest_framework.test import APIClient
from .models import User
class AuthTests(TestCase):
    def test_patient_registration_is_approved(self):
        r=APIClient().post('/api/auth/register/',{'username':'patient','email':'p@example.com','password':'strongpass123','first_name':'Pat','last_name':'Example','role':'patient'},format='json')
        self.assertEqual(r.status_code,201); self.assertTrue(User.objects.get(username='patient').is_approved)
    def test_doctor_registration_requires_approval(self):
        r=APIClient().post('/api/auth/register/',{'username':'doctor','email':'d@example.com','password':'strongpass123','first_name':'Doc','last_name':'Example','role':'doctor'},format='json')
        self.assertEqual(r.status_code,201); self.assertFalse(User.objects.get(username='doctor').is_approved)
