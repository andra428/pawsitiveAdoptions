from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Contact(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  phone= models.CharField(max_length=255)
class Pet2(models.Model):
  path=models.ImageField(upload_to='images/')
  name=models.CharField(max_length=100)
  race=models.CharField(max_length=100)
  age=models.IntegerField()
  health=models.CharField(max_length=100)
  size=models.CharField(max_length=100)
  hair=models.CharField(max_length=100)
  description=models.CharField(max_length=255,default='none')
  class Meta:
        managed = False

class Animal(models.Model):
  path=models.ImageField(upload_to='images/')
  animal = models.CharField(max_length=100, default="Dog")
  name=models.CharField(max_length=100)
  race=models.CharField(max_length=100)
  age=models.IntegerField(null= True, default=10)
  type_age = models.CharField(max_length=100, null=True, default="Months")
  size=models.CharField(max_length=100)
  hair=models.CharField(max_length=100)
  gender=models.CharField(max_length=50,default="Female")
  weight = models.IntegerField(default=15)
  adopted=models.BooleanField(default=0)
  description=models.CharField(max_length=255,default='none')

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, null=True)
    role = models.BooleanField()
    animal = models.CharField(max_length=100, null=True)
    race=models.CharField(max_length=100, null=True)
    age=models.IntegerField(null= True)
    type_age = models.CharField(max_length=100, null=True)
    size=models.CharField(max_length=100, null=True)
    hair=models.CharField(max_length=100, null=True)
    gender=models.CharField(max_length=50, null=True)
    description=models.CharField(max_length=255, null=True)
    housing_environment = models.CharField(max_length=300, null=True, default="mediu de gazduire")
    experience_history = models.CharField(max_length=300, null=True, default="experienta/istoric")

class CustomUserIdleId(models.Model):
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    idle = models.ForeignKey(Animal, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('customuser', 'idle')

class CustomUserIdAnimalScore(models.Model):
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    idAnimal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    score = models.IntegerField(null= True)
    heScore = models.IntegerField(null= True)
    ehScore = models.IntegerField(null= True)
    state = models.CharField(max_length=100, null=True)
    class Meta:
        unique_together = ('customuser', 'idAnimal')

class CustomUserMessages(models.Model):
    sender = models.ForeignKey(CustomUser,related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser,related_name='received_messages', on_delete=models.CASCADE)
    idAnimal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    subject = models.CharField(max_length=255, null=True)
    message = models.CharField(max_length=355, null=True)
    isNew = models.BooleanField(null=True, default=False)
    status = models.CharField(max_length=355, null=True)

    class Meta:
        unique_together = ('sender', 'receiver', 'date')
    
    