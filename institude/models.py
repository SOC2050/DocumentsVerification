from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class Institute(models.Model):  # Fixed typo in 'Institute'
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.email

    @classmethod 
    def getAdministrator(cls, email, password):
        try:
            adm = cls.objects.get(email=email)
            if password == adm.password : 
                return {'success': True, 'administrator': adm}
            else:
                return {'success': False, 'password': "Password does not match"}
        except cls.DoesNotExist:
            return {'success': False, 'message': "Invalid email" } 

