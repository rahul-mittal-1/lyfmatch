from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomManager
import uuid

# from django.core.exceptions import ValidationError



# Create your models here.
class Religion(models.Model):
    religion=models.CharField(max_length=50)
    
    def __str__(self):
        return self.religion


class Gender(models.Model):
      gender=models.CharField(max_length=50,default="m or f", null=False, blank=False)
      
      def __str__(self):
          return self.gender
    
    
class Height(models.Model):
    height = models.CharField(max_length=120, null=False, blank=False)
    
     
    def __str__(self):
        return str(self.height)


class MotherTongue(models.Model):
    motherTongue = models.CharField(max_length=120, null=False, blank=False)
    
     
    def __str__(self):
        return self.motherTongue


class MaritalStatus(models.Model):
    Marital_Status = models.CharField(max_length=120, null=False, blank=False)
    
     
    def __str__(self):
        return self.Marital_Status


class Country(models.Model):
    country=models.CharField(max_length=120)
    
    def __str__(self):
        return self.country


class State(models.Model):
    state=models.CharField(max_length=120)
    
    def __str__(self):
        return self.state


class Weight(models.Model):
    weight=models.CharField(max_length=120)
    
    def __str__(self):
        return self.weight


class Complexion(models.Model):
    complexion=models.CharField(max_length=120)
    
    def __str__(self):
        return self.complexion

class PhsyicalStatus(models.Model):
    phsyical_status=models.CharField(max_length=120)
    
    def __str__(self):
        return self.phsyical_status

class BloodGroup(models.Model):
    blood_group=models.CharField(max_length=120)
    
    def __str__(self):
        return self.blood_group

class EatingHabits(models.Model):
    eating_habits=models.CharField(max_length=120)
    
    def __str__(self):
        return self.eating_habits

class Education(models.Model):
    education=models.CharField(max_length=120)
    
    def __str__(self):
        return self.education

class Occupation(models.Model):
    occupation=models.CharField(max_length=120)
    
    def __str__(self):
        return self.occupation

class EmployedIn(models.Model):
    employed_in=models.CharField(max_length=120)
    
    def __str__(self):
        return self.employed_in

class Salary(models.Model):
    salary=models.CharField(max_length=120)
    
    def __str__(self):
        return self.salary





class CustomUser(AbstractUser):
    # Add your custom fields here
    username        = None
    email           = models.EmailField("Email Address", unique=True)
    gender 			= models.ForeignKey(Gender,on_delete=models.CASCADE, null=True, blank=True)
    motherTongue 	= models.ForeignKey(MotherTongue,on_delete=models.CASCADE, null=True, blank=True)
    religion 		= models.ForeignKey(Religion, on_delete=models.CASCADE, null=True, blank=True)
    phone 			= models.IntegerField(default=0)
    country 		= models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    state 			= models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)

    maritalStatus 	= models.ForeignKey(MaritalStatus, on_delete=models.CASCADE,null=True, blank=True)
    height 			= models.ForeignKey(Height, on_delete=models.CASCADE,null=True, blank=True)
    weight 			= models.ForeignKey(Weight, on_delete=models.CASCADE,null=True, blank=True)


    accountType_choices = (
        ('free', 'Free'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('mini', 'Mini'),
        ('mini', 'Mini'),
        ('royal', 'Royal'),
        ('grandroyal', 'GrandRoyal'),
    )
    accountType     = models.CharField(max_length=25, choices=accountType_choices, default='free')

    complexion 		= models.ForeignKey(Complexion, on_delete=models.CASCADE,null=True, blank=True)
    phsyicalStatus  = models.ForeignKey(PhsyicalStatus, on_delete=models.CASCADE,null=True, blank=True)
    bloodGroup 	    = models.ForeignKey(BloodGroup, on_delete=models.CASCADE,null=True, blank=True)
    eatingHabits 	= models.ForeignKey(EatingHabits, on_delete=models.CASCADE,null=True, blank=True)
    education 		= models.ForeignKey(Education, on_delete=models.CASCADE,null=True, blank=True)
    occupation 		= models.ForeignKey(Occupation, on_delete=models.CASCADE,null=True, blank=True)
    employedIn 	    = models.ForeignKey(EmployedIn, on_delete=models.CASCADE,null=True, blank=True)
    salary 			= models.ForeignKey(Salary, on_delete=models.CASCADE,null=True, blank=True)

    city 			= models.CharField(max_length=100,null=True)
    age 			= models.IntegerField(default=18)
    about_myself 	= models.CharField(max_length=1000,null=True,verbose_name='About Myself')
    photo 			= models.ImageField(upload_to="media",null=True, blank=True)
    is_subscribed 	= models.BooleanField(default=False)
    is_featured 	= models.BooleanField(default=False)
    

    
    USERNAME_FIELD  = "email"

    REQUIRED_FIELDS = []


    objects = CustomManager()


    def __str__(self):
        return self.email


    @property
    def gender_name(self):
      return self.gender.name




class Profile(models.Model):
    user        = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_id  = models.CharField(max_length=10, unique=True)
    # Add other fields as needed

    def __str__(self):
        return self.profile_id



class Preference(models.Model):
    user 					= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    preferred_gender 		= models.ForeignKey(Gender,on_delete=models.CASCADE, null=True, blank=True)
    preferred_religion 		= models.ForeignKey(Religion, on_delete=models.CASCADE, null=True, blank=True)
    preferred_motherTongue 	= models.ForeignKey(MotherTongue, on_delete=models.CASCADE, null=True, blank=True)
    preferred_maritalstatus = models.ForeignKey(MaritalStatus, on_delete=models.CASCADE,null=True, blank=True)
    min_height 				= models.IntegerField(null=True)
    max_height 				= models.IntegerField(null=True)
    min_age					= models.IntegerField(null=True)
    max_age					= models.IntegerField(null=True)
